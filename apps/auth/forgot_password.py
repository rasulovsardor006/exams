from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from apps.models import User  # O'z modelingizga mos keladigan joyni o'zgartiring
from .serializers import EmailSerializer  # Email uchun serializer

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)  # Foydalanuvchini topish
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        # Tasodifiy 6-honali kod yaratish
        verification_code = get_random_string(length=6, allowed_chars='0123456789')

        # Email yuborish
        send_mail(
            'Forgot Password Verification Code',
            f'Sizning tasdiqlash kodingiz: {verification_code}',
            'from@example.com',  # Sizning emailingiz
            [email],
            fail_silently=False,
        )

        # Kodni saqlash (masalan, User modelida)
        user.verification_code = verification_code
        user.save()

        return Response({"message": "Tasdiqlash kodi yuborildi!"}, status=status.HTTP_200_OK)
