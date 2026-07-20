"""Factory Boy factories for employee models."""

from datetime import date

import factory

from apps.accounts.choices import UserRole
from apps.employees.models import Employee, Position, Team
from tests.factories.accounts import UserFactory


class PositionFactory(factory.django.DjangoModelFactory):
    """Build positions for tests."""

    class Meta:
        model = Position

    title = factory.Sequence(lambda index: f"Position {index}")
    is_active = True


class TeamFactory(factory.django.DjangoModelFactory):
    """Build teams for tests."""

    class Meta:
        model = Team

    name = factory.Sequence(lambda index: f"Team {index}")
    description = ""
    is_active = True


class EmployeeFactory(factory.django.DjangoModelFactory):
    """Build employees for tests."""

    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory, role=UserRole.EMPLOYEE)
    team = factory.SubFactory(TeamFactory)
    position = factory.SubFactory(PositionFactory)
    hire_date = date(2024, 1, 15)
    notes = ""
