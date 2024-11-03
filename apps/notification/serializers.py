from rest_framework import serializers

from apps.notification.models import UserFCMToken


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFCMToken
        fields = ('token', 'user')
        extra_kwargs = {
            'user': {'required': False}
        }
