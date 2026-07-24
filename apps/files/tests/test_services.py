"""File attachment service tests."""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.exceptions import ValidationError

from apps.files import selectors, services
from apps.files.models import TaskAttachment
from apps.tasks.models import Task

User = get_user_model()


@override_settings(USE_S3=False)
class TaskAttachmentServiceTests(TestCase):
    """Verify task attachment creation and deletion."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="uploader@example.com",
            password="pass",
            first_name="Upload",
            last_name="User",
        )
        self.task = Task.objects.create(
            title="Design mockups",
            assignee=self.user,
            created_by=self.user,
            updated_by=self.user,
        )

    def test_create_task_attachment_persists_file(self) -> None:
        uploaded = SimpleUploadedFile(
            "mockup.png",
            b"fake-image-content",
            content_type="image/png",
        )

        attachment = services.create_task_attachment(
            task=self.task,
            uploaded_file=uploaded,
            actor=self.user,
        )

        self.assertEqual(TaskAttachment.objects.count(), 1)
        self.assertEqual(attachment.original_filename, "mockup.png")
        self.assertEqual(attachment.uploaded_by, self.user)
        self.assertTrue(attachment.file.name)

    def test_create_task_attachment_rejects_large_files(self) -> None:
        uploaded = SimpleUploadedFile(
            "large.bin",
            b"x" * (services.MAX_ATTACHMENT_SIZE + 1),
            content_type="application/octet-stream",
        )

        with self.assertRaises(ValidationError):
            services.create_task_attachment(
                task=self.task,
                uploaded_file=uploaded,
                actor=self.user,
            )

    def test_delete_task_attachment_removes_record(self) -> None:
        attachment = services.create_task_attachment_from_bytes(
            task=self.task,
            filename="notes.txt",
            content=b"hello",
            content_type="text/plain",
            actor=self.user,
        )

        services.delete_task_attachment(attachment=attachment, actor=self.user)

        self.assertEqual(TaskAttachment.objects.count(), 0)
        self.assertFalse(
            selectors.list_attachments_for_task(task=self.task).exists()
        )
