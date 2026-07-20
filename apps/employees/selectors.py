"""Read-only employee queries."""

from uuid import UUID

from django.db.models import QuerySet

from apps.employees.models import Employee, Position, Team


def get_employee_by_uuid(employee_uuid: UUID) -> Employee:
    """Return an employee with related identity and org data."""
    return Employee.objects.select_related(
        "user",
        "user__profile",
        "team",
        "position",
    ).get(uuid=employee_uuid)


def get_employee_for_user(user_id: int) -> Employee | None:
    """Return the employee record for a user when it exists."""
    return (
        Employee.objects.select_related("user", "user__profile", "team", "position")
        .filter(user_id=user_id)
        .first()
    )


def list_employees(
    *,
    team_uuid: UUID | None = None,
    position_uuid: UUID | None = None,
    is_active: bool | None = None,
) -> QuerySet[Employee]:
    """Return employees filtered by optional org attributes."""
    queryset = Employee.objects.select_related(
        "user",
        "user__profile",
        "team",
        "position",
    )
    if team_uuid is not None:
        queryset = queryset.filter(team__uuid=team_uuid)
    if position_uuid is not None:
        queryset = queryset.filter(position__uuid=position_uuid)
    if is_active is not None:
        queryset = queryset.filter(user__is_active=is_active)
    return queryset


def get_team_by_uuid(team_uuid: UUID) -> Team:
    """Return a team with its lead preloaded."""
    return Team.objects.select_related("lead").get(uuid=team_uuid)


def list_teams(*, is_active: bool | None = None) -> QuerySet[Team]:
    """Return teams ordered by name."""
    queryset = Team.objects.select_related("lead")
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    return queryset


def get_position_by_uuid(position_uuid: UUID) -> Position:
    """Return a position by public identifier."""
    return Position.objects.get(uuid=position_uuid)


def list_positions(*, is_active: bool | None = None) -> QuerySet[Position]:
    """Return positions ordered by title."""
    queryset = Position.objects.all()
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    return queryset
