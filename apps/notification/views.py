from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.notification.models import UserFCMToken
from apps.notification.serializers import FCMTokenSerializer


# Create your views here.

class RegisterFcmToken(CreateAPIView):
    serializer_class = FCMTokenSerializer
    queryset = UserFCMToken.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



