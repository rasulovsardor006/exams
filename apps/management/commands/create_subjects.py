from django.core.management.base import BaseCommand
from apps.models import Subject, User

class Command(BaseCommand):
    help = 'Create random subjects'

    def handle(self, *args, **options):
        user = User.objects.first()  # Admin yoki mavjud foydalanuvchilardan birini tanlash
        subjects = [
            {"name": "Mathematics", "description": "Basic math course"},
            {"name": "Physics", "description": "Introductory physics"},
            {"name": "Chemistry", "description": "Basic chemistry concepts"}
        ]
        for subject_data in subjects:
            subject, created = Subject.objects.get_or_create(
                name=subject_data["name"],
                defaults={"description": subject_data["description"], "user": user}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Subject "{subject.name}" created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Subject "{subject.name}" already exists'))
