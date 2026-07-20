"""Add Telegram link tokens."""

import uuid

from django.db import migrations, models


def populate_link_tokens(apps, schema_editor) -> None:
    """Assign unique link tokens to existing Telegram accounts."""
    TelegramAccount = apps.get_model("telegram", "TelegramAccount")
    for account in TelegramAccount.objects.all().iterator():
        account.link_token = uuid.uuid4()
        account.save(update_fields=["link_token"])


class Migration(migrations.Migration):
    """Add link_token field used for bot account binding."""

    dependencies = [
        ("telegram", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="telegramaccount",
            name="link_token",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                null=True,
                verbose_name="токен привязки",
            ),
        ),
        migrations.RunPython(populate_link_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="telegramaccount",
            name="link_token",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                verbose_name="токен привязки",
            ),
        ),
    ]
