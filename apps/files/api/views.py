"""Task attachment API views."""

from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAuthenticated
from apps.common.responses import success_response
from apps.files import selectors, services
from apps.files.models import TaskAttachment
from apps.files.serializers import TaskAttachmentSerializer
from apps.tasks.models import Task
from apps.tasks.permissions import CanManageTasks


class TaskAttachmentListCreateView(APIView):
    """List or upload attachments for a task."""

    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        """Employees read their task attachments; managers can upload."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [CanManageTasks()]

    def _get_task(self, uuid: UUID, user) -> Task:
        task = get_object_or_404(Task.objects.select_related("assignee"), uuid=uuid)
        if not user.is_manager and task.assignee_id != user.id:
            raise PermissionDenied("You cannot access this task.")
        return task

    def get(self, request: Request, uuid: UUID) -> Response:
        """Return attachments for a task."""
        task = self._get_task(uuid, request.user)
        attachments = selectors.list_attachments_for_task(task=task)
        return success_response(
            TaskAttachmentSerializer(
                attachments,
                many=True,
                context={"request": request},
            ).data
        )

    def post(self, request: Request, uuid: UUID) -> Response:
        """Upload a file attachment to a task."""
        task = self._get_task(uuid, request.user)
        uploaded_file = request.FILES.get("file")
        if uploaded_file is None:
            return Response(
                {"success": False, "message": "File is required.", "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )
        attachment = services.create_task_attachment(
            task=task,
            uploaded_file=uploaded_file,
            actor=request.user,
        )
        return success_response(
            TaskAttachmentSerializer(attachment, context={"request": request}).data,
            message="Attachment uploaded successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class TaskAttachmentDetailView(APIView):
    """Delete a task attachment."""

    permission_classes = [CanManageTasks]

    def delete(self, request: Request, uuid: UUID, attachment_uuid: UUID) -> Response:
        """Remove an attachment from a task."""
        task = get_object_or_404(Task, uuid=uuid)
        attachment = get_object_or_404(
            TaskAttachment.objects.filter(task=task),
            uuid=attachment_uuid,
        )
        services.delete_task_attachment(attachment=attachment, actor=request.user)
        return success_response(None, message="Attachment deleted successfully.")
