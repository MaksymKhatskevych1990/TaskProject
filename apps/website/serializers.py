"""Serializers for public website endpoints."""

from rest_framework import serializers

from apps.common.seo import SeoFieldsMixin
from apps.website import services
from apps.website.models import (
    BlogPost,
    PortfolioGalleryImage,
    PortfolioProject,
    SiteSeoSettings,
)


def build_seo_payload(
    serializer: serializers.Serializer,
    obj: SeoFieldsMixin,
    *,
    title_fallback: str,
    description_fallback: str,
) -> dict:
    """Return resolved public SEO values for a page."""
    return {
        "title": obj.resolve_seo_title(title_fallback),
        "description": obj.resolve_seo_description(description_fallback),
        "h1": obj.resolve_h1(title_fallback),
        "ogTitle": obj.resolve_og_title(title_fallback),
        "ogDescription": obj.resolve_og_description(description_fallback),
        "ogImage": build_media_url(serializer, obj.og_image),
        "canonicalUrl": obj.canonical_url or "",
        "noindex": obj.robots_noindex,
        "focusKeyword": obj.focus_keyword,
    }


def build_media_url(serializer: serializers.Serializer, file_field) -> str | None:
    """Return a browser-reachable media URL when a file is present.

    MinIO internal URLs (`minio:9000`) are rewritten to same-origin `/media/...`
    paths that nginx proxies. Relative paths avoid wrong host/port (e.g. missing
    `:8080`) and work with Next.js `unoptimized` images loaded by the browser.
    """
    if not file_field:
        return None

    raw_url = file_field.url
    if "minio:9000" in raw_url:
        path = raw_url.split("minio:9000", 1)[1]
        # path-style: /bucket/key?... → /media/key?...
        parts = path.lstrip("/").split("/", 1)
        if len(parts) == 2:
            _bucket, rest = parts
            return f"/media/{rest}"
        return f"/media/{path.lstrip('/')}"

    request = serializer.context.get("request")
    if request is not None:
        return request.build_absolute_uri(raw_url)
    return raw_url


class ContactLeadSerializer(serializers.Serializer):
    """Validate a contact form submission from the landing page."""

    name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=120)
    project = serializers.CharField(max_length=2000)
    plan = serializers.CharField(max_length=50, required=False, allow_blank=True)


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serialize blog posts for the public listing page."""

    date = serializers.SerializerMethodField()
    readTime = serializers.IntegerField(source="read_time_minutes")
    category = serializers.CharField(source="category.name")

    class Meta:
        model = BlogPost
        fields = ("slug", "title", "excerpt", "date", "readTime", "category", "noindex")

    noindex = serializers.BooleanField(source="robots_noindex")

    def get_date(self, obj: BlogPost) -> str:
        """Return the publication date as YYYY-MM-DD."""
        if obj.published_at is None:
            return ""
        return obj.published_at.date().isoformat()


class BlogPostDetailSerializer(BlogPostListSerializer):
    """Serialize a single blog post with full content."""

    content = serializers.SerializerMethodField()
    seo = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + ("content", "seo", "updatedAt")

    def get_seo(self, obj: BlogPost) -> dict:
        """Return resolved SEO for the article page."""
        return build_seo_payload(
            self,
            obj,
            title_fallback=obj.title,
            description_fallback=obj.excerpt,
        )

    def get_updatedAt(self, obj: BlogPost) -> str:
        """Return the last update date as YYYY-MM-DD."""
        return obj.updated_at.date().isoformat()

    def get_content(self, obj: BlogPost) -> list[str]:
        """Return content split into paragraphs and headings."""
        return services.parse_blog_content(obj.content)


class PortfolioGalleryImageSerializer(serializers.ModelSerializer):
    """Serialize a portfolio gallery image."""

    imageUrl = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioGalleryImage
        fields = ("imageUrl", "caption", "ordering")

    def get_imageUrl(self, obj: PortfolioGalleryImage) -> str | None:
        """Return an absolute URL for the gallery image."""
        return build_media_url(self, obj.image)


class PortfolioProjectListSerializer(serializers.ModelSerializer):
    """Serialize portfolio projects for the public listing."""

    coverImage = serializers.SerializerMethodField()
    clientUrl = serializers.URLField(source="client_url", allow_blank=True)
    before = serializers.CharField(source="before_label", allow_blank=True)
    after = serializers.CharField(source="after_label", allow_blank=True)
    hasCaseStudy = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioProject
        fields = (
            "slug",
            "title",
            "category",
            "description",
            "tags",
            "accent",
            "gradient",
            "coverImage",
            "featured",
            "metric",
            "before",
            "after",
            "clientUrl",
            "hasCaseStudy",
            "noindex",
        )

    noindex = serializers.BooleanField(source="robots_noindex")

    def get_coverImage(self, obj: PortfolioProject) -> str | None:
        """Return an absolute URL for the cover image."""
        return build_media_url(self, obj.cover_image)

    def get_hasCaseStudy(self, obj: PortfolioProject) -> bool:
        """Return whether the project has case study metrics."""
        return bool(obj.metric and obj.before_label and obj.after_label)


class PortfolioProjectDetailSerializer(PortfolioProjectListSerializer):
    """Serialize a single portfolio project with case study details."""

    caseDescription = serializers.CharField(source="case_description")
    gallery = PortfolioGalleryImageSerializer(source="gallery_images", many=True)
    seo = serializers.SerializerMethodField()

    class Meta(PortfolioProjectListSerializer.Meta):
        fields = PortfolioProjectListSerializer.Meta.fields + (
            "caseDescription",
            "gallery",
            "seo",
        )

    def get_seo(self, obj: PortfolioProject) -> dict:
        """Return resolved SEO for a portfolio case."""
        return build_seo_payload(
            self,
            obj,
            title_fallback=obj.title,
            description_fallback=obj.description,
        )


class SiteSeoSettingsSerializer(serializers.ModelSerializer):
    """Serialize public site-wide SEO defaults."""

    seo = serializers.SerializerMethodField()
    blogTitle = serializers.CharField(source="blog_title", allow_blank=True)
    blogDescription = serializers.CharField(source="blog_description", allow_blank=True)
    blogH1 = serializers.CharField(source="blog_h1", allow_blank=True)
    googleSiteVerification = serializers.CharField(
        source="google_site_verification",
        allow_blank=True,
    )

    class Meta:
        model = SiteSeoSettings
        fields = (
            "seo",
            "blogTitle",
            "blogDescription",
            "blogH1",
            "googleSiteVerification",
        )

    def get_seo(self, obj: SiteSeoSettings) -> dict:
        """Return resolved homepage SEO."""
        from apps.website.seo_defaults import HOME_DESCRIPTION, HOME_TITLE

        payload = build_seo_payload(
            self,
            obj,
            title_fallback=HOME_TITLE,
            description_fallback=HOME_DESCRIPTION,
        )
        payload["h1"] = (obj.seo_h1 or obj.hero_title or "").strip()
        return payload
