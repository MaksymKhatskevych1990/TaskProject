"use strict";

const SEO_LIMITS = {
  seo_title: { idealMin: 50, idealMax: 60, hardMax: 70 },
  seo_description: { idealMin: 140, idealMax: 160, hardMax: 180 },
  seo_h1: { idealMin: 20, idealMax: 70, hardMax: 150 },
  og_title: { idealMin: 50, idealMax: 60, hardMax: 70 },
  og_description: { idealMin: 140, idealMax: 160, hardMax: 180 },
  blog_title: { idealMin: 50, idealMax: 60, hardMax: 70 },
  blog_description: { idealMin: 140, idealMax: 160, hardMax: 180 },
};

function fieldById(name) {
  return document.getElementById(`id_${name}`);
}

function fallbackText() {
  const name = fieldById("name");
  const title = fieldById("title");
  const excerpt = fieldById("excerpt");
  const description = fieldById("description");
  return {
    title: (title && title.value) || (name && name.value) || "Название страницы",
    description:
      (excerpt && excerpt.value) ||
      (description && description.value) ||
      "Краткое описание появится здесь, когда вы заполните Title и Description.",
  };
}

function counterClass(length, limits) {
  if (length === 0 || length > limits.hardMax || length > limits.idealMax + 8) {
    return length === 0 ? "is-warn" : "is-bad";
  }
  if (length >= limits.idealMin && length <= limits.idealMax) {
    return "is-ok";
  }
  return "is-warn";
}

function bindCounter(input) {
  const limits = SEO_LIMITS[input.name];
  if (!limits) {
    return;
  }
  const hint = document.createElement("div");
  hint.className = "seo-counter";
  input.insertAdjacentElement("afterend", hint);

  const render = () => {
    const length = input.value.length;
    hint.className = `seo-counter ${counterClass(length, limits)}`;
    hint.textContent = `${length} / ${limits.idealMax} (идеал ${limits.idealMin}–${limits.idealMax})`;
  };
  input.addEventListener("input", render);
  render();
}

function bindKeywordHint() {
  const keyword = fieldById("focus_keyword");
  const title = fieldById("seo_title");
  const h1 = fieldById("seo_h1");
  if (!keyword || !title) {
    return;
  }
  const hint = document.createElement("div");
  hint.className = "seo-keyword-hint";
  keyword.insertAdjacentElement("afterend", hint);

  const render = () => {
    const query = keyword.value.trim().toLowerCase();
    if (!query) {
      hint.textContent = "";
      hint.className = "seo-keyword-hint";
      return;
    }
    const inTitle = title.value.toLowerCase().includes(query);
    const inH1 = !h1 || !h1.value.trim() || h1.value.toLowerCase().includes(query);
    if (inTitle && inH1) {
      hint.className = "seo-keyword-hint is-ok";
      hint.textContent = "Ключевой запрос есть в Title и H1.";
      return;
    }
    hint.className = "seo-keyword-hint is-warn";
    hint.textContent = "Добавьте ключевой запрос в Title и H1 — так страница лучше попадает в запрос.";
  };

  [keyword, title, h1].filter(Boolean).forEach((input) => {
    input.addEventListener("input", render);
  });
  render();
}

function bindSerpPreview() {
  const titleInput = fieldById("seo_title");
  const descriptionInput = fieldById("seo_description");
  if (!titleInput || !descriptionInput) {
    return;
  }

  const box = document.createElement("div");
  box.className = "seo-serp-preview";
  box.innerHTML = `
    <p class="seo-serp-preview__label">Как это увидит Google</p>
    <div class="seo-serp-preview__url"></div>
    <div class="seo-serp-preview__title"></div>
    <p class="seo-serp-preview__description"></p>
  `;
  titleInput.closest(".form-row, .form-group, .mb-3")?.parentElement?.prepend(box);
  if (!box.parentElement) {
    titleInput.parentElement.insertAdjacentElement("beforebegin", box);
  }

  const urlNode = box.querySelector(".seo-serp-preview__url");
  const titleNode = box.querySelector(".seo-serp-preview__title");
  const descriptionNode = box.querySelector(".seo-serp-preview__description");
  const domainInput = fieldById("domain");

  const render = () => {
    const fallback = fallbackText();
    const title = titleInput.value.trim() || fallback.title;
    const description = descriptionInput.value.trim() || fallback.description;
    const host = (domainInput && domainInput.value.trim()) || window.location.host;
    urlNode.textContent = `https://${host} › страница`;
    titleNode.textContent = title;
    descriptionNode.textContent = description;
  };

  [titleInput, descriptionInput, domainInput, fieldById("name"), fieldById("title"), fieldById("excerpt")]
    .filter(Boolean)
    .forEach((input) => input.addEventListener("input", render));
  render();
}

document.addEventListener("DOMContentLoaded", () => {
  Object.keys(SEO_LIMITS).forEach((name) => {
    const input = fieldById(name);
    if (input) {
      bindCounter(input);
    }
  });
  bindKeywordHint();
  bindSerpPreview();
});
