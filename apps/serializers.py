from rest_framework import serializers
from .models import Answer
from rest_framework import serializers
from .models import User, Subject, Examine, Question

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'is_verified', 'is_active']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'user']



class ExamineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examine
        fields = ['id', 'subject', 'user', 'start_time', 'end_time', 'duration']



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'option_a', 'option_b', 'option_c', 'correct_answer', 'exam']







class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'selected_option', 'created_at']