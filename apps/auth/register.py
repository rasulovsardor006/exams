from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from apps.models import User
from apps.auth.serializers import RegisterSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.models import User

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            status.HTTP_200_OK: "emailga habar ketdi",
            status.HTTP_404_NOT_FOUND: "Email not found"
        }
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_mail(
                'Tasdiqlash Kodingiz',
                f'Sizning tasdiqlash kodingiz: {user.verification_code}',
                'your_email@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Foydalanuvchi ro'yxatdan o'tdi. Tasdiqlash uchun email tekshiring."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

