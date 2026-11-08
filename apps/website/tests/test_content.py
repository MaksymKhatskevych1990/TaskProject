"""Public site content API and settings admin tests."""

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status

from apps.website.admin import SiteSeoSettingsAdmin
from apps.website.cms_seed import seed_site_content
from apps.website.models import SiteNavLink, SiteOffice, SiteSeoSettings, SiteService
from tests.base import BaseAPITestCase
from tests.factories.accounts import UserFactory


class SiteContentAPITests(BaseAPITestCase):
    """Verify the public CMS payload."""

    def test_content_includes_contacts_and_blocks(self) -> None:
        """The content endpoint exposes brand, contacts, and seeded blocks."""
        seed_site_content()

        response = self.client.get(reverse("api:v1:website:site-content"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        data = response.data["data"]
        self.assertEqual(data["brand"], "Chameleon Digital Studio")
        self.assertEqual(data["email"], "hello@chameleon.digital")
        self.assertEqual(data["telegramUsername"], "devcraft_studio")
        self.assertGreaterEqual(len(data["nav"]), 4)
        self.assertEqual(data["nav"][0]["href"], "/poslugy")
        self.assertEqual(data["hero"]["offers"][0]["id"], "site")
        self.assertEqual(data["pricing"][1]["slug"], "business")
        self.assertTrue(data["offices"][0]["isHeadquarters"])
        self.assertIn("seo", data)

    def test_content_reflects_admin_contact_changes(self) -> None:
        """Editing contacts on the settings row updates the public API."""
        settings, _ = SiteSeoSettings.objects.get_or_create(pk=1)
        settings.phone = "+380999000111"
        settings.email = "studio@example.com"
        settings.telegram_username = "chameleon_studio"
        settings.hero_title = "Запускаємо продукти"
        settings.save()

        response = self.client.get(reverse("api:v1:website:site-content"))

        data = response.data["data"]
        self.assertEqual(data["phone"], "+380999000111")
        self.assertEqual(data["email"], "studio@example.com")
        self.assertEqual(data["telegramUsername"], "chameleon_studio")
        self.assertEqual(data["hero"]["title"], "Запускаємо продукти")


class SiteSettingsAdminTests(BaseAPITestCase):
    """Verify the settings page stays a singleton."""

    def test_cannot_add_a_second_settings_row(self) -> None:
        """Add is hidden after the singleton exists."""
        SiteSeoSettings.objects.get_or_create(pk=1)
        admin = SiteSeoSettingsAdmin(SiteSeoSettings, AdminSite())
        request = RequestFactory().get("/admin/")
        request.user = UserFactory(is_staff=True, is_superuser=True)

        self.assertFalse(admin.has_add_permission(request))
        self.assertFalse(admin.has_delete_permission(request))

    def test_seed_creates_nav_only_once(self) -> None:
        """Re-running the seed does not duplicate blocks."""
        seed_site_content()
        seed_site_content()

        self.assertEqual(SiteSeoSettings.objects.count(), 1)
        self.assertEqual(SiteNavLink.objects.count(), 4)


class UpgradeMarketingContentTests(BaseAPITestCase):
    """Verify the conversion/SEO content upgrade command."""

    def test_upgrade_sets_keyword_h1_and_remote_office(self) -> None:
        """The command writes commercial H1 copy and honest Dnipro NAP."""
        from django.core.management import call_command

        seed_site_content()
        call_command("upgrade_marketing_content")

        settings = SiteSeoSettings.objects.get(pk=1)
        self.assertEqual(settings.seo_h1, "Розробка сайтів під ключ")
        self.assertEqual(settings.hero_primary_cta, "Отримати розрахунок")
        office = SiteOffice.objects.get(site=settings, slug="dnipro")
        self.assertEqual(office.street_address, "")
        self.assertEqual(office.address_locality, "Дніпро")
        self.assertFalse(SiteOffice.objects.filter(street_address__icontains="Хрещатик").exists())
        titles = list(SiteService.objects.order_by("ordering").values_list("title", flat=True))
        self.assertIn("Інтернет-магазини", titles)
        self.assertIn("Контекстна реклама", titles)
        self.assertIn("CRM та внутрішні системи", titles)
