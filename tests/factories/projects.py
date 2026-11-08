"""Factory Boy factories for project models."""

import factory

from apps.projects.choices import ProjectStatus
from apps.projects.models import Project, ProjectNote
from tests.factories.accounts import UserFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    """Build studio projects for tests."""

    class Meta:
        model = Project

    name = factory.Sequence(lambda index: f"Project {index}")
    slug = factory.Sequence(lambda index: f"project-{index}")
    is_active = True
    status = ProjectStatus.DEVELOPMENT


class ProjectNoteFactory(factory.django.DjangoModelFactory):
    """Build project notes for tests."""

    class Meta:
        model = ProjectNote

    project = factory.SubFactory(ProjectFactory)
    body = factory.Faker("sentence")
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SelfAttribute("created_by")
