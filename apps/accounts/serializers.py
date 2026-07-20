"""Account serializers."""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.choices import UserRole
from apps.accounts.models import Profile, User
from apps.telegram.models import TelegramAccount


class TelegramAccountSerializer(serializers.ModelSerializer):
    """Serialize Telegram contact fields."""

    class Meta:
        model = TelegramAccount
        fields = (
            "username",
            "chat_id",
            "notifications_enabled",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize profile fields."""

    class Meta:
        model = Profile
        fields = (
            "phone",
            "position",
            "bio",
            "timezone",
            "avatar",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class UserSerializer(serializers.ModelSerializer):
    """Serialize core user fields."""

    profile = ProfileSerializer(read_only=True)
    telegram_account = serializers.SerializerMethodField()
    full_name = serializers.CharField(read_only=True)

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
            "date_joined",
            "last_login",
            "profile",
            "telegram_account",
        )
        read_only_fields = fields

    def get_telegram_account(self, obj: User) -> dict | None:
        """Return Telegram data when a linked account exists."""
        account = getattr(obj, "telegram_account", None)
        if account is None:
            return None
        return TelegramAccountSerializer(account).data


class UserCreateSerializer(serializers.Serializer):
    """Validate user creation input."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    role = serializers.ChoiceField(choices=UserRole.choices, default=UserRole.EMPLOYEE)
    phone = serializers.CharField(max_length=32, required=False, allow_blank=True)
    position = serializers.CharField(max_length=120, required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    timezone = serializers.CharField(
        max_length=64, required=False, default="Europe/Kyiv"
    )
    telegram_username = serializers.CharField(
        max_length=64, required=False, allow_blank=True
    )
    telegram_chat_id = serializers.IntegerField(required=False, allow_null=True)
    telegram_notifications_enabled = serializers.BooleanField(required=False, default=True)

    def validate_password(self, value: str) -> str:
        """Apply Django password validators."""
        validate_password(value)
        return value


class UserUpdateSerializer(serializers.Serializer):
    """Validate administrative user updates."""

    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(choices=UserRole.choices, required=False)
    is_active = serializers.BooleanField(required=False)
    phone = serializers.CharField(max_length=32, required=False, allow_blank=True)
    position = serializers.CharField(max_length=120, required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    timezone = serializers.CharField(max_length=64, required=False)
    avatar = serializers.ImageField(required=False, allow_null=True)
    telegram_username = serializers.CharField(
        max_length=64, required=False, allow_blank=True
    )
    telegram_chat_id = serializers.IntegerField(required=False, allow_null=True)
    telegram_notifications_enabled = serializers.BooleanField(required=False)


class MeUpdateSerializer(serializers.Serializer):
    """Validate self-service profile updates."""

    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    phone = serializers.CharField(max_length=32, required=False, allow_blank=True)
    position = serializers.CharField(max_length=120, required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    timezone = serializers.CharField(max_length=64, required=False)
    avatar = serializers.ImageField(required=False, allow_null=True)


class PasswordChangeSerializer(serializers.Serializer):
    """Validate password change requests."""

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value: str) -> str:
        """Apply Django password validators."""
        validate_password(value)
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Return tokens together with the authenticated user payload."""

    @classmethod
    def get_token(cls, user: User):
        """Attach role claims to the JWT."""
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        return token

    def validate(self, attrs: dict) -> dict:
        """Add serialized user data to the token response."""
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data
