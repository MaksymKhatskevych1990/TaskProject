"""Read-only queries for website content."""

from __future__ import annotations

from django.db.models import QuerySet

from apps.website.choices import BlogPostStatus
from apps.website.models import BlogPost, PortfolioProject


def list_published_blog_posts() -> QuerySet[BlogPost]:
    """Return published blog posts ordered for the public listing."""
    return (
        BlogPost.objects.filter(
            status=BlogPostStatus.PUBLISHED,
            published_at__isnull=False,
        )
        .select_related("category")
        .order_by("-published_at")
    )


def get_published_blog_post(*, slug: str) -> BlogPost | None:
    """Return a published blog post by slug."""
    return (
        BlogPost.objects.filter(
            slug=slug,
            status=BlogPostStatus.PUBLISHED,
            published_at__isnull=False,
        )
        .select_related("category")
        .first()
    )


def list_published_portfolio_projects() -> QuerySet[PortfolioProject]:
    """Return published portfolio projects ordered for the public listing."""
    return PortfolioProject.objects.filter(status=BlogPostStatus.PUBLISHED).order_by(
        "sort_order",
        "-created_at",
    )


def get_published_portfolio_project(*, slug: str) -> PortfolioProject | None:
    """Return a published portfolio project by slug."""
    return (
        PortfolioProject.objects.filter(
            slug=slug,
            status=BlogPostStatus.PUBLISHED,
        )
        .prefetch_related("gallery_images")
        .first()
    )
