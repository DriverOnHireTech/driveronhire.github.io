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
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination
from fcm_django.models import FCMDevice
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination
from driver_management.paginations import cutomepegination
 
# from geopy.geocoders import Nominatim
# import geocoder


class MyBookingList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None): 
        user=request.user
        data=request.data
        trip_type=request.data['trip_type']
        car_type= request.data['car_type']
        gear_type=request.data['gear_type']
        pickup_location=request.data['pickup_location']
        drop_location=request.data['drop_location']

        serializer=PlacebookingSerializer(data=data)
        
        if serializer.is_valid():
                currant_location = serializer.validated_data.get('currant_location')
                # driver_type=serializer.validated_data.get('driver_type')
                car_type= serializer.validated_data.get('car_type')
                transmission_type=serializer.validated_data.get('gear_type')

                if currant_location:
                    if currant_location is None:
                        return JsonResponse({'error': 'Current location is missing.'}, status=status.HTTP_400_BAD_REQUEST)
                    driver =AddDriver.objects.all()
                    if driver:
                        driver = driver.filter(Q(car_type__contains=car_type) & Q(transmission_type__contains=transmission_type))
                    
                    driver=driver.annotate(
                            distance = Distance('driverlocation', currant_location)
                             ).filter(distance__lte=D(km=300)) # Radius will be changed to 5 km while deployment
                    
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

                    driver_id = []
                    if driver.exists():
                        for drive in driver_data:
                            add_driver = AddDriver.objects.filter(id=drive['id'])
                            for new_driver in add_driver:
                                print("Add driver id: ", new_driver.driver_user)
                                driver_id.append(new_driver.driver_user)
                        
                        devices = FCMDevice.objects.filter(user__in=driver_id)

                        registration_ids = []
                        for device in devices:
                            registration_id = device.registration_id
                            registration_ids.append(registration_id)
                        
                        print("registration id:", registration_ids)

                        # Send notification using FCM
                        for token in registration_ids:
                            print("Token value", token)
                            message = messaging.Message(
                                notification=messaging.Notification(
                                    title="New Booking",
                                    body=f"Trip Type:{trip_type}\n Car Type:{car_type}\n Gear Type:{gear_type}\nPickup Location:{pickup_location}\nDrop Location{drop_location}"
                                ),
                                token= token 
                            )
                            # Send the message
                            response = messaging.send(message)
                            print("Notification sent:", response) 
                    
                    serializer.validated_data['user_id'] = user.id
                    serializer.save()

                return Response({'data':serializer.data, 'drivers':driver_data}, status=status.HTTP_201_CREATED)
                        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def get(self, request):
        booking=PlaceBooking.objects.all().order_by('-id')
        serializer = PlacebookingSerializer(booking, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Acceptedride(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        data = request.data
        user = request.user
        print("output data:",data)
        print("User id: ", user.id)
        data.setdefault("accepted_driver",user.id)
        print("accepted driver", data['accepted_driver'])
        booking= PlaceBooking.objects.get(id=id)
        print("Booking details: ", booking.status)
        serializer= PlacebookingSerializer(booking, data=data, partial=True)
        booking.accepted_driver= user

        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'booking Updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg':'Not Accpeted', 'error':serializer.errors})

    
"""for book leter"""
class ScheduleBookingView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        current_time = datetime.now()
        booking_time = current_time + timedelta(minutes=1)
        serializer = BookLaterSerializer(data=request.data)
        if serializer.is_valid():
            car_type= serializer.validated_data.get('car_type')
            transmission_type=serializer.validated_data.get('gear_type')   
            driver=AddDriver.objects.filter( car_type=car_type, transmission_type=transmission_type).values('first_name', 'mobile')
            print("Driver Details: ", driver)

            if driver.exists():
                devices = FCMDevice.objects.all()
                print("Device data: ", devices)

                registration_ids = []
                for device in devices:
                    registration_id = device.registration_id
                    registration_ids.append(registration_id)
                print("registration id:", registration_ids)

                # Send notification using FCM
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="New Booking",
                        body="A new booking is available!"
                    ),
                    token= registration_ids[0] 
                )

                # Send the message
                response = messaging.send(message)
                print("Notification sent:", response) 

                status = serializer.validated_data.get('status')

                #for booking accept 
                if status == "accept":
                    return Response({'msg':'booking is accepted'})
                #for pending booking
                if status == "pending":
                    return Response({'msg':'booking is sent'})
                
                #for booking decline 
                elif status == "decline":
                    return Response({'msg':'booking is decline'})
                
                serializer.validated_data['user_id'] = user.id
                serializer.save()

                return Response({'data':serializer.data, 'drivers':list(driver)})
                        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""end book leter"""


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
        user = request.user
        booking = PlaceBooking.objects.get(id=id)
        serializer = PlacebookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['user_id'] = user.id
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
            return Response({'msg':'No Data found', 'data':serializer.data}, status=status.HTTP_204_NO_CONTENT)


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



# Agent can book from here

class Agentbookingview(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        data=request.data
        user=request.user
        client_name = request.data['client_name']
        email=[request.data['email']]
        mobile_number=request.data['mobile_number']
        bookingfor=request.data['bookingfor']
        serializer= Agentbookingserailizer(data=data)
        if serializer.is_valid():
            serializer.validated_data['booking_created_by']=User.objects.get(id=user.id)
            title = "Your booking details"
            message = f"Your name: {client_name}\n mobile number: {mobile_number}\n booking for: {bookingfor}"
            mail_send= send_mail( title, message, settings.EMAIL_HOST_USER, email, fail_silently=False)
            serializer.save()
            return Response({'msg':'Booking done by Agent', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
                return Response({'msg':'Booking not done', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

    pagination_class = PageNumberPagination

    def get(self, request):
        page = request.query_params.get('page', 1)

        try:

            mobile_number= request.GET.get('mobile_number')
            client_name= request.GET.get('client_name')
            if(mobile_number or client_name):
                clinet_data=AgentBooking.objects.filter(Q(mobile_number=mobile_number) | Q(client_name=client_name))
                serializer = Agentbookingserailizer(clinet_data, many=True)
                pagination = cutomepegination()
                paginated_queryset = pagination.paginate_queryset(clinet_data, request)
                serialized_data = Agentbookingserailizer(paginated_queryset, many=True)

                # Return the paginated response
                return pagination.get_paginated_response(serialized_data.data)
            else:
                alldata=AgentBooking.objects.all().order_by('-id')
                serializer = Agentbookingserailizer(alldata, many=True)
                pagination = cutomepegination()
                paginated_queryset = pagination.paginate_queryset(alldata, request)
                serialized_data = Agentbookingserailizer(paginated_queryset, many=True)

                # Return the paginated response
                return pagination.get_paginated_response(serialized_data.data)


            serializer = Agentbookingserailizer(page, many=True)
            return self.get_paginated_response({'msg': 'Customer Data', 'data': serializer.data})


            return Response({'msg': 'No Data Found'}, status=status.HTTP_204_NO_CONTENT)
            
        except AgentBooking.DoesNotExist:
            return Response({'msg':'No Data Found', 'error':serializer.errors}, status=status.HTTP_204_NO_CONTENT)
        
    
    def patch(self, request, id):
        
            agent_booking= AgentBooking.objects.get(id=id)
            serializer= Agentbookingserailizer(agent_booking, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Booking is updated', 'data':serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'Data not found', 'error':serializer.errors}, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, id):
        agentdata=AgentBooking.objects.get(id=id)
        agentdata.delete()
        return Response({'msg':'Data Delete'}, status=status.HTTP_200_OK)
    


class onoffduteyview(APIView):
    def get(self, request):
        pass

# Filter driver based on package
class driverlineupplacebooking(APIView):  
    def get(self, request):
        scheme_type= request.GET.get("scheme_type")
        
        if scheme_type:
            # Get all driver which is in scheme 
            driver= AddDriver.objects.filter(scheme_type=scheme_type).order_by('id')
            serializer=MyDriverSerializer(driver, many=True)
            
            return Response({'msg':'this is scheme driver', 'data':serializer.data})
        else:
            adddriverdata=AddDriver.objects.all()
            serializer1 = MyDriverSerializer(adddriverdata, many=True)
            return Response({'msg':'all driver list', "data":serializer1.data}, status=status.HTTP_200_OK)
     
            
class AgentDetailView(APIView):
    def get(self, request, id):
        try:
            data = AgentBooking.objects.get(id=id)
            serializer = Agentbookingserailizer(data)
            return Response({'msg': 'Data with id', 'data': serializer.data})
        except:
            return Response({'msg':'No Data Found', 'error':serializer.errors}, status=status.HTTP_204_NO_CONTENT)
