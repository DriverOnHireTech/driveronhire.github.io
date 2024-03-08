from django.shortcuts import render, HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from rest_framework import status
from .models import *
from .serializers import *
import requests

def home(request):
    return render(request, 'user_master/index.html')

# Registering New user
class createUsermaster(APIView):
    def post(self, request):
        data = request.data
        
        serializer=UsermasterSerializer(data=data)
        
        if serializer.is_valid():           
            obj=serializer.save()
            msg="User is created"
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        if serializer.is_valid():
           
            serializer.save()
            msg = "User not created"
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyCountryList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    queryset = Country.objects.all()
    serializer_class = MyCountrySerializer


class MyCountryGetList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    try:
        def get(self, request, pk):
            try:
                country = Country.objects.get(pk=pk)
                serializer = MyCountrySerializer(country)
                return Response(serializer.data)
            except Country.DoesNotExist:
                return Response({'error': 'Country not found'}, status=404)
    except:
        Response({'msg': 'Not Authenticated'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    serializer_class = MyCountrySerializer

    def put(self, request, pk):
        try:
            country = Country.objects.get(pk=pk)
            serializer = MyCountrySerializer(country, data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Country.DoesNotExist:
            return Response({'error': 'Country not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            country = Country.objects.get(pk=pk)
            country.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Country.DoesNotExist:
            return Response({'error': 'Country not found'}, status=status.HTTP_404_NOT_FOUND)


class MyStateList(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = MyStateSerializer


class MyStateGetList(APIView):
    def get(self, request, pk):
        try:
            state = State.objects.get(pk=pk)
            serializer = MyStateSerializer(state)
            return Response(serializer.data)
        except State.DoesNotExist:
            return Response({'error': 'State not found'}, status=404)

    serializer_class = MyStateSerializer

    def put(self, request, pk):
        try:
            state = State.objects.get(pk=pk)
            serializer = MyStateSerializer(state, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except State.DoesNotExist:
            return Response({'error': 'State not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            state = State.objects.get(pk=pk)
            state.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except State.DoesNotExist:
            return Response({'error': 'State not found'}, status=status.HTTP_404_NOT_FOUND)


class MyCityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = MyCitySerializer


class MyCityGetList(APIView):
    def get(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
            serializer = MyCitySerializer(city)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({'error': 'City not found'}, status=404)

    serializer_class = MyCitySerializer

    def put(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
            serializer = MyCitySerializer(city, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except City.DoesNotExist:
            return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
            city.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)


class MyLocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = MyLocationSerializer


class MyLocationGetList(APIView):
    def get(self, request, id):
        try:
            location = Location.objects.get(id=id)
            serializer = MyLocationSerializer(location)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = MyLocationSerializer

    def put(self, request, id):
        try:
            location = Location.objects.get(id=id)
            serializer = MyLocationSerializer(location, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            location = Location.objects.get(id=id)
            location.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)


class MyZoneList(generics.ListCreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = MyZoneSerializer


class MyZoneGetList(APIView):
    def get(self, request, id):
        try:
            zone = Zone.objects.get(id=id)
            serializer = MyZoneSerializer(zone)
            return Response(serializer.data)
        except Zone.DoesNotExist:
            return Response({'error': 'Zone not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = MyZoneSerializer

    def put(self, request, id):
        try:
            zone = Zone.objects.get(id=id)
            serializer = MyZoneSerializer(zone, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Zone.DoesNotExist:
            return Response({'error': 'Zone not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            zone = Zone.objects.get(id=id)
            zone.delete()
            return Response({'message': 'Object deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Zone.DoesNotExist:
            return Response({'error': 'Zone not found'}, status=status.HTTP_404_NOT_FOUND)


class MyBranchList(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = MyBranchSerializer


class MyBranchGetList(APIView):
    def get(self, request, id):
        try:
            branch = Branch.objects.get(id=id)
            serializer = MyBranchSerializer(branch)
            return Response(serializer.data)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = MyBranchSerializer

    def put(self, request, id):
        try:
            branch = Branch.objects.get(id=id)
            serializer = MyBranchSerializer(branch, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            branch = Branch.objects.get(id=id)
            branch.delete()
            return Response({'message': 'object deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)


class MyReferenceList(generics.ListCreateAPIView):
    queryset = Reference.objects.all()
    serializer_class = MyReferenceSerializers


class MyReferenceGetList(APIView):
    def get(self, request, id):
        try:
            reference = Reference.objects.get(id=id)
            serializer = MyReferenceSerializers(reference)
            return Response(serializer.data)
        except Reference.DoesNotExist:
            return Response({'error': 'Reference does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = MyReferenceSerializers

    def put(self, request, id):
        try:
            reference = Reference.objects.get(id=id)
            serializer = MyReferenceSerializers(reference, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Reference.DoesNotExist:
            return Response({'error': 'Reference not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            reference = Reference.objects.get(id=id)
            reference.delete()
            return Response({'message': 'Object deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Reference.DoesNotExist:
            return Response({'error': 'Response Not found'}, status=status.HTTP_404_NOT_FOUND)


class MyTaxList(generics.ListCreateAPIView):
    queryset = Tax.objects.all()
    serializer_class = MyTaxSerializers


class MyTaxGetList(APIView):
    def get(self, request, id):
        try:
            tax = Tax.objects.get(id=id)
            serializer = MyTaxSerializers(tax)
            return Response(serializer.data)
        except Tax.DoesNotExist:
            return Response({'error': 'Tax not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = MyTaxSerializers

    def put(self, request, id):
        try:
            tax = Tax.objects.get(id=id)
            serializer = MyTaxSerializers(tax, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Tax.DoesNotExist:
            return Response({'error': 'Tax not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            tax = Tax.objects.get(id=id)
            tax.delete()
            return Response({'message': 'Object deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Tax.DoesNotExist:
            return Response({'error': 'Tax not found'}, status=status.HTTP_404_NOT_FOUND)


class MyCarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = MyCarSerializers


class MyCarGetList(APIView):
    def get(self, request, id):
        try:
            car = Car.objects.get(id=id)
            serializer = MyCarSerializers(car)
            return Response(serializer.data)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = MyCarSerializers

    def put(self, request, id):
        try:
            car = Car.objects.get(id=id)
            serializer = MyCarSerializers(car, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            car = Car.objects.get(id=id)
            car.delete()
            return Response({'message': 'Object deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)


class MyCouponList(generics.ListCreateAPIView):
    queryset = CouponList.objects.all()
    serializer_class = MyCouponSerializers


class MyCouponGetList(APIView):
    def get(self, request, id):
        try:
            coupon = CouponList.objects.get(id=id)
            serializer = MyCouponSerializers(coupon)
            return Response(serializer.data)
        except CouponList.DoesNotExist:
            return Response({'error': 'Coupon not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = MyCouponSerializers

    def put(self, request, id):
        try:
            coupon = CouponList.objects.get(id=id)
            serializer = MyCouponSerializers(coupon, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CouponList.DoesNotExist:
            return Response({'error': 'Coupon not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            coupon = CouponList.objects.get(id=id)
            coupon.delete()
            return Response({'message': 'Object deleted'}, status=status.HTTP_204_NO_CONTENT)
        except CouponList.DoesNotExist:
            return Response({'error': 'Coupon not found'}, status=status.HTTP_404_NOT_FOUND)


class MySubscriptionList(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = MySubscriptionSerializers


class MySubscriptionGetList(APIView):
    def get(self, request, id):
        try:
            subscription = Subscription.objects.get(id=id)
            serializer = MySubscriptionSerializers(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = MySubscriptionSerializers

    def put(self, request, id):
        try:
            subscription = Subscription.objects.get(id=id)
            serializer = MySubscriptionSerializers(subscription, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CouponList.DoesNotExist:
            return Response({'error': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            subscription = Subscription.objects.get(id=id)
            subscription.delete()
            return Response({'message': 'Object deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)


class Regionapi(APIView):
    def post(self, request):
        data= request.data
        region_seri=  Regionserializer(data=data)
        if region_seri.is_valid():
            region_seri.save()
            return Response({'msg':'Region is added', 'data':region_seri.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'Region is not added', 'data':region_seri.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        all_regions= region.objects.all()
        serializer =  Regionserializer(all_regions, many=True)
        return Response({'msg':'All Region List', 'data':serializer.data}, status=status.HTTP_200_OK)


#Charges API endpoint
class twohrscharges(APIView):
    """2HRS driver service charges"""
    def get(self, request):
        try:
            _2hrs =localtwohrscharges.objects.all()
            serializer = chargestwohrsserailizer(_2hrs, many=True)
            return Response({"msg":"Local 2hrs charges","data":serializer.data}, status=status.HTTP_200_OK)
        except chargestwohrsserailizer.DoesNotExist:
            return Response({'error': 'Data does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class fourhrscharges(APIView):
    """4HRS driver service charges"""
    def get(self, request):
        try:
            fourhrs =localfourhrscharges.objects.all()
            serializer = localfourhrschargesSerializer(fourhrs, many=True)
            return Response({"msg":"Local 4hrs charges","data":serializer.data}, status=status.HTTP_200_OK)
        except chargestwohrsserailizer.DoesNotExist:
            return Response({'error': 'Data does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

""""Get location based on city query parameter"""
class locatiobycity(APIView):
    def get(self, request):
        pass
