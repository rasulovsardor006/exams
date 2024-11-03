from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.models import Subject, Examine, User
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create random exams for subjects'

    def handle(self, *args, **options):
        user = User.objects.first()  # User tanlab olish
        subjects = Subject.objects.all()  # Mavjud barcha fanlarni olish

        for subject in subjects:
            start_time = timezone.now()
            end_time = start_time + timedelta(hours=1)

            exam, created = Examine.objects.get_or_create(
                subject=subject,
                user=user,
                defaults={"start_time": start_time, "end_time": end_time}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Exam for subject "{subject.name}" created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Exam for subject "{subject.name}" already exists'))
