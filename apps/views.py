from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import User, Subject, Examine, Question
from .serializers import UserSerializer, SubjectSerializer, ExamineSerializer, QuestionSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Answer
from .serializers import AnswerSerializer
from reportlab.lib import colors


# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


# Examine Views
class ExamineListCreateView(generics.ListCreateAPIView):
    queryset = Examine.objects.all()
    serializer_class = ExamineSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExamineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Examine.objects.all()
    serializer_class = ExamineSerializer
    permission_classes = [permissions.IsAdminUser]


# Question Views
class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        question = serializer.validated_data.get('question')

        if Answer.objects.filter(user=user, question=question).exists():
            raise ValidationError("Siz ushbu savolga avval javob bergansiz, boshqa savoldi tanlang!")

        serializer.save(user=user)

    def get(self, request, *args, **kwargs):
        user_answers = self.get_queryset().filter(user=request.user)
        score = sum(5 for answer in user_answers if answer.is_correct())
        response_data = {
            'answers': AnswerSerializer(user_answers, many=True).data,
            'score': score
        }
        return Response(response_data, status=status.HTTP_200_OK)

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get user answer details and calculate score")
    def get(self, request, *args, **kwargs):
        user_answers = Answer.objects.filter(user=request.user)

        score = 0
        total_correct = 0

        for user_answer in user_answers:
            if user_answer.is_correct():
                score += 5
                total_correct += 1

        answer_data = [{
            "question_id": user_answer.question_id,
            "selected_option": user_answer.selected_option,
            "is_correct": user_answer.is_correct()
        } for user_answer in user_answers]

        return Response({
            "answers": answer_data,
            "total_correct": total_correct,
            "score": score
        })
class AnswerListPDFDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Barcha javoblarni PDF formatida yuklab olish")
    def get(self, request, *args, **kwargs):
        answers = Answer.objects.filter(user=request.user)

        score = 0
        total_correct = 0
        for answer in answers:
            if answer.is_correct():
                score += 5
                total_correct += 1

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="all_answers.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        p.drawString(100, 750, f"Foydalanuvchi: {request.user.name}:{request.user.role}")
        p.drawString(100, 730, f"Jami ball: {score}")
        p.drawString(100, 710, "Foydalanuvchi javoblari ro'yxati")

        y = 680
        for answer in answers:
            if answer.is_correct():
                p.setFillColor("#008000")
            else:
                p.setFillColor("#FF0000")

            p.drawString(100, y, f"Savol ID: {answer.question_id}, Select: {answer.selected_option}, Correct: {answer.is_correct()}")
            y -= 20

            if y < 50:
                p.showPage()
                y = 750

        p.showPage()
        p.save()

        return response
