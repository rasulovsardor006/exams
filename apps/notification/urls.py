from django.urls import path

from apps.notification.views import RegisterFcmToken

app_name = 'notification'

urlpatterns = [
    path("RegisterFcmToken/", RegisterFcmToken.as_view(), name="register-fcm-token"),
]
