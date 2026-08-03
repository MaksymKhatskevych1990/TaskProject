"""Website API tests."""

from datetime import datetime, timezone as dt_timezone

from django.urls import reverse
from rest_framework import status

from apps.website.models import BlogCategory, BlogPost
from tests.base import BaseAPITestCase


class WebsiteContactAPITests(BaseAPITestCase):
    """Verify public contact form endpoint."""

    def test_contact_lead_accepts_valid_payload(self) -> None:
        """Anonymous users can submit a contact lead."""
        response = self.client.post(
            reverse("api:v1:website:contact"),
            {
                "name": "Олена П.",
                "phone": "@olena",
                "project": "Потрібен лендинг для салону краси",
                "plan": "Бізнес",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

    def test_contact_lead_rejects_missing_fields(self) -> None:
        """Required fields must be present."""
        response = self.client.post(
            reverse("api:v1:website:contact"),
            {"name": "Олена П."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WebsiteBlogAPITests(BaseAPITestCase):
    """Verify public blog endpoints."""

    def setUp(self) -> None:
        """Create sample blog posts."""
        super().setUp()
        self.category = BlogCategory.objects.create(name="SEO", slug="seo")
        self.published = BlogPost.objects.create(
            title="SEO checklist",
            slug="seo-checklist",
            excerpt="Useful SEO tips",
            content="Intro\n\n## Section\n\nDetails",
            category=self.category,
            status="published",
            published_at=datetime(2026, 7, 15, tzinfo=dt_timezone.utc),
            read_time_minutes=7,
        )
        BlogPost.objects.create(
            title="Draft article",
            slug="draft-article",
            excerpt="Hidden",
            content="Draft",
            category=self.category,
            status="draft",
        )

    def test_blog_list_returns_only_published_posts(self) -> None:
        """Public list excludes draft articles."""
        response = self.client.get(reverse("api:v1:website:blog-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["slug"], "seo-checklist")
        self.assertEqual(response.data["data"][0]["category"], "SEO")
        self.assertEqual(response.data["data"][0]["readTime"], 7)

    def test_blog_detail_returns_content_blocks(self) -> None:
        """Single post endpoint returns parsed content blocks."""
        response = self.client.get(
            reverse("api:v1:website:blog-detail", kwargs={"slug": "seo-checklist"}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["content"],
            ["Intro", "## Section", "Details"],
        )

    def test_blog_detail_returns_404_for_missing_or_draft_post(self) -> None:
        """Unknown and draft slugs are not accessible."""
        missing = self.client.get(
            reverse("api:v1:website:blog-detail", kwargs={"slug": "missing"}),
        )
        draft = self.client.get(
            reverse("api:v1:website:blog-detail", kwargs={"slug": "draft-article"}),
        )

        self.assertEqual(missing.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(draft.status_code, status.HTTP_404_NOT_FOUND)

    def test_blog_detail_supports_unicode_slug(self) -> None:
        """Unicode slugs are reachable through the detail endpoint."""
        BlogPost.objects.create(
            title="Unicode slug post",
            slug="внедрение-ai-систем",
            excerpt="Unicode slug excerpt",
            content="Unicode body",
            category=self.category,
            status="published",
            published_at=datetime(2026, 8, 3, tzinfo=dt_timezone.utc),
        )

        response = self.client.get("/api/v1/website/blog/внедрение-ai-систем/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["slug"], "внедрение-ai-систем")


class WebsitePortfolioAPITests(BaseAPITestCase):
    """Verify public portfolio endpoints."""

    def setUp(self) -> None:
        """Create sample portfolio projects."""
        super().setUp()
        from apps.website.models import PortfolioProject

        self.published = PortfolioProject.objects.create(
            title="Glow Beauty",
            slug="glow-beauty",
            category="E-commerce",
            description="Store for cosmetics",
            tags=["Дизайн", "SEO"],
            accent="violet",
            gradient="from-violet/60 to-cyan/40",
            featured=True,
            sort_order=1,
            metric="+640%",
            before_label="12 orders/month",
            after_label="89 orders/month",
            case_description="Full e-commerce launch",
            status="published",
        )
        PortfolioProject.objects.create(
            title="Draft project",
            slug="draft-project",
            category="Лендинг",
            description="Hidden",
            status="draft",
        )

    def test_portfolio_list_returns_only_published_projects(self) -> None:
        """Public list excludes draft projects."""
        response = self.client.get(reverse("api:v1:website:portfolio-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["slug"], "glow-beauty")
        self.assertTrue(response.data["data"][0]["hasCaseStudy"])
        self.assertEqual(response.data["data"][0]["before"], "12 orders/month")

    def test_portfolio_detail_returns_case_study_fields(self) -> None:
        """Single project endpoint returns case study details."""
        response = self.client.get(
            reverse("api:v1:website:portfolio-detail", kwargs={"slug": "glow-beauty"}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["caseDescription"], "Full e-commerce launch")
        self.assertEqual(response.data["data"]["gallery"], [])

    def test_portfolio_detail_returns_404_for_missing_or_draft_project(self) -> None:
        """Unknown and draft slugs are not accessible."""
        missing = self.client.get(
            reverse("api:v1:website:portfolio-detail", kwargs={"slug": "missing"}),
        )
        draft = self.client.get(
            reverse("api:v1:website:portfolio-detail", kwargs={"slug": "draft-project"}),
        )

        self.assertEqual(missing.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(draft.status_code, status.HTTP_404_NOT_FOUND)
