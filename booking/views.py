from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
from driver_management.models import AddDriver
from driver_management.serializers import *
from authentication.models import  User
from firebase_admin import messaging
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.http import JsonResponse
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
 
# from geopy.geocoders import Nominatim
# import geocoder


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

                 
                if car_type is None :    
                    driver=AddDriver.objects.filter(driver_type=driver_type, car_type=car_type, transmission_type=transmission_type)

                elif currant_location:
                    if currant_location is None:
                        return JsonResponse({'error': 'Current location is missing.'}, status=status.HTTP_400_BAD_REQUEST)
                    driver =AddDriver.objects.all()
                    if driver:
                        driver = driver.filter(car_type=car_type, driver_type="Part Time", transmission_type=transmission_type)
                        print("Driver Details",driver)
                    
                    
                    driver=driver.annotate(
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

                #for booking accept 
                if PlaceBooking.status == "accept":
                    return Response({'msg':'booking is accepted'})
                
                #for booking decline 
                elif PlaceBooking.status == "decline":
                    return Response({'msg':'booking is decline'})
                
                serializer.validated_data['user_id'] = user.id
                serializer.save(status="accept")

                return Response({'data':serializer.data,"drivers":driver_data}, status=status.HTTP_201_CREATED)
                        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user = request.user.id
        booking=PlaceBooking.objects.all().order_by('id')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(booking, request)
        serializer = PlacebookingSerializer(page, many=True)
        
        return paginator.get_paginated_response(serializer.data)


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
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        data = request.data
        FeedBack_seri= Feedbackserializer(data=data)
        if FeedBack_seri.is_valid():
            FeedBack_seri.save()
            return Response({'msg': 'Thanks for the feedback', 'data':FeedBack_seri.data}, status=status.HTTP_201_CREATED)
        else:
             return Response({'msg': 'Unable to generate', 'data':FeedBack_seri.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        get_feedback = Feedback.objects.all()
        serializer = Feedbackserializer(get_feedback, many=True)
        return Response({'msg': 'All feedback list', 'data':serializer.data}, status=status.HTTP_201_CREATED)


class userprofile(APIView):  
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
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


class UserProfileWithId(APIView):
    def get(self, request, id):
        try:
            user = Profile.objects.get(id=id)
            serializer = Profileserializer(user)
            return Response(serializer.data)

        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class PendingBooking(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data=request.data
            user=request.user
            booking_status= request.GET.get('booking_status')
            print("booking status", booking_status)

            #Fetching pending records
            if booking_status is not None:
                pending_booking=PlaceBooking.objects.filter(status=booking_status)
                number_of_booking= pending_booking.count()
                
                serializer = PlacebookingSerializer(pending_booking, many=True)
                return Response({'msg':'Your bookings', 'data':serializer.data}, status=status.HTTP_200_OK)
            else:
                bookings = PlaceBooking.objects.all()

                serializer = PlacebookingSerializer(bookings, many=True)
                return Response({'msg':'No Data found', 'data':serializer.data, 'number_of_booking':number_of_booking.data}, status=status.HTTP_200_OK)
        
        except PlaceBooking.DoesNotExist:
            return Response({'msg':'No Data found', 'data':serializer.data})


class UpcomingBooking(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user=request.user
            current_datetime = datetime.now()


            upcoming_booking=PlaceBooking.objects.filter(booking_time__lt=current_datetime)
            result = upcoming_booking.order_by('booking_time').first()
                
            if result is not None:
                serializer = PlacebookingSerializer(result)
                return Response({'msg':'Upcoming bookings', 'data':serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No upcoming bookings'}, status=status.HTTP_200_OK)
    
        except PlaceBooking.DoesNotExist:
            return Response({'msg':'No Data found', 'data':serializer.data})
