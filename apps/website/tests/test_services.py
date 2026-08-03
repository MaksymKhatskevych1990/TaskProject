"""Tests for website selectors and services."""

from django.utils import timezone

from apps.website import services
from apps.website.models import BlogCategory, BlogPost, ContactLead
from apps.website.selectors import get_published_blog_post, list_published_blog_posts
from tests.base import BaseTestCase


class WebsiteServiceTests(BaseTestCase):
    """Verify website business logic."""

    def test_submit_contact_lead_persists_record(self) -> None:
        """Contact submissions are stored in the database."""
        lead = services.submit_contact_lead(
            name="Олена П.",
            phone="@olena",
            project="Потрібен лендинг",
            plan="Бізнес",
        )

        self.assertEqual(ContactLead.objects.count(), 1)
        self.assertEqual(lead.name, "Олена П.")

    def test_parse_blog_content_splits_blocks(self) -> None:
        """Blog content is split into paragraphs and headings."""
        content = "Intro\n\n## Heading\n\nParagraph two"
        self.assertEqual(
            services.parse_blog_content(content),
            ["Intro", "## Heading", "Paragraph two"],
        )

    def test_parse_blog_content_normalizes_windows_line_endings(self) -> None:
        """Windows line endings are normalized before splitting."""
        content = "Intro\r\n\r\n## Heading\r\n\r\n* **Item one.**\r\n* **Item two.**"
        self.assertEqual(
            services.parse_blog_content(content),
            ["Intro", "## Heading", "* **Item one.**\n* **Item two.**"],
        )


class WebsiteSelectorTests(BaseTestCase):
    """Verify website read queries."""

    def setUp(self) -> None:
        """Create sample blog content."""
        super().setUp()
        self.category = BlogCategory.objects.create(name="SEO", slug="seo")
        self.published = BlogPost.objects.create(
            title="Published post",
            slug="published-post",
            excerpt="Short excerpt",
            content="Body paragraph",
            category=self.category,
            status="published",
            published_at=timezone.now(),
            read_time_minutes=5,
        )
        BlogPost.objects.create(
            title="Draft post",
            slug="draft-post",
            excerpt="Hidden excerpt",
            content="Draft body",
            category=self.category,
            status="draft",
        )

    def test_list_published_blog_posts_excludes_drafts(self) -> None:
        """Only published posts appear in the public list."""
        posts = list(list_published_blog_posts())
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].slug, "published-post")

    def test_get_published_blog_post_returns_none_for_draft(self) -> None:
        """Draft posts are not accessible by slug."""
        self.assertIsNone(get_published_blog_post(slug="draft-post"))
        self.assertEqual(
            get_published_blog_post(slug="published-post"),
            self.published,
        )
