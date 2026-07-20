"""Employee business operations."""

import logging
from datetime import date
from typing import Any
from uuid import UUID

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.accounts import services as account_services
from apps.accounts.choices import UserRole
from apps.accounts.models import User
from apps.accounts.selectors import get_user_by_uuid
from apps.employees import selectors
from apps.employees.models import Employee, Position, Team

logger = logging.getLogger(__name__)


def _sync_profile_position(*, user: User, position: Position | None) -> None:
    """Keep Profile.position text aligned with the catalog title."""
    profile = user.profile
    profile.position = position.title if position is not None else ""
    profile.save(update_fields=["position", "updated_at"])


def create_position(
    *,
    title: str,
    is_active: bool = True,
    actor: User,
) -> Position:
    """Create a job title catalog entry."""
    if Position.objects.filter(title__iexact=title).exists():
        raise ValidationError({"title": ["A position with this title already exists."]})

    position = Position.objects.create(
        title=title.strip(),
        is_active=is_active,
        created_by=actor,
        updated_by=actor,
    )
    logger.info("Created position", extra={"position_uuid": str(position.uuid)})
    return position


def update_position(
    *,
    position: Position,
    data: dict[str, Any],
    actor: User,
) -> Position:
    """Update a catalog position."""
    if "title" in data:
        title = data["title"].strip()
        conflict = Position.objects.filter(title__iexact=title).exclude(pk=position.pk)
        if conflict.exists():
            raise ValidationError(
                {"title": ["A position with this title already exists."]}
            )
        position.title = title
    if "is_active" in data:
        position.is_active = data["is_active"]
    position.updated_by = actor
    position.save()

    if "title" in data:
        for employee in Employee.objects.filter(position=position).select_related(
            "user__profile"
        ):
            _sync_profile_position(user=employee.user, position=position)

    logger.info("Updated position", extra={"position_uuid": str(position.uuid)})
    return position


def deactivate_position(*, position: Position, actor: User) -> Position:
    """Deactivate a position without deleting historical assignments."""
    position.is_active = False
    position.updated_by = actor
    position.save(update_fields=["is_active", "updated_by", "updated_at"])
    logger.info("Deactivated position", extra={"position_uuid": str(position.uuid)})
    return position


def create_team(
    *,
    name: str,
    description: str = "",
    lead: User | None = None,
    is_active: bool = True,
    actor: User,
) -> Team:
    """Create a studio team."""
    if Team.objects.filter(name__iexact=name).exists():
        raise ValidationError({"name": ["A team with this name already exists."]})

    team = Team.objects.create(
        name=name.strip(),
        description=description,
        lead=lead,
        is_active=is_active,
        created_by=actor,
        updated_by=actor,
    )
    logger.info("Created team", extra={"team_uuid": str(team.uuid)})
    return team


def update_team(*, team: Team, data: dict[str, Any], actor: User) -> Team:
    """Update team attributes."""
    if "name" in data:
        name = data["name"].strip()
        conflict = Team.objects.filter(name__iexact=name).exclude(pk=team.pk)
        if conflict.exists():
            raise ValidationError({"name": ["A team with this name already exists."]})
        team.name = name
    if "description" in data:
        team.description = data["description"]
    if "lead" in data:
        team.lead = data["lead"]
    if "is_active" in data:
        team.is_active = data["is_active"]
    team.updated_by = actor
    team.save()
    logger.info("Updated team", extra={"team_uuid": str(team.uuid)})
    return selectors.get_team_by_uuid(team.uuid)


def deactivate_team(*, team: Team, actor: User) -> Team:
    """Deactivate a team and clear member assignments."""
    with transaction.atomic():
        team.is_active = False
        team.updated_by = actor
        team.save(update_fields=["is_active", "updated_by", "updated_at"])
        Employee.objects.filter(team=team).update(team=None)
    logger.info("Deactivated team", extra={"team_uuid": str(team.uuid)})
    return selectors.get_team_by_uuid(team.uuid)


def create_employee(
    *,
    actor: User,
    user_uuid: UUID | None = None,
    email: str | None = None,
    password: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    role: str = UserRole.EMPLOYEE,
    team: Team | None = None,
    position: Position | None = None,
    hire_date: date | None = None,
    notes: str = "",
) -> Employee:
    """Create an employee for an existing or newly created user."""
    with transaction.atomic():
        if user_uuid is not None:
            user = get_user_by_uuid(user_uuid)
            if selectors.get_employee_for_user(user.pk) is not None:
                raise ValidationError(
                    {"user_uuid": ["This user already has an employee record."]}
                )
        else:
            if not email or not password or not first_name or not last_name:
                raise ValidationError(
                    {
                        "detail": [
                            "Provide user_uuid or email, password, first_name, "
                            "and last_name."
                        ]
                    }
                )
            user = account_services.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                actor=actor,
            )

        employee = Employee.objects.create(
            user=user,
            team=team,
            position=position,
            hire_date=hire_date,
            notes=notes,
            created_by=actor,
            updated_by=actor,
        )
        _sync_profile_position(user=user, position=position)

    logger.info("Created employee", extra={"employee_uuid": str(employee.uuid)})
    return selectors.get_employee_by_uuid(employee.uuid)


def update_employee(
    *,
    employee: Employee,
    data: dict[str, Any],
    actor: User,
) -> Employee:
    """Update employee organizational fields."""
    with transaction.atomic():
        if "team" in data:
            employee.team = data["team"]
        if "position" in data:
            employee.position = data["position"]
            _sync_profile_position(user=employee.user, position=data["position"])
        if "hire_date" in data:
            employee.hire_date = data["hire_date"]
        if "notes" in data:
            employee.notes = data["notes"]
        employee.updated_by = actor
        employee.save()

    logger.info("Updated employee", extra={"employee_uuid": str(employee.uuid)})
    return selectors.get_employee_by_uuid(employee.uuid)


def deactivate_employee(*, employee: Employee, actor: User) -> Employee:
    """Deactivate the linked user account without deleting history."""
    if employee.user_id == actor.pk:
        raise ValidationError({"detail": ["You cannot deactivate your own account."]})

    with transaction.atomic():
        employee.user.is_active = False
        employee.user.save(update_fields=["is_active"])
        employee.team = None
        employee.updated_by = actor
        employee.save(update_fields=["team", "updated_by", "updated_at"])

    logger.info(
        "Deactivated employee",
        extra={
            "employee_uuid": str(employee.uuid),
            "actor_uuid": str(actor.uuid),
        },
    )
    return selectors.get_employee_by_uuid(employee.uuid)
