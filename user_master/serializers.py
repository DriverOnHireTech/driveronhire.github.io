from rest_framework import serializers
from .models import *


class MyCountrySerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(max_length=5, required=False)
    country_name = serializers.CharField(max_length=30, required=True)
    status = serializers.BooleanField(default=True)

    class Meta:
        model = Country
        fields = '__all__'


class MyStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__' 


class MyCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class MyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class MyZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'


class MyBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class MyReferenceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'


class MyTaxSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'


class MyCarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class MyCouponSerializers(serializers.ModelSerializer):
    class Meta:
        model = CouponList
        fields = '__all__'


class MySubscriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class UsermasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = '__all__'

class Regionserializer(serializers.ModelSerializer):
    class Meta:
        model = region
        fields = '__all__'

class chargestwohrsserailizer(serializers.ModelSerializer):
    class Meta:
        model= localtwohrscharges
        fields="__all__"