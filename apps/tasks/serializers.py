"""Task serializers."""

from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.tasks.choices import TaskStatus
from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serialize task records."""

    assignee = UserSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Task
        fields = (
            "uuid",
            "title",
            "description",
            "assignee",
            "status",
            "status_display",
            "due_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class TaskCreateSerializer(serializers.Serializer):
    """Validate task creation input."""

    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    assignee_uuid = serializers.UUIDField()
    status = serializers.ChoiceField(
        choices=TaskStatus.choices,
        required=False,
        default=TaskStatus.TODO,
    )
    due_date = serializers.DateField(required=False, allow_null=True)
    notify = serializers.BooleanField(required=False, default=True)


class TaskUpdateSerializer(serializers.Serializer):
    """Validate task update input."""

    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    assignee_uuid = serializers.UUIDField(required=False)
    status = serializers.ChoiceField(choices=TaskStatus.choices, required=False)
    due_date = serializers.DateField(required=False, allow_null=True)
    notify_on_reassign = serializers.BooleanField(required=False, default=True)
