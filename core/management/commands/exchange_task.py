from django.core.management.base import BaseCommand
from core.tasks import fetch_usd_to_bdt_rate
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


class Command(BaseCommand):
    help = "Creates a scheduler for exchange rate fetching task"

    def handle(self, *args, **options):

        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )

        task_name = "Exchange Rate"
        task_path = "core.tasks.fetch_usd_to_bdt_rate"

        if not PeriodicTask.objects.filter(name=task_name).exists():
            PeriodicTask.objects.create(
                interval=schedule,
                name=task_name,
                task=task_path,
                args=json.dumps([]),
                kwargs=json.dumps({}),
            )
            print(f"Periodic task '{task_name}' created successfully.")
        else:
            print(f"Periodic task '{task_name}' already exists.")
