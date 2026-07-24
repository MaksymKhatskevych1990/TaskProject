"""Hook dashboard metrics into the Django admin index."""

from types import MethodType

from django.contrib import admin
from django.contrib.admin.sites import AdminSite


def _index_with_dashboard(
    self: AdminSite,
    request,
    extra_context=None,
):
    """Inject studio dashboard metrics into the admin home page."""
    from apps.dashboard.selectors import get_studio_dashboard

    context = dict(extra_context or {})
    context["studio_dashboard"] = get_studio_dashboard()
    return self._studio_original_index(request, extra_context=context)


def register_admin_dashboard() -> None:
    """Extend the default admin index with dashboard widgets once."""
    if hasattr(admin.site, "_studio_original_index"):
        return

    admin.site._studio_original_index = admin.site.index
    admin.site.index = MethodType(_index_with_dashboard, admin.site)
