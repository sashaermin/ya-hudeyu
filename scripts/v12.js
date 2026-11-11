"use strict";

const CONTACT_EMAIL = "sashaermin@gmail.com";
const contactAvailable = CONTACT_EMAIL !== "CONTACT_EMAIL";
const root = document.documentElement;
const systemTheme = matchMedia("(prefers-color-scheme: dark)");
const themeButton = document.querySelector(".theme");
const galleryTools = document.querySelector(".gallery-tools");
const galleryButtons = document.querySelectorAll("[data-gallery]");
const screens = document.querySelectorAll(".screen");
let galleryOverride;

function currentTheme() {
  return root.dataset.theme || (systemTheme.matches ? "dark" : "light");
}

function screenUrl(id, theme) {
  return `/assets/v12/screens/${id}_${theme}.webp`;
}

function updateGallery(theme) {
  galleryButtons.forEach((button) => {
    button.setAttribute(
      "aria-pressed",
      String(button.dataset.gallery === theme),
    );
  });
  screens.forEach((link) => {
    const url = screenUrl(link.dataset.screen, theme);
    link.href = url;
    link.querySelector("img").src = url;
  });
}

function updateTheme() {
  const theme = currentTheme();
  themeButton.setAttribute("aria-pressed", String(theme === "dark"));
  updateGallery(galleryOverride || theme);
}

updateTheme();
themeButton.dataset.ready = "";
themeButton.addEventListener("click", () => {
  root.dataset.theme = currentTheme() === "dark" ? "light" : "dark";
  try {
    localStorage.setItem("theme", root.dataset.theme);
  } catch {
    /* session only */
  }
  updateTheme();
});
systemTheme.addEventListener("change", updateTheme);
if (galleryTools) galleryTools.hidden = false;
galleryButtons.forEach((button) => {
  button.addEventListener("click", () => {
    galleryOverride = button.dataset.gallery;
    updateGallery(galleryOverride);
  });
});

const viewer = document.querySelector("#viewer");
if (viewer && typeof viewer.showModal === "function") {
  const image = viewer.querySelector("#viewer-image");
  const title = viewer.querySelector("#viewer-title");
  screens.forEach((link) =>
    link.addEventListener("click", (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)
        return;
      event.preventDefault();
      image.src = link.href;
      title.textContent = link.querySelector("img").alt;
      viewer.showModal();
    }),
  );
  viewer
    .querySelector("#close-viewer")
    .addEventListener("click", () => viewer.close());
}

const helpSearch = document.querySelector(".help-search");
if (helpSearch) {
  const input = helpSearch.querySelector("input");
  const clear = helpSearch.querySelector("button");
  const status = helpSearch.querySelector('[role="status"]');
  const links = document.querySelector("[data-help-links]");
  const topicList = document.querySelector(".help-topics");
  const normalize = (value) => value.toLocaleLowerCase("ru").replace(/ё/g, "е");
  const topics = Array.from(topicList.children, (section) => ({
    section,
    link: links.querySelector(`a[href="#${section.id}"]`),
    text: normalize(`${section.textContent} ${section.dataset.helpKeywords}`),
  }));

  function filterHelp() {
    const terms = normalize(input.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const { section, link, text } of topics) {
      const matches = terms.every((term) => text.includes(term));
      section.hidden = link.hidden = !matches;
      if (matches) count++;
    }
    links.hidden = count === 0;
    status.textContent = !terms.length
      ? "Показаны все темы."
      : count
        ? `Найдено тем: ${count}.`
        : "Ничего не найдено. Попробуйте другое слово или очистите поиск.";
  }

  function resetHelp() {
    input.value = "";
    filterHelp();
  }

  helpSearch.addEventListener("submit", (event) => event.preventDefault());
  input.addEventListener("input", filterHelp);
  clear.addEventListener("click", () => {
    resetHelp();
    input.focus();
  });
  topicList.addEventListener("click", (event) => {
    const link = event.target.closest('a[href^="#"]');
    const target = link && document.getElementById(link.hash.slice(1));
    if (target?.hidden) resetHelp();
  });
  filterHelp();
  helpSearch.hidden = false;
}

if (contactAvailable) {
  const contacts = {
    support: { label: CONTACT_EMAIL },
    privacy: {
      label: "Написать по вопросам конфиденциальности",
      subject: "Вопрос о конфиденциальности «Я ХУдЕЮ»",
    },
    bug: {
      label: "Сообщить об ошибке",
      className: "button secondary",
      subject: "Ошибка в приложении «Я ХУдЕЮ»",
      body: [
        "Что произошло и чего вы ожидали:",
        "",
        "Шаги для воспроизведения:",
        "1. ",
        "",
        "Устройство:",
        "Версия Android:",
        "Версия приложения:",
      ].join("\r\n"),
    },
    release: {
      label: "Спросить о выпуске по почте",
      subject: "Сообщите о выходе «Я ХУдЕЮ»",
    },
  };
  document.querySelectorAll("[data-contact]").forEach((placeholder) => {
    const { label, className, subject, body } =
      contacts[placeholder.dataset.contact] ?? contacts.support;
    const fields = [];
    if (subject) fields.push(`subject=${encodeURIComponent(subject)}`);
    if (body) fields.push(`body=${encodeURIComponent(body)}`);

    const link = document.createElement("a");
    link.textContent = label;
    if (className) link.className = className;
    link.href = `mailto:${CONTACT_EMAIL}${fields.length ? "?" + fields.join("&") : ""}`;
    placeholder.replaceChildren(link);
  });
  document.querySelector("[data-bug-report]")?.removeAttribute("hidden");
}

function validRelease(entry) {
  if (!entry || typeof entry !== "object") return false;
  const { version, size, date, android, sha256, url, changes } = entry;
  if (
    ![version, size, date, android, sha256, url].every(
      (value) => typeof value === "string" && value.trim(),
    )
  )
    return false;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^[a-f\d]{64}$/i.test(sha256))
    return false;
  const parsedDate = new Date(date);
  if (
    !Number.isFinite(+parsedDate) ||
    parsedDate.toISOString().slice(0, 10) !== date
  )
    return false;
  if (
    !Array.isArray(changes) ||
    !changes.every((change) => typeof change === "string" && change.trim())
  )
    return false;
  try {
    const apk = new URL(url);
    return (
      apk.protocol === "https:" &&
      !apk.username &&
      !apk.password &&
      /\.apk$/i.test(apk.pathname)
    );
  } catch {
    return false;
  }
}

function element(tag, value) {
  const node = document.createElement(tag);
  if (value !== undefined) node.textContent = value;
  return node;
}

function setReleaseVersion(label) {
  document.querySelectorAll("[data-version], [data-release-title]")
    .forEach((node) => { node.textContent = label; });
}

function setReleaseStatus(label) {
  document.querySelectorAll("[data-release-status]")
    .forEach((node) => { node.textContent = label; });
}

function renderReleases(releases) {
  const latest = releases[0];
  setReleaseVersion(`Версия ${latest.version}`);
  setReleaseStatus("Приложение доступно для Android.");
  document.querySelectorAll("[data-release-label]").forEach((link) => {
    link.textContent = link.dataset.releaseLabel;
  });
  document.querySelectorAll("[data-release-default]").forEach((node) => {
    node.hidden = true;
  });
  document.querySelectorAll("[data-release-details]").forEach((node) => {
    const list = element("dl");
    for (const [label, value] of [
      ["Размер", latest.size],
      ["Дата", latest.date],
      ["Android", latest.android],
      ["SHA-256", latest.sha256],
    ])
      list.append(element("dt", label), element("dd", value));
    node.append(list);
  });
  document.querySelectorAll("[data-apk]").forEach((link) => {
    link.href = latest.url;
    link.hidden = false;
  });
  document.querySelectorAll("[data-releases]").forEach((container) => {
    const limit = Number(container.dataset.limit);
    const history = limit ? releases.slice(0, limit) : releases;
    container.replaceChildren();
    if (limit) container.append(element("h3", "Последние версии"));
    history.forEach((release) => {
      const article = element("article");
      article.append(
        element(
          limit ? "h4" : "h3",
          `Версия ${release.version} · ${release.date}`,
        ),
      );
      if (release.changes.length) {
        const changes = element("ul");
        release.changes.forEach((change) =>
          changes.append(element("li", change)),
        );
        article.append(changes);
      }
      container.append(article);
    });
    if (limit) {
      const all = element("a", "Полная история версий");
      all.href = "/download/#releases";
      container.append(all);
    }
    container.hidden = false;
  });
}

fetch("/releases.json")
  .then((response) => {
    if (!response.ok) throw new Error("Release manifest unavailable");
    return response.json();
  })
  .then((releases) => {
    if (!Array.isArray(releases) || !releases.every(validRelease))
      throw new Error("Invalid release manifest");
    const versions = new Set(releases.map(({ version }) => version.trim()));
    if (versions.size !== releases.length)
      throw new Error("Duplicate release versions");
    // Stable sort keeps the publisher's order for releases on the same day.
    releases.sort((a, b) => b.date.localeCompare(a.date));
    if (releases.length) {
      renderReleases(releases);
    } else if (contactAvailable) {
      document.querySelectorAll('[data-contact="release"]').forEach((contact) => {
        contact.hidden = false;
      });
    }
  })
  .catch(() => {
    setReleaseVersion("Статус выпуска недоступен");
    setReleaseStatus("Не удалось загрузить информацию о выпуске. Попробуйте обновить страницу.");
    document.querySelectorAll("[data-release-history-status]").forEach((status) => {
      status.textContent = "Не удалось загрузить историю версий.";
    });
  });
