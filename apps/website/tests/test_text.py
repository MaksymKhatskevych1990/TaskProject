"""Tests for website text helpers."""

from apps.website.text import ensure_unique_slug, is_latin_slug, latin_slugify
from apps.website.models import BlogPost, BlogCategory
from tests.base import BaseTestCase


class WebsiteTextTests(BaseTestCase):
    """Verify slug transliteration helpers."""

    def test_latin_slugify_transliterates_ukrainian_title(self) -> None:
        """Ukrainian titles become readable Latin slugs."""
        self.assertEqual(
            latin_slugify("Як підготувати сайт до SEO"),
            "yak-pidgotuvaty-sayt-do-seo",
        )

    def test_latin_slugify_transliterates_russian_title(self) -> None:
        """Russian titles are transliterated as well."""
        self.assertEqual(
            latin_slugify("Внедрение AI-систем"),
            "vnedrenye-ai-system",
        )

    def test_is_latin_slug_rejects_cyrillic(self) -> None:
        """Cyrillic slugs are treated as invalid."""
        self.assertFalse(is_latin_slug("внедрение-ai-систем"))
        self.assertTrue(is_latin_slug("vnedrenie-ai-system"))

    def test_ensure_unique_slug_adds_suffix(self) -> None:
        """Duplicate slugs receive numeric suffixes."""
        category = BlogCategory.objects.create(name="SEO", slug="seo")
        BlogPost.objects.create(
            title="First",
            slug="seo-checklist",
            excerpt="Excerpt",
            content="Body",
            category=category,
            status="published",
        )

        unique_slug = ensure_unique_slug(BlogPost, "seo-checklist")

        self.assertEqual(unique_slug, "seo-checklist-2")
