"""Website API views."""

from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.responses import success_response
from apps.website import selectors, services
from apps.website.serializers import (
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    ContactLeadSerializer,
    PortfolioProjectDetailSerializer,
    PortfolioProjectListSerializer,
)


class ContactLeadView(APIView):
    """Accept contact form submissions from the public landing page."""

    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def post(self, request: Request):
        """Validate and store a contact lead."""
        serializer = ContactLeadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.submit_contact_lead(**serializer.validated_data)
        return success_response(message="Заявку отримано.")


class BlogPostListView(APIView):
    """Return published blog posts for the marketing site."""

    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """List published blog posts."""
        posts = selectors.list_published_blog_posts()
        return success_response(BlogPostListSerializer(posts, many=True).data)


class BlogPostDetailView(APIView):
    """Return a single published blog post."""

    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def get(self, request: Request, slug: str) -> Response:
        """Return one published blog post by slug."""
        post = selectors.get_published_blog_post(slug=slug)
        if post is None:
            raise NotFound("Статья не найдена.")
        return success_response(BlogPostDetailSerializer(post).data)


class PortfolioProjectListView(APIView):
    """Return published portfolio projects for the marketing site."""

    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """List published portfolio projects."""
        projects = selectors.list_published_portfolio_projects()
        serializer = PortfolioProjectListSerializer(
            projects,
            many=True,
            context={"request": request},
        )
        return success_response(serializer.data)


class PortfolioProjectDetailView(APIView):
    """Return a single published portfolio project."""

    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def get(self, request: Request, slug: str) -> Response:
        """Return one published portfolio project by slug."""
        project = selectors.get_published_portfolio_project(slug=slug)
        if project is None:
            raise NotFound("Роботу не знайдено.")
        serializer = PortfolioProjectDetailSerializer(
            project,
            context={"request": request},
        )
        return success_response(serializer.data)
