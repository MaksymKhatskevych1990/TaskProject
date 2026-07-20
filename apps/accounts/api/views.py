"""Accounts API views."""

from uuid import UUID

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts import selectors, services
from apps.accounts.models import User
from apps.accounts.permissions import CanManageUsers
from apps.accounts.serializers import (
    MeUpdateSerializer,
    PasswordChangeSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.telegram.services import TELEGRAM_FIELDS
from apps.common.permissions import IsAuthenticated
from apps.common.responses import success_response


class MeView(APIView):
    """Read and update the authenticated user's profile."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Return the current user and profile."""
        user = selectors.get_user_with_profile(request.user)
        return success_response(UserSerializer(user).data)

    def patch(self, request: Request) -> Response:
        """Update the current user's profile."""
        serializer = MeUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = services.update_me(user=request.user, data=serializer.validated_data)
        return success_response(UserSerializer(user).data)


class MePasswordView(APIView):
    """Change the authenticated user's password."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Validate and apply a new password."""
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.change_password(
            user=request.user,
            current_password=serializer.validated_data["current_password"],
            new_password=serializer.validated_data["new_password"],
        )
        return success_response(message="Password updated successfully.")


class UserListCreateView(APIView):
    """List users or create a new account."""

    permission_classes = [CanManageUsers]

    def get(self, request: Request) -> Response:
        """Return users filtered by optional query parameters."""
        role = request.query_params.get("role")
        is_active_param = request.query_params.get("is_active")
        is_active = None
        if is_active_param is not None:
            is_active = is_active_param.lower() in {"1", "true", "yes"}

        users = selectors.list_users(is_active=is_active, role=role)
        return success_response(UserSerializer(users, many=True).data)

    def post(self, request: Request) -> Response:
        """Create a user account."""
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        user = services.create_user(
            email=validated["email"],
            password=validated["password"],
            first_name=validated["first_name"],
            last_name=validated["last_name"],
            role=validated["role"],
            actor=request.user,
            profile_data={
                "phone": validated.get("phone", ""),
                "position": validated.get("position", ""),
                "bio": validated.get("bio", ""),
                "timezone": validated.get("timezone", "Europe/Kyiv"),
            },
            telegram_data={
                key: validated[key]
                for key in TELEGRAM_FIELDS
                if key in validated
            },
        )
        return success_response(
            UserSerializer(user).data,
            message="User created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class UserDetailView(APIView):
    """Retrieve, update, or deactivate a user."""

    permission_classes = [CanManageUsers]

    def get_object(self, user_uuid: UUID) -> User:
        """Load the requested user."""
        return selectors.get_user_by_uuid(user_uuid)

    def get(self, request: Request, uuid: UUID) -> Response:
        """Return a single user."""
        user = self.get_object(uuid)
        return success_response(UserSerializer(user).data)

    def patch(self, request: Request, uuid: UUID) -> Response:
        """Update a user account."""
        user = self.get_object(uuid)
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = services.update_user(
            user=user,
            data=serializer.validated_data,
            actor=request.user,
        )
        return success_response(UserSerializer(updated_user).data)

    def delete(self, request: Request, uuid: UUID) -> Response:
        """Deactivate a user account."""
        user = self.get_object(uuid)
        deactivated_user = services.deactivate_user(user=user, actor=request.user)
        return success_response(UserSerializer(deactivated_user).data)
