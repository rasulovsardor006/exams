from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.serializers import ChangeUserModelSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ChangeUserModelSerializer,
        responses={
            200: 'Password successfully changed',
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def post(self, request, *args, **kwargs):
        # Avval foydalanuvchi autentifikatsiya qilinganligini tekshiramiz
        if not request.user.is_authenticated:
            return Response({'message': 'Foydalanuvchi autentifikatsiya qilinmagan.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChangeUserModelSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user = request.user

            if user.is_verified:  # Faqat tasdiqlangan foydalanuvchilar parolni o'zgartira oladi
                user.set_password(password)
                user.save()
                return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Foydalanuvchi emailni tasdiqlamagan.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)