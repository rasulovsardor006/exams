from django.contrib.auth.hashers import  make_password

from rest_framework import serializers

from apps.models import User

class ChangeUserModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=55)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True},
                        'confirm_password': {'write_only': True}}




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Foydalanuvchini yaratish
        user = User(
            name=validated_data['name'],
            email=validated_data['email']
        )
        user.password = make_password(validated_data['password'])  # Parolni hashlash
        user.save()
        return user

# apps/auth/serializers.py
# apps/auth/serializers.py
# apps/auth/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext as _

# User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError(_('Invalid email or password.'))

        if not user.check_password(attrs['password']):
            raise serializers.ValidationError(_('Invalid email or password.'))

        return attrs




class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

