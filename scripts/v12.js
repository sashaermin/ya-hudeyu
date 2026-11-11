"use strict";

const CONTACT_EMAIL = "CONTACT_EMAIL";
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
  document.querySelectorAll(".theme-image").forEach((image) => {
    image.src = screenUrl(image.dataset.screen, theme);
  });
  updateGallery(galleryOverride || theme);
}

updateTheme();
themeButton.hidden = false;
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

if (CONTACT_EMAIL !== "CONTACT_EMAIL") {
  document.querySelectorAll("[data-contact]").forEach((placeholder) => {
    const link = document.createElement("a");
    const aboutRelease = placeholder.dataset.contact === "release";
    link.textContent = aboutRelease
      ? "Сообщить о выходе"
      : "Связаться по электронной почте";
    const subject = aboutRelease
      ? "?subject=" + encodeURIComponent("Сообщите о выходе «Я ХУдЕЮ»")
      : "";
    link.href = `mailto:${CONTACT_EMAIL}${subject}`;
    placeholder.replaceChildren(link);
  });
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

function renderReleases(releases) {
  const latest = releases[0];
  document
    .querySelectorAll("[data-version], [data-release-title]")
    .forEach((node) => {
      node.textContent = `Версия ${latest.version}`;
    });
  document.querySelectorAll("[data-release-status]").forEach((node) => {
    node.textContent = "Доступна для Android";
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
    if (limit) container.append(element("h3", "Что нового"));
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
      const all = element("a", "Все обновления");
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
    if (releases.length) renderReleases(releases);
  })
  .catch(() => {
    document.querySelectorAll("[data-release-status]").forEach((node) => {
      node.textContent =
        "Не удалось загрузить информацию о выпуске. Попробуйте обновить страницу.";
    });
  });
