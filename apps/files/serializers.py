"""File attachment serializers."""

from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.files.models import TaskAttachment


class TaskAttachmentSerializer(serializers.ModelSerializer):
    """Serialize task attachment records."""

    uploaded_by = UserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = TaskAttachment
        fields = (
            "uuid",
            "original_filename",
            "content_type",
            "file_size",
            "uploaded_by",
            "file_url",
            "created_at",
        )
        read_only_fields = fields

    def get_file_url(self, obj: TaskAttachment) -> str | None:
        """Return a URL for downloading the attachment when available."""
        if not obj.file:
            return None
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url
