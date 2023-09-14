from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
from driver_management.models import AddDriver, Driverlocation
from driver_management.serializers import *
from authentication.models import  User
from firebase_admin import messaging
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db.models import F
from django.http import JsonResponse

# from geopy.geocoders import Nominatim
# import geocoder

from math import sin, radians, cos, sqrt, atan2


class userregistration(APIView):
    def post(self, request):
        data=request.data

        serializer=ClientregistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response({'msg': 'user is created'}, status=status.HTTP_201_CREATED)
        
        else:
            return Response({'msg': 'user not created'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        user = bookinguser.objects.all().order_by('full_name').reverse()
        serializer = ClientregistrationSerializer(user, many=True)
        return Response(serializer.data)
    

class Userlogin(APIView):
    def post(self, request):
        full_name=request.data['full_name']
        mobile_number=request.data['mobile_number']
        
      
        if bookinguser.objects.filter(full_name=full_name, mobile_number=mobile_number).exists():
            return Response ({
                'msg':'user can book driver',
                'status':status.HTTP_200_OK
            })
        else:
              return Response ({
                'msg':'user not login for book driver',
                'status':status.HTTP_400_BAD_REQUEST
            })
        

class MyBookingList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, format=None): 
        user=request.user
        data=request.data
        serializer=PlacebookingSerializer(data=data)
        
        if serializer.is_valid():
                currant_location = serializer.validated_data.get('currant_location')
                driver_type=serializer.validated_data.get('driver_type')
                car_type= serializer.validated_data.get('car_type')
                transmission_type=serializer.validated_data.get('transmission_type')
    
                driver=AddDriver.objects.filter(driver_type=driver_type, car_type=car_type, transmission_type=transmission_type)

                if currant_location:
                    # currant_location = obj.currant_location or None
                    if currant_location is None:
                        return JsonResponse({'error': 'Current location is missing.'}, status=status.HTTP_400_BAD_REQUEST)
                    driver =Driverlocation.objects.all().annotate(
                            distance = Distance('driverlocation', currant_location)
                            ).filter(distance__lte=D(km=3))
                    
                driver_data = []
                for driver_obj in driver:
                    driver_location = driver_obj.driverlocation
                    if driver_location:
                        location_dict = {
                            "id": driver_obj.id,
                            "longitude": driver_location.x,
                            "latitude": driver_location.y,
                        }
                        driver_data.append(location_dict)                

                if driver.exists():
                     # Send notification using FCM
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title="New Booking",
                            body="A new booking is available!"
                        ),
                        topic="Driver_Booking"  # Replace with the appropriate FCM topic
                    )

                    # Send the message
                    response = messaging.send(message)
                    print("Notification sent:", response) 

<<<<<<< HEAD
                    # Save Booking
                    if PlaceBooking.status == 'accept':
                        accepted=AddDriver.objects.get(id=id)
                        return Response({'msg':'Booking accepted', 'driver':accepted})
=======
>>>>>>> 425542cd1856126e520ba227d59d16bc1ec1c031
                    

                

                serializer.validated_data['user_id'] = user.id
                serializer.save()

                # Check if the driver has accepted the booking
                driver_id = driver[0].id
                booking = PlaceBooking.objects.create(
                    currant_location=currant_location,
                    # accepted_driver= accepted_drive_id,
                    user_id=user.id,
                )
                booking.status = 'pending'
                booking.save()

                # If the driver has accepted the booking, save the booking in the database with the driver's name
                if booking.status == 'accept':
                    booking.driver_name = driver[0].name
                    booking.save()

                # Save Booking
                # if PlaceBooking.status == 'accept':
                #     return Response({'msg':'Booking accepted'})
                return Response({'data':serializer.data,"drivers":driver_data}, status=status.HTTP_201_CREATED)
                        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user = request.user.id
        booking=PlaceBooking.objects.all().order_by('id')
        serializer = PlacebookingSerializer(booking, many=True)
        
        return Response(serializer.data)
    

class BookingListWithId(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request, id):
        user= request.user
        booking = PlaceBooking.objects.get(id=id)
        serializer = PlacebookingSerializer(booking)
        return Response(serializer.data)
    
    serializer_class = PlacebookingSerializer

    def put(self, request, id):
        booking = PlaceBooking.objects.get(id=id)
        serializer = PlacebookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
       
      


class SearchDriverWithinRadius(APIView):
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        radius = 6371  # Earth's radius in kilometers
        distance = radius * c

        return distance

    def get(self, request):
        client_latitude = request.query_params.get('client_latitude')
        client_longitude = request.query_params.get('client_longitude')
        if not client_latitude or not client_longitude:
            return Response([])

        client_latitude = float(client_latitude)
        client_longitude = float(client_longitude)

        # Filter drivers within 3 km from the client location.
        drivers = AddDriver.objects.all()
        filtered_drivers = []

        for driver in drivers:
            distance = self.haversine_distance(
                client_latitude, client_longitude, driver.latitude, driver.longitude
            )
            if distance <= 3:
                filtered_drivers.append(driver)

        serializer = DriverSerializer(filtered_drivers, many=True)
        return Response(serializer.data)
    

class InvoiceGenerate(APIView):
    def post(self, request):
        data = request.data
        user = request.user
        inv_seri =  InvoiceSerializer(data = data)
        if inv_seri.is_valid():
            inv_seri.validated_data['user_id'] = user.id
            inv_seri.save()
            return Response({'msg': 'invice is generate', 'data':inv_seri.data}, status=status.HTTP_201_CREATED)
        else:
             return Response({'msg': 'Unable to generate', 'data':inv_seri.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def get(self, request):
        try:
            get_all_inv = Invoice.objects.all().order_by('invoice_generate')
            get_seri= InvoiceSerializer(get_all_inv, many=True)
            return Response({'msg': 'All invoice list', 'data':get_seri.data}, status=status.HTTP_200_OK)
        
        except Invoice.DoesNotExist:
            raise serializers.ValidationError("No Data Found")
  
        
class FeedbackApi(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        data = request.data
        FeedBack_seri= Feedbackserializer(data=data)
        if FeedBack_seri.is_valid():
            FeedBack_seri.save()
            return Response({'msg': 'Thanks for the feedback', 'data':FeedBack_seri.data}, status=status.HTTP_201_CREATED)
        else:
             return Response({'msg': 'Unable to generate', 'data':FeedBack_seri.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        get_feedback = Feedback.objects.all()
        serializer = Feedbackserializer(get_feedback, many=True)
        return Response({'msg': 'All feedback list', 'data':serializer.data}, status=status.HTTP_201_CREATED)


class userprofile(APIView):  
    def post(self, request):
        user=request.user
        serializer= Profileserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Profile is update', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'unable to update', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:
            user = request.user
            allprofile = Profile.objects.all()
            pro_seri =Profileserializer(allprofile, many=True)
            return Response({'msg': 'All Profile List', 'data':pro_seri.data}, status=status.HTTP_200_OK)
        
        except Profile.DoesNotExist:
            return Response({'msg':'No Profile avalaible', 'data':pro_seri.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)