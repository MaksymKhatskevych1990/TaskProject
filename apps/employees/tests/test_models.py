"""Employee model tests."""

from django.test import TestCase

from apps.employees.models import Employee
from tests.factories.employees import EmployeeFactory, PositionFactory, TeamFactory


class EmployeeModelTests(TestCase):
    """Verify employee model relationships."""

    def test_employee_links_user_team_and_position(self) -> None:
        """An employee stores organizational relationships."""
        team = TeamFactory(name="Backend")
        position = PositionFactory(title="Developer")
        employee = EmployeeFactory(team=team, position=position)

        self.assertEqual(employee.team, team)
        self.assertEqual(employee.position, position)
        self.assertTrue(Employee.objects.filter(user=employee.user).exists())
