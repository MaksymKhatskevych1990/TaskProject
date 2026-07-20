"""Employees API tests."""

from django.urls import reverse
from rest_framework import status

from apps.accounts.choices import UserRole
from apps.employees.models import Employee, Position, Team
from tests.base import BaseAPITestCase
from tests.factories.accounts import UserFactory
from tests.factories.employees import EmployeeFactory, TeamFactory


class EmployeesAPITests(BaseAPITestCase):
    """Verify organization directory endpoints."""

    def test_manager_can_create_position_team_and_employee(self) -> None:
        """Managers can build the organizational catalog and directory."""
        manager = UserFactory(role=UserRole.MANAGER)
        self.authenticate(manager)

        position_response = self.client.post(
            reverse("api:v1:employees:position-list"),
            {"title": "Backend Engineer"},
            format="json",
        )
        team_response = self.client.post(
            reverse("api:v1:employees:team-list"),
            {"name": "Platform", "lead_uuid": str(manager.uuid)},
            format="json",
        )
        employee_response = self.client.post(
            reverse("api:v1:employees:employee-list"),
            {
                "email": "hire@example.com",
                "password": "StrongPass123!",
                "first_name": "Hire",
                "last_name": "Person",
                "team_uuid": team_response.data["data"]["uuid"],
                "position_uuid": position_response.data["data"]["uuid"],
            },
            format="json",
        )

        self.assertEqual(position_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(team_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(employee_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Position.objects.filter(title="Backend Engineer").exists())
        self.assertTrue(Team.objects.filter(name="Platform").exists())
        self.assertTrue(
            Employee.objects.filter(user__email="hire@example.com").exists()
        )

    def test_authenticated_user_can_list_employees(self) -> None:
        """Any authenticated user can read the employee directory."""
        EmployeeFactory()
        user = UserFactory()
        self.authenticate(user)

        response = self.client.get(reverse("api:v1:employees:employee-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(len(response.data["data"]), 1)

    def test_employee_cannot_create_team(self) -> None:
        """Regular employees cannot mutate organizational structure."""
        employee_user = UserFactory(role=UserRole.EMPLOYEE)
        self.authenticate(employee_user)

        response = self.client.post(
            reverse("api:v1:employees:team-list"),
            {"name": "Forbidden"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_can_update_and_deactivate_employee(self) -> None:
        """Managers can reassign and deactivate employees."""
        manager = UserFactory(role=UserRole.MANAGER)
        employee = EmployeeFactory()
        new_team = TeamFactory(name="Design")
        self.authenticate(manager)

        update_response = self.client.patch(
            reverse(
                "api:v1:employees:employee-detail",
                kwargs={"uuid": employee.uuid},
            ),
            {"team_uuid": str(new_team.uuid)},
            format="json",
        )
        delete_response = self.client.delete(
            reverse(
                "api:v1:employees:employee-detail",
                kwargs={"uuid": employee.uuid},
            )
        )

        employee.refresh_from_db()
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(employee.user.is_active)
        self.assertIsNone(employee.team)
