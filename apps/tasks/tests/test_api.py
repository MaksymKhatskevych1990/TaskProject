"""Task API tests."""

from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from apps.accounts.choices import UserRole
from apps.tasks.models import Task
from tests.base import BaseAPITestCase
from tests.factories.accounts import UserFactory


class TaskAPITests(BaseAPITestCase):
    """Verify task API endpoints."""

    @patch("apps.tasks.services.telegram_services.notify_user_about_task")
    def test_manager_can_create_task(self, mock_notify) -> None:
        """Managers can create tasks for employees."""
        manager = UserFactory(role=UserRole.MANAGER)
        assignee = UserFactory(email="assignee@example.com")
        self.authenticate(manager)
        mock_notify.return_value = True

        response = self.client.post(
            reverse("api:v1:tasks:task-list"),
            {
                "title": "Fix landing page",
                "description": "Update hero section",
                "assignee_uuid": str(assignee.uuid),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title="Fix landing page").exists())
        mock_notify.assert_called_once()

    def test_employee_sees_only_own_tasks(self) -> None:
        """Employees cannot list tasks assigned to other users."""
        employee = UserFactory(role=UserRole.EMPLOYEE, email="mine@example.com")
        other = UserFactory(email="other@example.com")
        Task.objects.create(
            title="Mine",
            assignee=employee,
            created_by=employee,
            updated_by=employee,
        )
        Task.objects.create(
            title="Other",
            assignee=other,
            created_by=other,
            updated_by=other,
        )
        self.authenticate(employee)

        response = self.client.get(reverse("api:v1:tasks:task-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data["data"]]
        self.assertEqual(titles, ["Mine"])
