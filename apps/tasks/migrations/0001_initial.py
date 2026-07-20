"""Initial task models."""

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Create task table."""

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="создано",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="обновлено"),
                ),
                ("title", models.CharField(max_length=200, verbose_name="название")),
                ("description", models.TextField(blank=True, verbose_name="описание")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("todo", "К выполнению"),
                            ("in_progress", "В работе"),
                            ("done", "Выполнена"),
                            ("cancelled", "Отменена"),
                        ],
                        db_index=True,
                        default="todo",
                        max_length=20,
                        verbose_name="статус",
                    ),
                ),
                (
                    "due_date",
                    models.DateField(blank=True, null=True, verbose_name="срок"),
                ),
                (
                    "assignee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_tasks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="исполнитель",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="создал",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="обновил",
                    ),
                ),
            ],
            options={
                "verbose_name": "задача",
                "verbose_name_plural": "задачи",
                "ordering": ["-created_at"],
            },
        ),
    ]
