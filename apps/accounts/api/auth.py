"""Authentication API views."""

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView

from apps.accounts.serializers import CustomTokenObtainPairSerializer
from apps.accounts.services import logout_user
from apps.common.permissions import IsAuthenticated
from apps.common.responses import success_response


class TokenObtainPairView(BaseTokenObtainPairView):
    """Obtain access and refresh tokens for a valid user."""

    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class TokenRefreshView(BaseTokenRefreshView):
    """Refresh an access token."""

    permission_classes = [AllowAny]


class LogoutView(APIView):
    """Blacklist the submitted refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Invalidate the refresh token supplied by the client."""
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"refresh": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logout_user(refresh_token=refresh_token)
        return success_response(message="Logged out successfully.")
