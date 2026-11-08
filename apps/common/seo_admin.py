"""Admin presentation for SEO fields."""

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.common.seo import SeoFieldsMixin

SEO_FIELDSET = (
    _("SEO"),
    {
        "description": _(
            "Эти поля попадают в title, сниппет Google и превью в соцсетях. "
            "Пустое поле подставляет название или описание страницы."
        ),
        "fields": SeoFieldsMixin.SEO_FIELDS,
    },
)

SEO_ADMIN_MEDIA = {
    "css": {"all": ("website/admin/seo_fields.css",)},
    "js": ("website/admin/seo_fields.js",),
}


def seo_status_badge(obj: SeoFieldsMixin) -> str:
    """Show whether the Google snippet fields are ready."""
    if obj.seo_is_complete():
        label, color = _("готово"), "#198754"
    elif (obj.seo_title or "").strip() or (obj.seo_description or "").strip():
        label, color = _("частично"), "#fd7e14"
    else:
        label, color = _("пусто"), "#6c757d"
    return format_html(
        '<span style="display:inline-block;padding:2px 8px;border-radius:12px;'
        'color:#fff;background:{};font-weight:600;">{}</span>',
        color,
        label,
    )
