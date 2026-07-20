"""Employees API views."""

from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAuthenticated
from apps.common.responses import success_response
from apps.employees import selectors, services
from apps.employees.models import Employee, Position, Team
from apps.employees.permissions import CanManageOrganization
from apps.employees.serializers import (
    EmployeeCreateSerializer,
    EmployeeSerializer,
    EmployeeUpdateSerializer,
    PositionSerializer,
    PositionWriteSerializer,
    TeamSerializer,
    TeamWriteSerializer,
)


def _parse_bool(value: str | None) -> bool | None:
    """Parse an optional boolean query parameter."""
    if value is None:
        return None
    return value.lower() in {"1", "true", "yes"}


def _parse_uuid(value: str | None) -> UUID | None:
    """Parse an optional UUID query parameter."""
    if not value:
        return None
    try:
        return UUID(value)
    except ValueError as exc:
        raise ValidationError({"detail": ["Invalid UUID filter value."]}) from exc


class PositionListCreateView(APIView):
    """List and create job titles."""

    def get_permissions(self):
        """Allow reads for authenticated users and writes for managers."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageOrganization()]

    def get(self, request: Request) -> Response:
        """Return the position catalog."""
        positions = selectors.list_positions(
            is_active=_parse_bool(request.query_params.get("is_active"))
        )
        return success_response(PositionSerializer(positions, many=True).data)

    def post(self, request: Request) -> Response:
        """Create a position."""
        serializer = PositionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        position = services.create_position(
            title=serializer.validated_data["title"],
            is_active=serializer.validated_data.get("is_active", True),
            actor=request.user,
        )
        return success_response(
            PositionSerializer(position).data,
            message="Position created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class PositionDetailView(APIView):
    """Retrieve, update, or deactivate a position."""

    def get_permissions(self):
        """Allow reads for authenticated users and writes for managers."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageOrganization()]

    def get_object(self, uuid: UUID) -> Position:
        """Load the requested position."""
        return get_object_or_404(Position, uuid=uuid)

    def get(self, request: Request, uuid: UUID) -> Response:
        """Return a single position."""
        position = self.get_object(uuid)
        return success_response(PositionSerializer(position).data)

    def patch(self, request: Request, uuid: UUID) -> Response:
        """Update a position."""
        position = self.get_object(uuid)
        serializer = PositionWriteSerializer(position, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = services.update_position(
            position=position,
            data=serializer.validated_data,
            actor=request.user,
        )
        return success_response(PositionSerializer(updated).data)

    def delete(self, request: Request, uuid: UUID) -> Response:
        """Deactivate a position."""
        position = self.get_object(uuid)
        deactivated = services.deactivate_position(
            position=position,
            actor=request.user,
        )
        return success_response(PositionSerializer(deactivated).data)


class TeamListCreateView(APIView):
    """List and create teams."""

    def get_permissions(self):
        """Allow reads for authenticated users and writes for managers."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageOrganization()]

    def get(self, request: Request) -> Response:
        """Return teams."""
        teams = selectors.list_teams(
            is_active=_parse_bool(request.query_params.get("is_active"))
        )
        return success_response(TeamSerializer(teams, many=True).data)

    def post(self, request: Request) -> Response:
        """Create a team."""
        serializer = TeamWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        team = services.create_team(
            name=validated["name"],
            description=validated.get("description", ""),
            lead=validated.get("lead"),
            is_active=validated.get("is_active", True),
            actor=request.user,
        )
        return success_response(
            TeamSerializer(team).data,
            message="Team created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class TeamDetailView(APIView):
    """Retrieve, update, or deactivate a team."""

    def get_permissions(self):
        """Allow reads for authenticated users and writes for managers."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageOrganization()]

    def get_object(self, uuid: UUID) -> Team:
        """Load the requested team."""
        return get_object_or_404(Team.objects.select_related("lead"), uuid=uuid)

    def get(self, request: Request, uuid: UUID) -> Response:
        """Return a single team."""
        team = self.get_object(uuid)
        return success_response(TeamSerializer(team).data)

    def patch(self, request: Request, uuid: UUID) -> Response:
        """Update a team."""
        team = self.get_object(uuid)
        serializer = TeamWriteSerializer(team, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = services.update_team(
            team=team,
            data=serializer.validated_data,
            actor=request.user,
        )
        return success_response(TeamSerializer(updated).data)

    def delete(self, request: Request, uuid: UUID) -> Response:
        """Deactivate a team."""
        team = self.get_object(uuid)
        deactivated = services.deactivate_team(team=team, actor=request.user)
        return success_response(TeamSerializer(deactivated).data)


class EmployeeListCreateView(APIView):
    """List and create employees."""

    def get_permissions(self):
        """Allow reads for authenticated users and writes for managers."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageOrganization()]

    def get(self, request: Request) -> Response:
        """Return the employee directory."""
        employees = selectors.list_employees(
            team_uuid=_parse_uuid(request.query_params.get("team")),
            position_uuid=_parse_uuid(request.query_params.get("position")),
            is_active=_parse_bool(request.query_params.get("is_active")),
        )
        return success_response(EmployeeSerializer(employees, many=True).data)

    def post(self, request: Request) -> Response:
        """Create an employee record."""
        serializer = EmployeeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        employee = services.create_employee(
            actor=request.user,
            user_uuid=validated["user"].uuid if "user" in validated else None,
            email=validated.get("email"),
            password=validated.get("password"),
            first_name=validated.get("first_name"),
            last_name=validated.get("last_name"),
            role=validated.get("role", "employee"),
            team=validated.get("team"),
            position=validated.get("position"),
            hire_date=validated.get("hire_date"),
            notes=validated.get("notes", ""),
        )
        return success_response(
            EmployeeSerializer(employee).data,
            message="Employee created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class EmployeeDetailView(APIView):
    """Retrieve, update, or deactivate an employee."""

    def get_permissions(self):
        """Allow reads for authenticated users and writes for managers."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageOrganization()]

    def get_object(self, uuid: UUID) -> Employee:
        """Load the requested employee."""
        return get_object_or_404(
            Employee.objects.select_related(
                "user",
                "user__profile",
                "team",
                "position",
            ),
            uuid=uuid,
        )

    def get(self, request: Request, uuid: UUID) -> Response:
        """Return a single employee."""
        employee = self.get_object(uuid)
        return success_response(EmployeeSerializer(employee).data)

    def patch(self, request: Request, uuid: UUID) -> Response:
        """Update an employee."""
        employee = self.get_object(uuid)
        serializer = EmployeeUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = services.update_employee(
            employee=employee,
            data=serializer.validated_data,
            actor=request.user,
        )
        return success_response(EmployeeSerializer(updated).data)

    def delete(self, request: Request, uuid: UUID) -> Response:
        """Deactivate an employee."""
        employee = self.get_object(uuid)
        deactivated = services.deactivate_employee(
            employee=employee,
            actor=request.user,
        )
        return success_response(EmployeeSerializer(deactivated).data)
