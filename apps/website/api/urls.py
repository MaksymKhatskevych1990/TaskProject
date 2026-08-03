"""Website API routes."""

from django.urls import path

from apps.website.api import views

app_name = "website"

urlpatterns = [
    path("contact/", views.ContactLeadView.as_view(), name="contact"),
    path("blog/", views.BlogPostListView.as_view(), name="blog-list"),
    path("blog/<slug:slug>/", views.BlogPostDetailView.as_view(), name="blog-detail"),
    path("portfolio/", views.PortfolioProjectListView.as_view(), name="portfolio-list"),
    path(
        "portfolio/<slug:slug>/",
        views.PortfolioProjectDetailView.as_view(),
        name="portfolio-detail",
    ),
]
