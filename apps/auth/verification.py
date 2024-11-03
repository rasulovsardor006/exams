from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.models import User



class VerifyEmailView(APIView):
    permission_classes = [AllowAny]  # To'g'ri formatda ro'yxat
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'verification_code': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'verification_code']
        )
    )
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('verification_code')
        try:
            user = User.objects.get(email=email, verification_code=code)
            user.is_verified = True
            user.save()
            return Response({"message": "Email tasdiqlandi."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Noto'g'ri kod yoki email."}, status=status.HTTP_400_BAD_REQUEST)








