"use strict";

const CYRILLIC_TO_LATIN = {
  shch: "shch",
  sh: "sh",
  ch: "ch",
  ts: "ts",
  kh: "kh",
  zh: "zh",
  ye: "ye",
  yi: "yi",
  yu: "yu",
  ya: "ya",
  yo: "yo",
  а: "a",
  б: "b",
  в: "v",
  г: "h",
  ґ: "g",
  д: "d",
  е: "e",
  є: "ye",
  ж: "zh",
  з: "z",
  и: "y",
  і: "i",
  ї: "yi",
  й: "y",
  к: "k",
  л: "l",
  м: "m",
  н: "n",
  о: "o",
  п: "p",
  р: "r",
  с: "s",
  т: "t",
  у: "u",
  ф: "f",
  х: "kh",
  ц: "ts",
  ч: "ch",
  ш: "sh",
  щ: "shch",
  ь: "",
  ы: "y",
  ъ: "",
  э: "e",
  ё: "yo",
  ю: "yu",
  я: "ya",
};

function transliterate(value) {
  const normalized = value.toLowerCase().replace(/'/g, "");
  let result = "";
  let index = 0;

  while (index < normalized.length) {
    let matched = false;
    for (const size of [4, 3, 2, 1]) {
      const chunk = normalized.slice(index, index + size);
      if (Object.prototype.hasOwnProperty.call(CYRILLIC_TO_LATIN, chunk)) {
        result += CYRILLIC_TO_LATIN[chunk];
        index += size;
        matched = true;
        break;
      }
    }
    if (!matched) {
      result += normalized[index];
      index += 1;
    }
  }

  return result;
}

function latinSlugify(value) {
  return transliterate(value)
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .trim()
    .replace(/[\s_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function bindLatinSlug(sourceSelector, slugSelector) {
  const source = document.querySelector(sourceSelector);
  const slug = document.querySelector(slugSelector);
  if (!source || !slug) {
    return;
  }

  let manual = Boolean(slug.value);

  slug.addEventListener("input", () => {
    manual = true;
  });

  source.addEventListener("input", () => {
    if (manual) {
      return;
    }
    const nextSlug = latinSlugify(source.value);
    slug.value = nextSlug || "post";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  bindLatinSlug("#id_title", "#id_slug");
  bindLatinSlug("#id_name", "#id_slug");
});
