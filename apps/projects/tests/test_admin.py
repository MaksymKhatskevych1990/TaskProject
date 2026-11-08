"""Project admin permission and note tests."""

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Permission
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.accounts.choices import UserRole
from apps.projects.admin import ProjectAdmin
from apps.projects.choices import ProjectStatus
from apps.projects.models import Project
from tests.factories.accounts import UserFactory
from tests.factories.projects import ProjectFactory


def _fieldset_fields(fieldsets) -> list[str]:
    """Flatten admin fieldset field names."""
    fields: list[str] = []
    for _name, options in fieldsets:
        fields.extend(options["fields"])
    return fields


def _note_inline_payload() -> dict[str, str]:
    """Return an empty readonly note inline formset payload."""
    return {
        "notes-TOTAL_FORMS": "0",
        "notes-INITIAL_FORMS": "0",
        "notes-MIN_NUM_FORMS": "0",
        "notes-MAX_NUM_FORMS": "0",
    }


class ProjectAdminTests(TestCase):
    """Verify server credentials stay superuser-only in admin."""

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.project_admin = ProjectAdmin(Project, AdminSite())
        self.project = ProjectFactory(
            name="Redwood",
            slug="redwood",
            domain="redwood.studio",
            server_host="10.0.0.8",
            server_password="super-secret-password",
            extra_credentials="cms: admin / hunter2",
        )
        self.superuser = UserFactory(
            email="root@example.com",
            role=UserRole.ADMIN,
            is_staff=True,
            is_superuser=True,
            first_name="Root",
            last_name="Admin",
        )
        self.staff = UserFactory(
            email="staff@example.com",
            role=UserRole.ADMIN,
            is_staff=True,
            is_superuser=False,
            first_name="Staff",
            last_name="Admin",
        )
        staff_permissions = Permission.objects.filter(
            content_type__app_label="projects",
            codename__in=(
                "change_project",
                "view_project",
                "view_projectnote",
            ),
        )
        self.staff.user_permissions.add(*staff_permissions)

    def test_secret_fieldset_visible_only_to_superuser(self) -> None:
        """Staff admins do not get the server-access fieldset."""
        staff_request = self.factory.get("/")
        staff_request.user = self.staff
        superuser_request = self.factory.get("/")
        superuser_request.user = self.superuser

        staff_fields = _fieldset_fields(
            self.project_admin.get_fieldsets(staff_request, self.project)
        )
        superuser_fields = _fieldset_fields(
            self.project_admin.get_fieldsets(superuser_request, self.project)
        )

        self.assertIn("seo_title", staff_fields)
        self.assertIn("focus_keyword", staff_fields)
        for field in Project.SECRET_FIELDS:
            self.assertNotIn(field, staff_fields)
            self.assertIn(field, superuser_fields)

    def test_staff_change_page_hides_secret_values(self) -> None:
        """The HTML served to staff must not contain stored credentials."""
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("admin:projects_project_change", args=[self.project.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "super-secret-password")
        self.assertNotContains(response, "cms: admin / hunter2")
        self.assertNotContains(response, "id_server_password")
        self.assertContains(response, "redwood.studio")

    def test_superuser_change_page_shows_secret_values(self) -> None:
        """Superusers can read stored server credentials."""
        self.client.force_login(self.superuser)

        response = self.client.get(
            reverse("admin:projects_project_change", args=[self.project.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "super-secret-password")
        self.assertContains(response, "id_server_password")

    def test_staff_cannot_overwrite_secrets_via_post(self) -> None:
        """Posted secret fields are ignored when the user is not a superuser."""
        self.client.force_login(self.staff)
        payload = {
            "name": "Redwood",
            "slug": "redwood",
            "is_active": "on",
            "status": ProjectStatus.DEVELOPMENT,
            "description": "",
            "lead": "",
            "started_on": "",
            "hosting_provider": "",
            "domain": "redwood.studio",
            "staging_domain": "",
            "repository_url": "",
            "site_admin_url": "",
            "internal_notes": "",
            "new_note": "",
            "note_recipient": "",
            "server_host": "evil.example",
            "server_password": "hacked",
            "extra_credentials": "stolen",
            **_note_inline_payload(),
        }

        response = self.client.post(
            reverse("admin:projects_project_change", args=[self.project.pk]),
            payload,
        )

        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.server_host, "10.0.0.8")
        self.assertEqual(self.project.server_password, "super-secret-password")
        self.assertEqual(self.project.extra_credentials, "cms: admin / hunter2")

    def test_saving_note_creates_history(self) -> None:
        """Composing a note on save stores it on the project."""
        self.client.force_login(self.superuser)
        payload = {
            "name": "Redwood",
            "slug": "redwood",
            "is_active": "on",
            "status": ProjectStatus.DEVELOPMENT,
            "description": "",
            "lead": "",
            "started_on": "",
            "hosting_provider": "",
            "domain": "redwood.studio",
            "staging_domain": "",
            "repository_url": "",
            "site_admin_url": "",
            "internal_notes": "",
            "new_note": "Проверить деплой",
            "note_recipient": "",
            "server_host": "10.0.0.8",
            "server_port": "22",
            "server_username": "",
            "server_password": "super-secret-password",
            "server_ssh_key": "",
            "server_path": "",
            "extra_credentials": "cms: admin / hunter2",
            **_note_inline_payload(),
        }

        response = self.client.post(
            reverse("admin:projects_project_change", args=[self.project.pk]),
            payload,
        )

        self.assertEqual(response.status_code, 302)
        note = self.project.notes.get()
        self.assertEqual(note.body, "Проверить деплой")
        self.assertFalse(note.telegram_sent)
        self.assertIsNone(note.recipient)
