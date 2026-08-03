"""Convert existing blog slugs to Latin."""

from django.db import migrations, models

from apps.website.text import ensure_unique_slug, is_latin_slug, latin_slugify


def latinize_blog_slugs(apps, schema_editor) -> None:
    """Rewrite non-Latin blog slugs using transliteration."""
    BlogCategory = apps.get_model("website", "BlogCategory")
    BlogPost = apps.get_model("website", "BlogPost")

    for category in BlogCategory.objects.all().order_by("pk"):
        if category.slug and not is_latin_slug(category.slug):
            source = category.name or category.slug
            base_slug = latin_slugify(source)
            category.slug = ensure_unique_slug(BlogCategory, base_slug, exclude_pk=category.pk)
            category.save(update_fields=["slug"])

    for post in BlogPost.objects.all().order_by("pk"):
        if post.slug and not is_latin_slug(post.slug):
            source = post.title or post.slug
            base_slug = latin_slugify(source)
            post.slug = ensure_unique_slug(BlogPost, base_slug, exclude_pk=post.pk)
            post.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_seed_blog_posts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogcategory",
            name="slug",
            field=models.SlugField(
                allow_unicode=False,
                help_text="Заповнюється автоматично латиницею з назви.",
                max_length=100,
                unique=True,
                verbose_name="slug",
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="slug",
            field=models.SlugField(
                allow_unicode=False,
                help_text="Заповнюється автоматично латиницею з заголовка.",
                max_length=200,
                unique=True,
                verbose_name="slug",
            ),
        ),
        migrations.RunPython(latinize_blog_slugs, migrations.RunPython.noop),
    ]
