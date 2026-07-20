"""Tasks API views."""

from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.selectors import get_user_by_uuid
from apps.common.permissions import IsAuthenticated
from apps.common.responses import success_response
from apps.tasks import selectors, services
from apps.tasks.models import Task
from apps.tasks.permissions import CanManageTasks
from apps.tasks.serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
)


class TaskListCreateView(APIView):
    """List and create tasks."""

    def get_permissions(self):
        """Employees read their tasks; managers can create tasks."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageTasks()]

    def get(self, request: Request) -> Response:
        """Return tasks visible to the current user."""
        status_filter = request.query_params.get("status")
        if request.user.is_manager:
            tasks = selectors.list_tasks(status=status_filter)
        else:
            tasks = selectors.list_tasks(
                assignee=request.user,
                status=status_filter,
            )
        return success_response(TaskSerializer(tasks, many=True).data)

    def post(self, request: Request) -> Response:
        """Create a task and notify the assignee."""
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        assignee = get_user_by_uuid(validated["assignee_uuid"])
        task = services.create_task(
            title=validated["title"],
            description=validated.get("description", ""),
            assignee=assignee,
            status=validated.get("status"),
            due_date=validated.get("due_date"),
            actor=request.user,
            notify=validated.get("notify", True),
        )
        return success_response(
            TaskSerializer(task).data,
            message="Task created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class TaskDetailView(APIView):
    """Retrieve or update a single task."""

    def get_permissions(self):
        """Employees can read their tasks; managers can update them."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageTasks()]

    def get_object(self, uuid: UUID, user) -> Task:
        """Load a task the user is allowed to access."""
        task = get_object_or_404(
            Task.objects.select_related("assignee", "created_by", "updated_by"),
            uuid=uuid,
        )
        if not user.is_manager and task.assignee_id != user.id:
            raise PermissionDenied("You cannot access this task.")
        return task

    def get(self, request: Request, uuid: UUID) -> Response:
        """Return a single task."""
        task = self.get_object(uuid, request.user)
        return success_response(TaskSerializer(task).data)

    def patch(self, request: Request, uuid: UUID) -> Response:
        """Update a task."""
        task = self.get_object(uuid, request.user)
        serializer = TaskUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data.copy()
        assignee_uuid = validated.pop("assignee_uuid", None)
        notify_on_reassign = validated.pop("notify_on_reassign", True)
        data = validated
        if assignee_uuid is not None:
            data["assignee"] = get_user_by_uuid(assignee_uuid)
        updated = services.update_task(
            task=task,
            data=data,
            actor=request.user,
            notify_on_reassign=notify_on_reassign,
        )
        return success_response(TaskSerializer(updated).data)
