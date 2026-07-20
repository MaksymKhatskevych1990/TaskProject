"""Factory Boy factories for Telegram models."""

import factory

from apps.telegram.models import TelegramAccount
from tests.factories.accounts import UserFactory


class TelegramAccountFactory(factory.django.DjangoModelFactory):
    """Build Telegram accounts for tests."""

    class Meta:
        model = TelegramAccount
        django_get_or_create = ("user",)

    user = factory.SubFactory(UserFactory)
    username = factory.Sequence(lambda index: f"user{index}")
    chat_id = factory.Sequence(lambda index: 1_000_000 + index)
    notifications_enabled = True
