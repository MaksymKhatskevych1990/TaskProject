"""Custom managers for account models."""

from typing import Any

from django.contrib.auth.models import BaseUserManager

from apps.accounts.choices import UserRole


class UserManager(BaseUserManager):
    """Create users and superusers with email as the login identifier."""

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """Create a standard active user."""
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        role = extra_fields.get("role", UserRole.EMPLOYEE)
        extra_fields.setdefault("is_staff", role == UserRole.ADMIN)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """Create a superuser with administrative defaults."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
