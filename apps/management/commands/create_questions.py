from django.core.management.base import BaseCommand
from apps.models import Examine, Question

class Command(BaseCommand):
    help = 'Create random questions for exams'

    def handle(self, *args, **options):
        exams = Examine.objects.all()
        questions_data = [
            {"title": "What is 2 + 2?", "option_a": "3", "option_b": "4", "option_c": "5", "correct_answer": "B"},
            {"title": "What is the capital of France?", "option_a": "Berlin", "option_b": "London", "option_c": "Paris", "correct_answer": "C"},
            {"title": "What is the boiling point of water?", "option_a": "100C", "option_b": "90C", "option_c": "80C", "correct_answer": "A"}
        ]

        for exam in exams:
            for q_data in questions_data:
                question, created = Question.objects.get_or_create(
                    exam=exam,
                    title=q_data["title"],
                    defaults={
                        "option_a": q_data["option_a"],
                        "option_b": q_data["option_b"],
                        "option_c": q_data["option_c"],
                        "correct_answer": q_data["correct_answer"]
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Question "{question.title}" created for exam "{exam.subject.name}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'Question "{question.title}" already exists in exam "{exam.subject.name}"'))
