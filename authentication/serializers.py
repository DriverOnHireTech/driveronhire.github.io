from rest_framework import serializers
from .models import User
from fcm_django.models import FCMDevice


class NewUserSerializer(serializers.ModelSerializer):
    # phone= serializers.IntegerField(max_value=100000000000, min_value=10)
    class Meta:
        model = User
        fields= ['phone', 'usertype', 'password', 'id', 'type', 'name' ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserLoginserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'otp']


class Fcmserializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = "__all__"