"""Factory Boy factories for task models."""

import factory

from apps.tasks.models import Task
from tests.factories.accounts import UserFactory


class TaskFactory(factory.django.DjangoModelFactory):
    """Build tasks for tests."""

    class Meta:
        model = Task

    title = factory.Sequence(lambda index: f"Task {index}")
    description = factory.Faker("sentence")
    assignee = factory.SubFactory(UserFactory)
    created_by = factory.SelfAttribute("assignee")
    updated_by = factory.SelfAttribute("assignee")
