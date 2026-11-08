"""Assemble public landing-page content from site settings."""

from apps.website.models import SiteSeoSettings, split_lines
from apps.website.seo_defaults import HOME_DESCRIPTION, HOME_TITLE
from apps.website.serializers import build_seo_payload

CMS_PREFETCH = (
    "sitenavlink_items",
    "siteherooffer_items",
    "siteservice_items",
    "sitestat_items",
    "sitetestimonial_items",
    "sitecasestudy_items",
    "siteprocessstep_items",
    "sitepricingplan_items",
    "siteguarantee_items",
    "sitefaqitem_items",
    "siteoffice_items",
)


def get_site_settings() -> SiteSeoSettings:
    """Return the singleton settings row with landing blocks prefetched."""
    settings, _created = (
        SiteSeoSettings.objects.prefetch_related(*CMS_PREFETCH).get_or_create(pk=1)
    )
    return settings


def build_site_content(settings: SiteSeoSettings, *, serializer=None) -> dict:
    """Return the public CMS payload consumed by the marketing site."""
    seo = {
        "title": settings.resolve_seo_title(HOME_TITLE),
        "description": settings.resolve_seo_description(
            settings.site_description or HOME_DESCRIPTION
        ),
        "h1": (settings.seo_h1 or settings.hero_title or "").strip(),
        "ogTitle": settings.resolve_og_title(HOME_TITLE),
        "ogDescription": settings.resolve_og_description(
            settings.site_description or HOME_DESCRIPTION
        ),
        "ogImage": None,
        "canonicalUrl": settings.canonical_url or "",
        "noindex": settings.robots_noindex,
        "focusKeyword": settings.focus_keyword,
    }
    if serializer is not None:
        seo = build_seo_payload(
            serializer,
            settings,
            title_fallback=HOME_TITLE,
            description_fallback=settings.site_description or HOME_DESCRIPTION,
        )
        seo["h1"] = (settings.seo_h1 or settings.hero_title or "").strip()

    return {
        "brand": settings.brand,
        "brandShort": settings.brand_short,
        "domain": settings.domain,
        "tagline": settings.tagline,
        "description": settings.site_description,
        "email": settings.email,
        "phone": settings.phone,
        "telegramUsername": settings.telegram_handle,
        "telegramUrl": settings.telegram_url,
        "foundingYear": settings.founding_year,
        "currency": settings.currency,
        "locale": settings.locale,
        "nav": [
            {"href": item.href, "label": item.label}
            for item in settings.sitenavlink_items.all()
        ],
        "hero": {
            "status": settings.hero_status,
            "statusMeta": settings.hero_status_meta,
            "title": settings.hero_title,
            "hint": settings.hero_hint,
            "primaryCta": settings.hero_primary_cta,
            "secondaryCta": settings.hero_secondary_cta,
            "chameleonLabel": settings.hero_chameleon_label,
            "conditions": split_lines(settings.hero_conditions),
            "offers": [
                {
                    "id": item.slug,
                    "label": item.label,
                    "duration": item.duration,
                    "price": item.price,
                    "plan": item.plan,
                    "includes": item.includes,
                }
                for item in settings.siteherooffer_items.all()
            ],
        },
        "sections": {
            "services": {
                "eyebrow": settings.services_eyebrow,
                "title": settings.services_title,
                "subtitle": settings.services_subtitle,
                "also": settings.services_also,
            },
            "cases": {
                "eyebrow": settings.cases_eyebrow,
                "title": settings.cases_title,
                "subtitle": settings.cases_subtitle,
                "before": settings.cases_before_label,
                "after": settings.cases_after_label,
                "result": settings.cases_result_label,
            },
            "portfolio": {
                "eyebrow": settings.portfolio_eyebrow,
                "title": settings.portfolio_title,
                "subtitle": settings.portfolio_subtitle,
                "viewAll": settings.portfolio_cta,
            },
            "process": {
                "eyebrow": settings.process_eyebrow,
                "title": settings.process_title,
                "subtitle": settings.process_subtitle,
            },
            "pricing": {
                "eyebrow": settings.pricing_eyebrow,
                "title": settings.pricing_title,
                "subtitle": settings.pricing_subtitle,
                "from": settings.pricing_from_label,
                "choosePlan": settings.pricing_cta,
            },
            "guarantees": {
                "eyebrow": settings.guarantees_eyebrow,
                "title": settings.guarantees_title,
            },
            "faq": {
                "eyebrow": settings.faq_eyebrow,
                "title": settings.faq_title,
            },
        },
        "services": [
            {
                "title": item.title,
                "description": item.description,
                "features": split_lines(item.features),
                "featured": item.featured,
            }
            for item in settings.siteservice_items.all()
        ],
        "stats": [
            {
                "value": item.value,
                "suffix": item.suffix,
                "label": item.label,
                "decimals": item.decimals,
            }
            for item in settings.sitestat_items.all()
        ],
        "testimonials": [
            {
                "name": item.name,
                "role": item.role,
                "text": item.text,
                "rating": item.rating,
            }
            for item in settings.sitetestimonial_items.all()
        ],
        "cases": [
            {
                "category": item.category,
                "title": item.title,
                "description": item.description,
                "before": item.before_value,
                "after": item.after_value,
                "metric": item.metric,
                "metricLabel": item.metric_label,
            }
            for item in settings.sitecasestudy_items.all()
        ],
        "process": [
            {"title": item.title, "description": item.description}
            for item in settings.siteprocessstep_items.all()
        ],
        "pricing": [
            {
                "slug": item.slug,
                "name": item.name,
                "price": item.price,
                "description": item.description,
                "features": split_lines(item.features),
                "highlighted": item.highlighted,
                "badge": item.badge,
            }
            for item in settings.sitepricingplan_items.all()
        ],
        "guarantees": [
            {
                "title": item.title,
                "description": item.description,
                "image": item.image_key,
            }
            for item in settings.siteguarantee_items.all()
        ],
        "faq": [
            {"question": item.question, "answer": item.answer}
            for item in settings.sitefaqitem_items.all()
        ],
        "offices": [
            {
                "id": item.slug,
                "name": item.name,
                "label": item.label,
                "streetAddress": item.street_address,
                "addressLocality": item.address_locality,
                "addressRegion": item.address_region,
                "postalCode": item.postal_code,
                "addressCountry": item.address_country,
                "geo": {"latitude": item.latitude, "longitude": item.longitude},
                "telephone": item.telephone,
                "isHeadquarters": item.is_headquarters,
            }
            for item in settings.siteoffice_items.all()
        ],
        "contact": {
            "title": settings.contact_title,
            "subtitle": settings.contact_subtitle,
            "submit": settings.contact_submit,
            "submitting": settings.contact_submitting,
            "successTitle": settings.contact_success_title,
            "successSubtitle": settings.contact_success_subtitle,
            "errorMessage": settings.contact_error,
            "fields": {
                "name": {
                    "label": settings.contact_name_label,
                    "placeholder": settings.contact_name_placeholder,
                },
                "phone": {
                    "label": settings.contact_phone_label,
                    "placeholder": settings.contact_phone_placeholder,
                },
                "project": {
                    "label": settings.contact_project_label,
                    "placeholder": settings.contact_project_placeholder,
                },
                "plan": {"label": settings.contact_plan_label},
            },
        },
        "footer": {
            "about": settings.footer_about,
            "rights": settings.footer_rights,
            "blog": settings.footer_blog_label,
            "telegram": settings.footer_telegram_label,
            "writeInTelegram": settings.footer_write_telegram,
            "offices": settings.footer_offices_label,
            "faq": settings.footer_faq_label,
        },
        "blogPage": {
            "eyebrow": settings.blog_page_eyebrow,
            "title": settings.blog_page_title,
            "subtitle": settings.blog_page_subtitle,
            "readMore": settings.blog_read_more,
            "backToBlog": settings.blog_back_label,
            "readTime": settings.blog_read_time_label,
            "empty": settings.blog_empty,
            "ctaTitle": settings.blog_cta_title,
            "ctaSubtitle": settings.blog_cta_subtitle,
            "ctaButton": settings.blog_cta_button,
        },
        "seo": seo,
        "blogTitle": settings.blog_title,
        "blogDescription": settings.blog_description,
        "blogH1": settings.blog_h1,
        "googleSiteVerification": settings.google_site_verification,
    }
