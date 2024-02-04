from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument("task", type=str)
		parser.add_argument("every", nargs=1, type=int)

	def handle(self, *args, **options):
		task = options["task"]
		every = options["every"][0]
		interval, is_created = IntervalSchedule.objects.get_or_create(
            every=every, period="hours")
		try:
			PeriodicTask.objects.create(
				name=task,
				task=task,
				interval=interval,
				start_time=timezone.now().date(),
			)
			return f"Создана периодическая задача {task}"
		except ValidationError:
			return f"Задача {task} уже существует"
