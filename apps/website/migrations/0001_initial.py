# Generated manually for website blog models

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
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
                ("name", models.CharField(max_length=100, verbose_name="название")),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        max_length=100,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "ordering",
                    models.PositiveIntegerField(
                        db_index=True,
                        default=0,
                        verbose_name="порядок",
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
                "verbose_name": "категория блога",
                "verbose_name_plural": "категории блога",
                "ordering": ["ordering", "name"],
            },
        ),
        migrations.CreateModel(
            name="ContactLead",
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
                ("name", models.CharField(max_length=120, verbose_name="имя")),
                ("phone", models.CharField(max_length=120, verbose_name="контакт")),
                (
                    "project",
                    models.TextField(max_length=2000, verbose_name="описание проекта"),
                ),
                (
                    "plan",
                    models.CharField(blank=True, max_length=50, verbose_name="тариф"),
                ),
                (
                    "is_processed",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        verbose_name="обработана",
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
                "verbose_name": "заявка с сайта",
                "verbose_name_plural": "заявки с сайта",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="BlogPost",
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
                ("title", models.CharField(max_length=300, verbose_name="заголовок")),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        max_length=200,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "excerpt",
                    models.TextField(max_length=500, verbose_name="краткое описание"),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Абзацы разделяйте пустой строкой. Заголовки секций начинайте с «## ».",
                        verbose_name="содержание",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "черновик"),
                            ("published", "опубликовано"),
                        ],
                        db_index=True,
                        default="draft",
                        max_length=20,
                        verbose_name="статус",
                    ),
                ),
                (
                    "published_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="дата публикации",
                    ),
                ),
                (
                    "read_time_minutes",
                    models.PositiveSmallIntegerField(
                        default=5,
                        verbose_name="время чтения (мин)",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="posts",
                        to="website.blogcategory",
                        verbose_name="категория",
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
                "verbose_name": "статья блога",
                "verbose_name_plural": "статьи блога",
                "ordering": ["-published_at", "-created_at"],
            },
        ),
    ]
