"""Project read operations."""

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, QuerySet

from apps.projects.models import Project

User = get_user_model()


def list_projects_for_assignee(*, assignee: User) -> QuerySet[Project]:
    """Return active projects that contain tasks assigned to the user."""
    return (
        Project.objects.filter(is_active=True, tasks__assignee=assignee)
        .annotate(task_count=Count("tasks", filter=Q(tasks__assignee=assignee)))
        .order_by("slug")
        .distinct()
    )


def get_project_by_uuid(*, project_uuid) -> Project:
    """Return a single project by UUID."""
    return Project.objects.get(uuid=project_uuid)


def assignee_has_unassigned_tasks(*, assignee: User) -> bool:
    """Return whether the user has tasks without a project."""
    from apps.tasks.models import Task

    return Task.objects.filter(assignee=assignee, project__isnull=True).exists()


def count_unassigned_tasks(*, assignee: User) -> int:
    """Return how many tasks the user has without a project."""
    from apps.tasks.models import Task

    return Task.objects.filter(assignee=assignee, project__isnull=True).count()
