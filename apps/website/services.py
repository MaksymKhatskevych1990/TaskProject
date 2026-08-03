"""Website business logic."""

from __future__ import annotations

import logging

from apps.website.models import ContactLead

logger = logging.getLogger(__name__)


def submit_contact_lead(
    *,
    name: str,
    phone: str,
    project: str,
    plan: str = "",
) -> ContactLead:
    """Record a contact request from the public landing page."""
    lead = ContactLead.objects.create(
        name=name,
        phone=phone,
        project=project,
        plan=plan,
    )
    logger.info(
        "Website contact lead received",
        extra={
            "contact_lead_id": str(lead.uuid),
            "contact_name": name,
            "contact_phone": phone,
            "contact_plan": plan or None,
            "contact_project_preview": project[:120],
        },
    )
    return lead


def parse_blog_content(content: str) -> list[str]:
    """Split stored blog content into renderable blocks."""
    normalized = content.replace("\r\n", "\n").replace("\r", "\n").strip()
    return [block.strip() for block in normalized.split("\n\n") if block.strip()]
