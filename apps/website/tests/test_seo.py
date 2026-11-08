"""Public SEO field and API tests."""

from datetime import datetime
from datetime import timezone as dt_timezone

from django.urls import reverse
from rest_framework import status

from apps.website.models import BlogCategory, BlogPost, SiteSeoSettings
from apps.website.seo_defaults import HOME_DESCRIPTION, HOME_TITLE
from tests.base import BaseAPITestCase


class SiteSeoAPITests(BaseAPITestCase):
    """Verify public SEO settings and article overrides."""

    def test_seo_settings_use_defaults_when_empty(self) -> None:
        """An empty settings row still returns usable homepage copy."""
        response = self.client.get(reverse("api:v1:website:seo-settings"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["seo"]["title"], HOME_TITLE)
        self.assertEqual(response.data["data"]["seo"]["description"], HOME_DESCRIPTION)
        self.assertTrue(response.data["data"]["seo"]["h1"])
        self.assertFalse(response.data["data"]["seo"]["noindex"])
        self.assertEqual(SiteSeoSettings.objects.count(), 1)

    def test_seo_settings_return_admin_values(self) -> None:
        """Filled admin fields are exposed to the public site."""
        settings, _ = SiteSeoSettings.objects.get_or_create(pk=1)
        settings.seo_title = "Студія сайтів у Києві — Chameleon"
        settings.seo_description = "Робимо сайти, магазини і боти під ключ за 14 днів."
        settings.seo_h1 = "Сайти під ключ для бізнесу"
        settings.focus_keyword = "розробка сайтів Київ"
        settings.blog_title = "Блог про розробку сайтів"
        settings.google_site_verification = "abc123"
        settings.save()

        response = self.client.get(reverse("api:v1:website:seo-settings"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["data"]
        self.assertEqual(data["seo"]["title"], "Студія сайтів у Києві — Chameleon")
        self.assertEqual(data["seo"]["h1"], "Сайти під ключ для бізнесу")
        self.assertEqual(data["seo"]["focusKeyword"], "розробка сайтів Київ")
        self.assertEqual(data["blogTitle"], "Блог про розробку сайтів")
        self.assertEqual(data["googleSiteVerification"], "abc123")

    def test_blog_detail_includes_resolved_seo(self) -> None:
        """Article SEO falls back to the post title and excerpt."""
        category, _ = BlogCategory.objects.get_or_create(
            slug="seo",
            defaults={"name": "SEO"},
        )
        BlogPost.objects.create(
            title="Чеклист запуску",
            slug="seo-launch-checklist-test",
            excerpt="Що перевірити перед релізом",
            content="Текст",
            category=category,
            status="published",
            published_at=datetime(2026, 7, 15, tzinfo=dt_timezone.utc),
            seo_title="Чеклист запуску сайту — 12 пунктів",
            seo_h1="Як запустити сайт без втрати трафіку",
        )

        response = self.client.get(
            reverse(
                "api:v1:website:blog-detail",
                kwargs={"slug": "seo-launch-checklist-test"},
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        seo = response.data["data"]["seo"]
        self.assertEqual(seo["title"], "Чеклист запуску сайту — 12 пунктів")
        self.assertEqual(seo["h1"], "Як запустити сайт без втрати трафіку")
        self.assertEqual(seo["description"], "Що перевірити перед релізом")
        self.assertFalse(response.data["data"]["noindex"])
