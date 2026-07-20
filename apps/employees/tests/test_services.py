"""Employee service tests."""

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.accounts.choices import UserRole
from apps.employees import services
from tests.factories.accounts import UserFactory
from tests.factories.employees import EmployeeFactory, PositionFactory, TeamFactory


class EmployeeServiceTests(TestCase):
    """Verify employee write operations."""

    def test_create_employee_for_existing_user(self) -> None:
        """Managers can attach an employee record to an existing user."""
        manager = UserFactory(role=UserRole.MANAGER)
        user = UserFactory(email="member@example.com")
        team = TeamFactory()
        position = PositionFactory(title="Designer")

        employee = services.create_employee(
            actor=manager,
            user_uuid=user.uuid,
            team=team,
            position=position,
        )

        user.refresh_from_db()
        self.assertEqual(employee.user, user)
        self.assertEqual(employee.team, team)
        self.assertEqual(employee.position, position)
        self.assertEqual(user.profile.position, "Designer")

    def test_create_employee_creates_user_when_needed(self) -> None:
        """Managers can create a user and employee together."""
        manager = UserFactory(role=UserRole.MANAGER)

        employee = services.create_employee(
            actor=manager,
            email="new.hire@example.com",
            password="StrongPass123!",
            first_name="New",
            last_name="Hire",
            role=UserRole.EMPLOYEE,
        )

        self.assertEqual(employee.user.email, "new.hire@example.com")
        self.assertTrue(employee.user.check_password("StrongPass123!"))

    def test_create_employee_rejects_duplicate_user(self) -> None:
        """A user may have only one employee record."""
        manager = UserFactory(role=UserRole.MANAGER)
        existing = EmployeeFactory()

        with self.assertRaises(ValidationError):
            services.create_employee(actor=manager, user_uuid=existing.user.uuid)

    def test_deactivate_employee_deactivates_user(self) -> None:
        """Deactivating an employee also deactivates the linked user."""
        manager = UserFactory(role=UserRole.MANAGER)
        employee = EmployeeFactory()

        services.deactivate_employee(employee=employee, actor=manager)

        employee.refresh_from_db()
        self.assertFalse(employee.user.is_active)
        self.assertIsNone(employee.team)
