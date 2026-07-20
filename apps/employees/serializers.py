"""Employee serializers."""

from rest_framework import serializers

from apps.accounts.choices import UserRole
from apps.accounts.models import User
from apps.accounts.selectors import get_user_by_uuid
from apps.employees import selectors
from apps.employees.models import Employee, Position, Team


class PositionSerializer(serializers.ModelSerializer):
    """Serialize position catalog entries."""

    class Meta:
        model = Position
        fields = ("uuid", "title", "is_active", "created_at", "updated_at")
        read_only_fields = fields


class PositionWriteSerializer(serializers.Serializer):
    """Validate position create and update payloads."""

    title = serializers.CharField(max_length=120, required=False)
    is_active = serializers.BooleanField(required=False)

    def validate(self, attrs: dict) -> dict:
        """Require a title when creating a position."""
        if self.instance is None and "title" not in attrs:
            raise serializers.ValidationError({"title": ["This field is required."]})
        return attrs


class TeamLeadSerializer(serializers.ModelSerializer):
    """Serialize a compact team lead payload."""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("uuid", "email", "first_name", "last_name", "full_name")
        read_only_fields = fields


class TeamSerializer(serializers.ModelSerializer):
    """Serialize teams."""

    lead = TeamLeadSerializer(read_only=True)

    class Meta:
        model = Team
        fields = (
            "uuid",
            "name",
            "description",
            "lead",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class TeamWriteSerializer(serializers.Serializer):
    """Validate team create and update payloads."""

    name = serializers.CharField(max_length=120, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    lead_uuid = serializers.UUIDField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)

    def validate(self, attrs: dict) -> dict:
        """Require a name when creating a team and resolve the lead."""
        if self.instance is None and "name" not in attrs:
            raise serializers.ValidationError({"name": ["This field is required."]})

        if "lead_uuid" in attrs:
            lead_uuid = attrs.pop("lead_uuid")
            if lead_uuid is None:
                attrs["lead"] = None
            else:
                try:
                    attrs["lead"] = get_user_by_uuid(lead_uuid)
                except User.DoesNotExist as exc:
                    raise serializers.ValidationError(
                        {"lead_uuid": ["User not found."]}
                    ) from exc
        return attrs


class EmployeeUserSerializer(serializers.ModelSerializer):
    """Serialize the identity fields of an employee."""

    full_name = serializers.CharField(read_only=True)
    phone = serializers.CharField(source="profile.phone", read_only=True)

    class Meta:
        model = User
        fields = (
            "uuid",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "is_active",
            "phone",
        )
        read_only_fields = fields


class EmployeeSerializer(serializers.ModelSerializer):
    """Serialize employee directory records."""

    user = EmployeeUserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = (
            "uuid",
            "user",
            "team",
            "position",
            "hire_date",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class EmployeeCreateSerializer(serializers.Serializer):
    """Validate employee creation for an existing or new user."""

    user_uuid = serializers.UUIDField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, min_length=8, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE,
        required=False,
    )
    team_uuid = serializers.UUIDField(required=False, allow_null=True)
    position_uuid = serializers.UUIDField(required=False, allow_null=True)
    hire_date = serializers.DateField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, default="")

    def validate(self, attrs: dict) -> dict:
        """Require either an existing user or a complete new-user payload."""
        if "user_uuid" in attrs:
            user_uuid = attrs.pop("user_uuid")
            try:
                attrs["user"] = get_user_by_uuid(user_uuid)
            except User.DoesNotExist as exc:
                raise serializers.ValidationError(
                    {"user_uuid": ["User not found."]}
                ) from exc
        elif not all(
            key in attrs for key in ("email", "password", "first_name", "last_name")
        ):
            raise serializers.ValidationError(
                {
                    "detail": [
                        "Provide user_uuid or email, password, first_name, and "
                        "last_name."
                    ]
                }
            )

        if "team_uuid" in attrs:
            team_uuid = attrs.pop("team_uuid")
            if team_uuid is None:
                attrs["team"] = None
            else:
                try:
                    attrs["team"] = selectors.get_team_by_uuid(team_uuid)
                except Team.DoesNotExist as exc:
                    raise serializers.ValidationError(
                        {"team_uuid": ["Team not found."]}
                    ) from exc
        if "position_uuid" in attrs:
            position_uuid = attrs.pop("position_uuid")
            if position_uuid is None:
                attrs["position"] = None
            else:
                try:
                    attrs["position"] = selectors.get_position_by_uuid(position_uuid)
                except Position.DoesNotExist as exc:
                    raise serializers.ValidationError(
                        {"position_uuid": ["Position not found."]}
                    ) from exc
        return attrs


class EmployeeUpdateSerializer(serializers.Serializer):
    """Validate employee update payloads."""

    team_uuid = serializers.UUIDField(required=False, allow_null=True)
    position_uuid = serializers.UUIDField(required=False, allow_null=True)
    hire_date = serializers.DateField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs: dict) -> dict:
        """Resolve team and position references."""
        if "team_uuid" in attrs:
            team_uuid = attrs.pop("team_uuid")
            if team_uuid is None:
                attrs["team"] = None
            else:
                try:
                    attrs["team"] = selectors.get_team_by_uuid(team_uuid)
                except Team.DoesNotExist as exc:
                    raise serializers.ValidationError(
                        {"team_uuid": ["Team not found."]}
                    ) from exc
        if "position_uuid" in attrs:
            position_uuid = attrs.pop("position_uuid")
            if position_uuid is None:
                attrs["position"] = None
            else:
                try:
                    attrs["position"] = selectors.get_position_by_uuid(position_uuid)
                except Position.DoesNotExist as exc:
                    raise serializers.ValidationError(
                        {"position_uuid": ["Position not found."]}
                    ) from exc
        return attrs
