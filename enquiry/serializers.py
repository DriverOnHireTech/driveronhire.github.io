from rest_framework import serializers
from .models import Enquiry, driverenquiry



class MyEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'


class DriverEnquiryserializer(serializers.ModelSerializer):
    class Meta:
        model= driverenquiry
        fields = ('phone_number', 'name', 'message', 'email')
        