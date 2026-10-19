# Existing Telegram bot — presentation review

No Hub, Engine, producer, signing, new workflow or new infrastructure is used.
Only existing formatting functions and their offline tests/previews change.
Workflows, triggers, schedules, destinations, credentials, author/agent attribution,
status/check evaluation, timestamps, retry, ledger and delivery code are unchanged.

## Visual review

Download [preview.html](preview.html) and open it locally (mobile width supported).
There are **33 before/after fixtures**, covering every existing formatter and
registered task/stage event type, plus missing metadata, digest and long Unicode /
escaping cases. All data, SHAs and run/artifact IDs are **synthetic**, not evidence
of real work or successful checks. No credential is read and nothing is sent.
Original baseline HTML and final SHA-256 snapshots are in [snapshots.json](snapshots.json).
For display only, broken legacy closing tags are balanced in the before column;
the original baseline payload is retained verbatim in the JSON.

```sh
python3 -m unittest discover -s .github/scripts -p 'test_*.py' -v
python3 .github/scripts/preview_telegram.py
python3 .github/scripts/preview_telegram.py --write  # Local gallery only
python3 -m compileall -q .github/scripts
```

Local result: **71 tests, 2 existing registry-dependent skips**. The
registries exist only on application development branches, not this infrastructure
base; fixture-based behavior, delivery mocks and presentation tests run normally.
Differential checks compare the complete selected visible body and every href
against pre-change snapshots, not merely the presence of a few headings. Event
wording/icons, unknown/uncertain disclaimers, authors, agents, numbers and times
remain intact. Static function-body checks confirm no non-format function changed.

## Length and presentation differences

- Shared frame: bold `Я ХУдЕЮ | DEV REPORTS`, Android / Website / Windows label,
  bold existing event title, compact separator, sections and technical blockquotes.
- Existing Russian descriptions are retained; English subjects and missing fields
  are not translated or replaced with invented summaries. The differing source
  provenance/check policies are preserved, not upgraded to Hub verification.
- Android/Website keep their 4096 HTML-character budget; Windows digest keeps 3900.
  Windows normal messages historically budget decoded Telegram text (escaped HTML
  can exceed 4096 characters). All reviewed outputs also obey Telegram's 4096
  UTF-16 visible-unit ceiling, close their tags and preserve complete entities.
- Existing field truncation/summary selection remains. Already deliverable baseline
  content is never shortened further for branding: compact layout removes optional
  styling first. A pathological full card may retain the old frame if adding the
  new one cannot fit; data and links take priority over decoration.
- Existing oversized Unicode payloads retain their original data/truncation
  behavior verbatim instead of receiving a new clipping policy. They may still
  exceed Telegram's visible UTF-16 limit: this is a known legacy limitation,
  demonstrated by the long_unicode fixture, not a successful delivery claim.
  It cannot safely be fixed as part of this presentation-only rollout.
- Windows' separate manual plaintext routing-test message is unchanged; it is not
  a production report formatter. No fake timestamps or provenance fields are added
  to report types that did not have them.

## Safe publication and CI boundary

The review branch uses a commit containing `[skip actions]` and ends with
`Agent: Codex`. Android's existing push notifier accepts **all branches**; an
ordinary push could send a real message. GitHub's documented skip instruction
prevents push/PR workflows for this preparation commit without editing any trigger.
Website/Windows review branches also use this instruction and do not match their
working-branch notification filters. No workflow dispatch or rerun is authorized.
Consequently no successful hosted CI is claimed for this commit; local results
above are the available evidence. Read-only checks can be arranged only after
owner review without invoking notification workflows. Existing scheduled jobs and
their normal activity coverage are not altered by this PR.

Do not merge, deploy, change secrets/settings or send Telegram during review.
