"""Serializers for public website endpoints."""

from rest_framework import serializers

from apps.website import services
from apps.website.models import BlogPost, PortfolioGalleryImage, PortfolioProject


def build_media_url(serializer: serializers.Serializer, file_field) -> str | None:
    """Return an absolute media URL when a file is present."""
    if not file_field:
        return None
    request = serializer.context.get("request")
    if request is not None:
        return request.build_absolute_uri(file_field.url)
    return file_field.url


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
        fields = ("slug", "title", "excerpt", "date", "readTime", "category")

    def get_date(self, obj: BlogPost) -> str:
        """Return the publication date as YYYY-MM-DD."""
        if obj.published_at is None:
            return ""
        return obj.published_at.date().isoformat()


class BlogPostDetailSerializer(BlogPostListSerializer):
    """Serialize a single blog post with full content."""

    content = serializers.SerializerMethodField()

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + ("content",)

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
        )

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

    class Meta(PortfolioProjectListSerializer.Meta):
        fields = PortfolioProjectListSerializer.Meta.fields + (
            "caseDescription",
            "gallery",
        )
