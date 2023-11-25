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
from authentication import utils
 
# from geopy.geocoders import Nominatim
# import geocoder
from datetime import datetime, date


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
                             ).filter(distance__lte=D(km=5)) # Radius will be changed to 5 km while deployment
                    
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
                                print("Notification received: ",new_driver.has_received_notification)
                                new_driver.has_received_notification = True
                                driver_id.append(new_driver.driver_user)
                                
                                #Saving driver name whos received notification
                                

                        devices = FCMDevice.objects.filter(user__in=driver_id)

                        serializer.validated_data['user_id'] = user.id
                        serializer.save()
                        booking_id = serializer.data['id']
                        print("Serializer id: ",serializer.data['id'])
                        
                        notify=Notifydrivers.objects.create()
                        notify.place_booking = PlaceBooking.objects.get(id=booking_id)
                        notify.save()
                        print("notify place booking:", notify.place_booking)
                        print("placebooking data", PlaceBooking.objects.get(id=booking_id))
                        notify.driver.set(driver)
                        print("Notify: ",notify) 

                        registration_ids = []
                        for device in devices:
                            registration_id = device.registration_id
                            registration_ids.append(registration_id)
                        
                        print("registration id:", registration_ids)

                        # Send notification using FCM
                        for token in registration_ids:
                            if token is None or not token.strip():
                                print("Invalid token")
                                continue

                            print("Token value", token)

                            message = messaging.Message(
                                notification=messaging.Notification(
                                    title="New Booking",
                                    body=f"Trip Type:{trip_type}\n Car Type:{car_type}\n Gear Type:{gear_type}\nPickup Location:{pickup_location}\nDrop Location{drop_location}"
                                ),
                                token= token 
                            )
                            # Send the message
                            try:

                                response = messaging.send(message)
                                print("Notification sent:", response) 
                            except Exception as e:
                                print(f"Error sending notification to token {token}:{e}")
                    

                return Response({'data':serializer.data, 'drivers':driver_data}, status=status.HTTP_201_CREATED)
                        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def get(self, request):
        user = request.user
        print("User data: ",user)
        print(user.phone)
        xyz = AddDriver.objects.filter(driver_user=user)
        driver_ids = [driver.id for driver in xyz]
        print("adddriver details:", driver_ids)

        # Check if the user is a notified driver
        try:
            is_notified_driver = Notifydrivers.objects.filter(driver=driver_ids[0]).exists()
            notify_driver_data = Notifydrivers.objects.filter(driver=driver_ids[0])
           
            if is_notified_driver:
                data_list = []
                for booking_idd in notify_driver_data:
                    
                    booking = PlaceBooking.objects.filter(Q(id=booking_idd.place_booking.id) & Q(status="pending"))
                    
                    serializer = PlacebookingSerializer(booking, many=True)
                    
                    data_list.append(serializer.data)
                    
                revers_recors= data_list.reverse()

                return Response({'data ':data_list}, status=status.HTTP_200_OK)
            
            
            else:
                return Response({'error': 'Access forbidden. You are not a notified driver.'}, status=status.HTTP_403_FORBIDDEN)
            
        except:
            return Response({'error': 'You dont have any booking data.'}, status=status.HTTP_403_FORBIDDEN)


class Acceptedride(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        data = request.data
        user = request.user
        booking= PlaceBooking.objects.get(id=id)

        if booking.status == "accept":
                return Response({'msg': 'booking already accepted by other driver'})
        
        elif booking.status == "pending":
            serializer= PlacebookingSerializer(booking, data=data, partial=True)
            booking.accepted_driver= user
            if serializer.is_valid():
                
                accepted_driver = booking.accepted_driver
                # driver_name = AddDriver.objects.get(driver_user=7654002162)
                whatsapp_number = f"whatsapp:+919657847644"
                msg = f"your booking is accepted. Driver number is\n 7045630679"
                data.setdefault("accepted_driver",user.id)
                utils.twilio_whatsapp(self, to_number=whatsapp_number, message=msg)
                serializer.save()
                return Response({'msg':'bookking Updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
      
        else:
            return Response({'msg':'Not Accpeted', 'error':serializer.errors})
        return Response({'msg': 'No booking to accept'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
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
    """Get Logged user Booking"""
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        try:
            user= request.user
            booking = PlaceBooking.objects.filter(user=user).order_by('-id')
            serializer = PlacebookingSerializer(booking, many=True)
            return Response({"msg":"All Booking", 'data':serializer.data},status=status.HTTP_200_OK)
        except PlaceBooking.DoesNotExist:
            return Response({'msg':'No Data Fount'}, status=status.HTTP_204_NO_CONTENT)
        
    """End Get user booking"""

    def put(self, request, id):
        user = request.user
        booking = PlaceBooking.objects.get(id=id)
        serializer = PlacebookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['user_id'] = user.id
            serializer.save()
            return Response({'msg': "Booking Update", 'data':serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class get_bookingbyid(APIView):
    def get(self, request, id):
        try:
            get_booking= PlaceBooking.objects.get(id=id)
            serializer=PlacebookingSerializer(get_booking)
            return Response({'msg':"booking by id", 'data':serializer.data}, status=status.HTTP_200_OK)
        except:
            all_booking= PlaceBooking.objects.all()
            serializer= PlacebookingSerializer(all_booking, many=True)
            return Response({'msg':"All Booking", 'data':serializer.data}, status=status.HTTP_200_OK)
        

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


class PendingBooking(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
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
        id = request.data.get('id')
        client_name = request.data['client_name']
        car_type= request.data['car_type']
        booking_for = data['bookingfor']
        # email=[request.data['email']]
        mobile_number=request.data.get('mobile_number')
        message_number = f"+91{mobile_number}"
        bookingfor=request.data['bookingfor']
        if AgentBooking.objects.filter(id=id).exists:
            serializer= Agentbookingserailizer(data=data)
            if serializer.is_valid():
                serializer.validated_data['booking_created_by']=user
                # title = "Your booking details"
                message = f"Your name: {client_name}\n mobile number: {mobile_number}\n booking for: {bookingfor}"
                print(message)
                utils.twilio_message(to_number=message_number, message=message)
                print("message send")
                # mail_send= send_mail( title, message, settings.EMAIL_HOST_USER, email, fail_silently=False)

                # for sending notifiction
                driver =AddDriver.objects.all()
                if driver:
                        driver = driver.filter(car_type__contains=car_type)

                driver_id = []
                if driver.exists():
                    for new_driver in driver:
                        new_driver.has_received_notification = True
                        driver_id.append(new_driver.driver_user)
                            
                            

                    devices = FCMDevice.objects.filter(user__in=driver_id)

                    #serializer.validated_data['user_id'] = user
                    serializer.save()
                    booking_id = serializer.data['id']
                    print("Serializer id: ",serializer.data['id'])
                        
                    notify=Notifydrivers.objects.create()
                    notify.place_booking = AgentBooking.objects.get(id=booking_id)
                    notify.save()
                    print("notify place booking:", notify.place_booking)
                    print("placebooking data", PlaceBooking.objects.get(id=booking_id))
                    notify.driver.set(driver)
                    print("Notify: ",notify) 

                    registration_ids = []
                    for device in devices:
                        registration_id = device.registration_id
                        registration_ids.append(registration_id)
                        
                    print("registration id:", registration_ids)

                    # Send notification using FCM
                    for token in registration_ids:
                        if token is None or not token.strip():
                            print("Invalid token")
                            continue

                        print("Token value", token)

                        message = messaging.Message(
                            notification=messaging.Notification(
                                title="New Booking",
                                body=f"Trip Type:{booking_for}\n Car Type:{car_type}"
                            ),
                            token= token 
                        )
                            # Send the message
                        try:

                            response = messaging.send(message)
                            print("Notification sent:", response) 
                        except Exception as e:
                            print(f"Error sending notification to token {token}:{e}")

                

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


class userprofile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(sefl, request):
        user=request.user
        data=request.data
        serializer=Userprofileserializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['user']=user.id
            serializer.save()
            return Response({'msg':'Profile is created','data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'Unable to create profile', 'error':serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
