"""Portfolio models for the marketing site."""

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.website.models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0003_latin_slugs"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PortfolioProject",
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
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=False,
                        help_text="Заповнюється автоматично латиницею з назви.",
                        max_length=200,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                ("category", models.CharField(max_length=100, verbose_name="категория")),
                (
                    "description",
                    models.TextField(max_length=500, verbose_name="краткое описание"),
                ),
                (
                    "tags",
                    models.JSONField(blank=True, default=list, verbose_name="теги"),
                ),
                (
                    "accent",
                    models.CharField(
                        choices=[
                            ("cyan", "cyan"),
                            ("violet", "violet"),
                            ("green", "green"),
                            ("orange", "orange"),
                        ],
                        default="cyan",
                        max_length=20,
                        verbose_name="акцент",
                    ),
                ),
                (
                    "gradient",
                    models.CharField(
                        blank=True,
                        help_text="Tailwind-класи для превʼю без обкладинки, напр. from-violet/60 to-cyan/40",
                        max_length=120,
                        verbose_name="градиент",
                    ),
                ),
                (
                    "cover_image",
                    models.ImageField(
                        blank=True,
                        upload_to=apps.website.models.portfolio_cover_upload_to,
                        verbose_name="обложка",
                    ),
                ),
                (
                    "client_url",
                    models.URLField(blank=True, verbose_name="ссылка на сайт"),
                ),
                (
                    "featured",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        verbose_name="избранное",
                    ),
                ),
                (
                    "sort_order",
                    models.PositiveIntegerField(
                        db_index=True,
                        default=0,
                        verbose_name="порядок",
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
                    "metric",
                    models.CharField(blank=True, max_length=50, verbose_name="метрика"),
                ),
                (
                    "before_label",
                    models.CharField(blank=True, max_length=120, verbose_name="было"),
                ),
                (
                    "after_label",
                    models.CharField(blank=True, max_length=120, verbose_name="стало"),
                ),
                (
                    "case_description",
                    models.TextField(blank=True, max_length=2000, verbose_name="описание кейса"),
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
                "verbose_name": "работа портфолио",
                "verbose_name_plural": "работы портфолио",
                "ordering": ["sort_order", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PortfolioGalleryImage",
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
                (
                    "image",
                    models.ImageField(
                        upload_to=apps.website.models.portfolio_gallery_upload_to,
                        verbose_name="изображение",
                    ),
                ),
                (
                    "caption",
                    models.CharField(blank=True, max_length=200, verbose_name="подпись"),
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
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="website.portfolioproject",
                        verbose_name="проект",
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
                "verbose_name": "изображение галереи",
                "verbose_name_plural": "изображения галереи",
                "ordering": ["ordering", "created_at"],
            },
        ),
    ]
