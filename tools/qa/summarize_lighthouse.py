#!/usr/bin/env python3
"""Keep the actual mobile production Lighthouse scores and limitations."""
import json
import os
from pathlib import Path
import sys

report_path = Path(sys.argv[1])
report = json.loads(report_path.read_text())
if report.get('runtimeError'):
    raise ValueError(report['runtimeError'])
assert report['finalDisplayedUrl'].startswith('https://yahudeyu-app.ru/')
assert report['configSettings']['formFactor'] == 'mobile'
targets = {'performance': 90, 'accessibility': 95, 'best-practices': 95, 'seo': 95}
scores = {key: round(report['categories'][key]['score'] * 100) for key in targets}
metrics = {key: report['audits'][key]['numericValue'] for key in
           ['first-contentful-paint', 'largest-contentful-paint', 'speed-index',
            'total-blocking-time', 'cumulative-layout-shift']}
summary = dict(url=report['finalDisplayedUrl'], fetched_at=report['fetchTime'],
               lighthouse_version=report['lighthouseVersion'], form_factor='mobile',
               scores=scores, targets=targets, metrics=metrics,
               below_target=[key for key in targets if scores[key] < targets[key]],
               run_warnings=report.get('runWarnings', []),
               failed_audits=[dict(id=key, title=audit['title'], score=audit.get('score'))
                              for key, audit in report['audits'].items()
                              if audit.get('score') is not None and audit['score'] < 1],
               limitation='One simulated mobile lab run on GitHub runner; not real-user/device metrics. '
                          'SEO below target is expected while intentional noindex is retained; '
                          'do not enable indexing solely to improve the score.')
report_path.with_suffix('.summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
if os.environ.get('GITHUB_ACTIONS') == 'true':
    # Compact, non-secret API evidence survives expiring artifact URLs.
    print('::notice title=Production Lighthouse measured::' + json.dumps(summary, ensure_ascii=False))
