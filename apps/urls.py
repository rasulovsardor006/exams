from apps.auth.change_password import ChangePasswordView
from apps.auth.forgot_password import ForgotPasswordView
from apps.auth.login import  LoginAPIView
from apps.auth.register import RegisterView
from apps.auth.verification import VerifyEmailView
from django.urls import path

from apps.views import UserListCreateView, UserDetailView, SubjectListCreateView, SubjectDetailView, \
    ExamineListCreateView, ExamineDetailView, QuestionListCreateView, QuestionDetailView, AnswerListCreateView, \
    AnswerDetailView, AnswerListPDFDownloadView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Subject URL
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),

    # Examine URL
    path('examines/', ExamineListCreateView.as_view(), name='examine-list-create'),
    path('examines/<int:pk>/', ExamineDetailView.as_view(), name='examine-detail'),

    # Question URL
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('answers/', AnswerListCreateView.as_view(), name='answer-list-create'),
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
    path('answers-pdf-download/<int:pk>/',AnswerListPDFDownloadView.as_view(), name='answer-detail'),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),


]
