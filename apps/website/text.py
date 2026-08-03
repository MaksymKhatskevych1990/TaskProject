"""Text helpers for public website content."""

from __future__ import annotations

import re

from django.db.models import Model
from django.utils.text import slugify

CYRILLIC_TO_LATIN: dict[str, str] = {
    "щ": "shch",
    "ш": "sh",
    "ч": "ch",
    "ц": "ts",
    "х": "kh",
    "ж": "zh",
    "є": "ye",
    "ї": "yi",
    "ю": "yu",
    "я": "ya",
    "ґ": "g",
    "ё": "yo",
    "э": "e",
    "ы": "y",
    "ъ": "",
    "ь": "",
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "h",
    "д": "d",
    "е": "e",
    "з": "z",
    "и": "y",
    "і": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
}

LATIN_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def transliterate_cyrillic(text: str) -> str:
    """Convert Cyrillic characters to Latin equivalents."""
    normalized = text.lower().replace("'", "")
    result: list[str] = []
    index = 0

    while index < len(normalized):
        matched = False
        for size in (4, 3, 2, 1):
            chunk = normalized[index : index + size]
            if chunk in CYRILLIC_TO_LATIN:
                result.append(CYRILLIC_TO_LATIN[chunk])
                index += size
                matched = True
                break
        if not matched:
            result.append(normalized[index])
            index += 1

    return "".join(result)


def latin_slugify(text: str) -> str:
    """Build a URL-safe Latin slug from arbitrary text."""
    transliterated = transliterate_cyrillic(text)
    slug = slugify(transliterated, allow_unicode=False)
    return slug or "post"


def is_latin_slug(value: str) -> bool:
    """Return whether the slug contains only lowercase Latin characters."""
    return bool(value) and LATIN_SLUG_RE.fullmatch(value) is not None


def ensure_unique_slug(
    model_class: type[Model],
    base_slug: str,
    *,
    exclude_pk: int | None = None,
) -> str:
    """Return a unique slug for the given model."""
    slug = base_slug
    counter = 2

    while True:
        queryset = model_class.objects.filter(slug=slug)
        if exclude_pk is not None:
            queryset = queryset.exclude(pk=exclude_pk)
        if not queryset.exists():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1
