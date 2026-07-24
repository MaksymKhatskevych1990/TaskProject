"""Register periodic Celery Beat tasks."""

from django.conf import settings
from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    """Create or update django-celery-beat schedules used by the project."""

    help = "Register periodic Celery Beat tasks."

    def handle(self, *args, **options) -> None:
        reminder_hour = settings.TASK_REMINDER_HOUR
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour=str(reminder_hour),
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=settings.TIME_ZONE,
        )
        task, created = PeriodicTask.objects.update_or_create(
            name="Daily task deadline reminders",
            defaults={
                "task": "apps.tasks.tasks.send_daily_deadline_reminders",
                "crontab": schedule,
                "enabled": True,
            },
        )
        verb = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{verb} periodic task '{task.name}' at {reminder_hour:02d}:00 "
                f"({settings.TIME_ZONE})."
            )
        )
