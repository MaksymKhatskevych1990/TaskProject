"""Tests for reusable abstract models."""

from django.db import models
from django.test import SimpleTestCase

from apps.common.models import BaseModel


class BaseModelTests(SimpleTestCase):
    """Verify the shared model contract without creating a table."""

    def test_base_model_is_abstract(self) -> None:
        """The base model must never create its own database table."""
        self.assertTrue(BaseModel._meta.abstract)

    def test_base_model_exposes_audit_fields(self) -> None:
        """Future models inherit identifiers, timestamps, and audit users."""
        field_names = {field.name for field in BaseModel._meta.fields}

        self.assertTrue(
            {
                "uuid",
                "created_at",
                "updated_at",
                "created_by",
                "updated_by",
            }.issubset(field_names)
        )
        self.assertTrue(BaseModel._meta.get_field("uuid").unique)
        self.assertTrue(BaseModel._meta.get_field("created_by").null)
        self.assertEqual(
            BaseModel._meta.get_field("created_by").remote_field.on_delete,
            models.SET_NULL,
        )
