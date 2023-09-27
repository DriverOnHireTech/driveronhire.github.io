from rest_framework import serializers
from .models import User


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
<<<<<<< HEAD
        fields = ['phone', 'password']
=======
        fields= ['phone', 'usertype', 'password']
>>>>>>> 7a75edf39bf3040a65f0802dd4c93e522c362be9

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password']
