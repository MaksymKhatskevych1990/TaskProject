"""Factory Boy factories for account models."""

import factory

from apps.accounts.choices import UserRole
from apps.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Build users for tests."""

    class Meta:
        model = User

    email = factory.Sequence(lambda index: f"user{index}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = UserRole.EMPLOYEE
    is_active = True

    @factory.post_generation
    def password(self, create: bool, extracted: str | None, **kwargs: object) -> None:
        """Set a known password after object creation."""
        raw_password = extracted or "password123"
        self.set_password(raw_password)
        if create:
            self.save()
