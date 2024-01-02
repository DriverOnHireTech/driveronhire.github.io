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
from datetime import datetime, timedelta, time, timezone
from rest_framework.pagination import PageNumberPagination
from fcm_django.models import FCMDevice
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination
from driver_management.paginations import cutomepegination
from authentication import utils
from geopy import Nominatim
from .send_otp import send_sms
from user_master.models import ZoneA, ZoneB
from .zone_logic import zone_get, return_charges

 
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

        pickup_zone = zone_get(pickup_location)
        drop_zone = zone_get(drop_location)
        print("pick up zone: ",pickup_zone)
        print("drop zone: ",drop_zone)

        extra_charges = return_charges(pickup_zone, drop_zone)
        print("Extra charge: ", extra_charges)

        serializer=PlacebookingSerializer(data=data)
        
        if serializer.is_valid():
                car_type= serializer.validated_data.get('car_type')
                transmission_type=serializer.validated_data.get('gear_type')
                serializer.validated_data['mobile'] = user.phone

                # Converting Current location latitude and longitude to user address using geopy
                currant_location = serializer.validated_data.get('currant_location')
                print("current location: ", currant_location)
                print("Type of current location: ", type(currant_location))
                currant_location_str = str(currant_location)
                coordinates_str = currant_location_str.split("(")[1].split(")")[0]
                latitude, longitude = map(float, coordinates_str.split())

                def get_address(latitude, longitude):
                    """ Function for getting address using latitude and longitude"""
                    geolocator = Nominatim(user_agent="MyGeocodingApp") 
                    location = geolocator.reverse((latitude, longitude), language="en")
                    return location.address if location else "Location not found"

                address = get_address(latitude, longitude)
                serializer.validated_data['user_address'] = address # saving address in user address

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
                                new_driver.has_received_notification = True
                                driver_id.append(new_driver.driver_user)
                                
                                #Saving driver name whos received notification
                                

                        devices = FCMDevice.objects.filter(user__in=driver_id)

                        serializer.validated_data['user'] = user
                        serializer.save()
                        booking_id = serializer.data['id']
                        print("Serializer id: ",serializer.data['id'])
                        
                        notify=Notifydrivers.objects.create()
                        notify.place_booking = PlaceBooking.objects.get(id=booking_id)
                        notify.save()
                        bookingId=PlaceBooking.objects.get(id=booking_id)
                        notify.driver.set(driver)

                        registration_ids = []
                        for device in devices:
                            registration_id = device.registration_id
                            registration_ids.append(registration_id)

                        # Send notification using FCM
                        for token in registration_ids:
                            if token is None or not token.strip():
                                print("Invalid token")
                                continue

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
                            except Exception as e:
                                print(f"Error sending notification to token {token}:{e}")
                    

                return Response({'data':serializer.data, 'drivers':driver_data}, status=status.HTTP_201_CREATED)
                        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def get(self, request):
        user = request.user
        xyz = AddDriver.objects.filter(driver_user=user)
        driver_ids = [driver.id for driver in xyz]

        # Check if the user is a notified driver
        try:
            is_notified_driver = Notifydrivers.objects.filter(driver=driver_ids[0]).exists()
            notify_driver_data = Notifydrivers.objects.filter(driver=driver_ids[0])
           
            if is_notified_driver:
                data_list = []
                for booking_idd in notify_driver_data:
                    booking = PlaceBooking.objects.filter(Q(id=booking_idd.place_booking.id) & Q(status="pending"))
                    serializer = PlacebookingSerializer(booking, many=True)
                    
                    data_list.extend(serializer.data)
                    
                    
                revers_recors= data_list[::-1]

                return Response({'data':revers_recors}, status=status.HTTP_200_OK)
            
            
            else:
                return Response({'error': 'Access forbidden. You are not a notified driver.'}, status=status.HTTP_403_FORBIDDEN)
            
        except:
            return Response({'error': 'You dont have any booking data.'}, status=status.HTTP_403_FORBIDDEN)


"""Endpoint for web CRM"""
class getbooking(APIView):
    def get(self, request):
        try:
            booking_data= PlaceBooking.objects.all().order_by('-id')
            serializer=PlacebookingSerializer(booking_data, many=True)
            return Response({'msg':'All booking', 'data':serializer.data}, status=status.HTTP_200_OK)
        except PlaceBooking.DoesNotExist:
            return Response({'msg':'No booking found'}, status=status.HTTP_204_NO_CONTENT)

"""End endpoint"""

class Acceptedride(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        data = request.data
        user = request.user
        booking= PlaceBooking.objects.get(id=id)
        client_name=booking.user
        mobile=booking.mobile
        driver=booking.accepted_driver
        date=booking.booking_date
        if booking.status == "accept":
                return Response({'msg': 'booking already accepted by other driver'})
        
        elif booking.status == "pending":
            serializer= PlacebookingSerializer(booking, data=data, partial=True)
            booking.accepted_driver= user
            if serializer.is_valid():
                
                accepted_driver = booking.accepted_driver
                # driver_name = AddDriver.objects.get(driver_user=7654002162)
                whatsapp_number = f"whatsapp:+91{mobile}"
                msg="""Dear {client_name}

                                Mr. {driver}
                                Mobile - {driver}
                                Will be arriving at your destination.

                                Date -{date}
                                Time -

                                Our rates - https://www.driveronhire.com/rates

                                *T&C Apply
                                https://www.driveronhire.com/privacy-policy

                                Thanks 
                                Driveronhire.com
                                Any issue or feedback call us 02243439090"""
                message=msg.format(client_name=client_name, driver=driver, dname=driver,date=date)
                data.setdefault("accepted_driver",user.id)
                utils.twilio_whatsapp(to_number=whatsapp_number, message=message)
                serializer.save()
                return Response({'msg':'bookking Updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
      
        else:
            return Response({'msg':'Not Accpeted', 'error':serializer.errors})
        return Response({'msg': 'No booking to accept'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class startjourny(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        data = request.data
        user = request.user
        currenttime=datetime.now()
        start_deuty=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        booking= PlaceBooking.objects.get(id=id)
        if booking.deuty_started:
            return Response({'msg': 'Duty has already started', 'data': None}, status=status.HTTP_400_BAD_REQUEST)

        serializer=PlacebookingSerializer(booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['deuty_started']=start_deuty
            serializer.save()
            return Response({'msg':'Deuty Started', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg':'Deuty Not Started', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
#finish deuty
class endjourny(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        data = request.data
        user = request.user
        currenttime=datetime.now()
        end_deuty=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        booking= PlaceBooking.objects.get(id=id)
        if booking.deuty_end:
            return Response({'msg': 'Duty has already Ended', 'data': None}, status=status.HTTP_400_BAD_REQUEST)

        serializer=PlacebookingSerializer(booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['deuty_end']=end_deuty
            serializer.save()
            return Response({'msg':'Deuty Ended', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg':'Deuty Not Ended', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 


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

            if driver.exists():
                devices = FCMDevice.objects.all()
                print("Device data: ", devices)

                registration_ids = []
                for device in devices:
                    registration_id = device.registration_id
                    registration_ids.append(registration_id)

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
        driver_id= data['driver']
        placebooking_id = data['placebooking']
        print("placebooking id", placebooking_id)
        Placebooking_data = PlaceBooking.objects.values().get(id=placebooking_id)
        booking_type = Placebooking_data['booking_type']
        print("booking type: ", booking_type)
        print("Place booking data: ", Placebooking_data)
        user = request.user

        if booking_type == "local":
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_end_datetime = Placebooking_data.get('deuty_end')

            # Convert deuty_started to a datetime object with timezone information
            deuty_started_datetime = datetime.combine(datetime.today(), deuty_started_time, tzinfo=timezone.utc)

            # Make sure deuty_end_datetime has timezone information (if not already)
            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)

            # Calculate the time difference
            time_difference = deuty_end_datetime - deuty_started_datetime

            # Printing the time difference
            print("Time Difference:", time_difference)
            

        if booking_type == "outstation":
            print("outstation booking")
            

        if booking_type == "outstation_drop":
            print("Outstation drop booking")
            

        inv_seri =  InvoiceSerializer(data = data)
        if inv_seri.is_valid():
            # inv_seri.validated_data['user_id'] = user.id
            # print("data: ", data)
            # inv_seri.save()
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

            #Fetching pending records
            if booking_status is not None:
                pending_booking=PlaceBooking.objects.filter(status=booking_status, accepted_driver=user.id).order_by('-id')
                number_of_booking= pending_booking.count()
                
                serializer = PlacebookingSerializer(pending_booking, many=True)
                
                return Response({'msg':'Your bookings', 'data':serializer.data, 'numbe_of_booking':number_of_booking}, status=status.HTTP_200_OK)
            else:
                bookings = PlaceBooking.objects.all()

                serializer = PlacebookingSerializer(bookings, many=True)
                return Response({'msg':'Data found', 'data':serializer.data}, status=status.HTTP_200_OK)
        
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

       # Extracting latitude and longitude from Point field data
        coordinates = data['client_location']['coordinates']
        longitude, latitude = coordinates  # Note: order is (longitude, latitude)
      

        car_type=data['car_type']
        booking_for = request.data['bookingfor']
        trip_type=request.data['trip_type']
        mobile_number=request.data['mobile_number']
        # message_number = f"+91{mobile_number}"
        whatsapp_number = f"whatsapp:+91{mobile_number}"
        bookingfor=request.data['bookingfor']

        # if AgentBooking.objects.filter(id=id).exists():
        serializer= Agentbookingserailizer(data=data)
        if serializer.is_valid():
            serializer.validated_data['booking_created_by_name']=user.first_name
            serializer.save()

            user_location_point = Point(latitude, longitude, srid=4326)

            message = f"Hello, {client_name},. You have booked a driver for your {car_type} car, and the reservation is for an {booking_for} trip with a {trip_type}"
            #message='This is test message.'
            # print(message)
            # utils.twilio_message(to_number=message_number, message=message)
            utils.twilio_whatsapp(to_number=whatsapp_number, message=message)
            # serializer.save()
            driver =AddDriver.objects.all()
            if driver:
                driver = driver.filter(car_type__contains=car_type)

            driver=driver.annotate(
                        distance = Distance('driverlocation', user_location_point)
                            ).filter(distance__lte=D(km=5))
            
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
                            new_driver.has_received_notification = True
                            driver_id.append(new_driver.driver_user)
                
                devices = FCMDevice.objects.filter(user__in=driver_id)
                #serializer.validated_data['user_id'] = user
                
                booking_id = serializer.data.get('id')
               
                notify=NotifydriversAgent.objects.create()
                notify.agent_booking = AgentBooking.objects.get(id=booking_id)
                notify.save()
                notify.driver.set(driver)
                registration_ids = []
                for device in devices:
                    registration_id = device.registration_id
                    registration_ids.append(registration_id)
                    
                # Send notification using FCM
                for token in registration_ids:
                    if token is None or not token.strip():
                        print("Invalid token")
                        continue
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title="New Booking",
                            body=f"Trip Type:{booking_for}\n Car Type:{car_type}",
                            
                        ),
                        token= token 
                    )
                        # Send the message
                    try:

                        response = messaging.send(message)
                        print("Notification sent:", response) 
                    except Exception as e:
                        print(f"Error sending notification to token {token}:{e}")
            # serializer.save()
            

            # serializer.save()
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
                clinet_data=AgentBooking.objects.filter(Q(mobile_number=mobile_number) | Q(client_name=client_name)).order_by('-id')
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


class AgentBookingApp(APIView):
    """This class is for making get request for mobile app"""
    def get(self, request):
        user = request.user
        xyz = AddDriver.objects.filter(driver_user=user)
        driver_ids = [driver.id for driver in xyz]

        # Check if the user is a notified driver
        try:
            is_notified_driver = NotifydriversAgent.objects.filter(driver=driver_ids[0]).exists()
            notify_driver_data = NotifydriversAgent.objects.filter(driver=driver_ids[0])
           
            if is_notified_driver:
                data_list = []
                for booking_idd in notify_driver_data:
                    booking = AgentBooking.objects.filter(Q(id=booking_idd.agent_booking.id))
                    serializer = Agentbookingserailizer(booking, many=True)
                    data_list.extend(serializer.data)                    
                revers_recors= data_list[::-1]

                return Response({'data':revers_recors}, status=status.HTTP_200_OK)
            
            
            else:
                return Response({'error': 'Access forbidden. You are not a notified driver.'}, status=status.HTTP_403_FORBIDDEN)
            
        except:
            return Response({'error': 'You dont have any booking data.'}, status=status.HTTP_403_FORBIDDEN)



#Get booking by status
class Agentbooking_bystatus(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            data=request.data
            user=request.user
            booking_status= request.GET.get('booking_status')

            #Fetching pending records
            if booking_status is not None:
                pending_booking=AgentBooking.objects.filter(status=booking_status)
                number_of_booking= pending_booking.count()
                
                serializer =Agentbookingserailizer(pending_booking, many=True)
                
                return Response({'msg':'Your bookings', 'data':serializer.data}, status=status.HTTP_200_OK)
            else:
                bookings = AgentBooking.objects.all()

                serializer = Agentbookingserailizer(bookings, many=True)
                return Response({'msg':'No Data found', 'data':serializer.data, 'number_of_booking':number_of_booking.data}, status=status.HTTP_200_OK)
        
        except AgentBooking.DoesNotExist:
            return Response({'msg':'No Data found', 'data':serializer.data}, status=status.HTTP_204_NO_CONTENT)
    

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


class Agentstartjourny(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        data = request.data
        user = request.user
        currenttime=datetime.now()
        start_deuty=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        booking= AgentBooking.objects.get(id=id)
        if booking.deuty_started:
            return Response({'msg': 'Duty has already started', 'data': None}, status=status.HTTP_400_BAD_REQUEST)

        serializer=Agentbookingserailizer(booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['deuty_started']=start_deuty
            serializer.save()
            return Response({'msg':'Deuty Started', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg':'Deuty Not Started', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Agentendjourny(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        data = request.data
        user = request.user
        currenttime=datetime.now()
        end_deuty=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        booking= AgentBooking.objects.get(id=id)
        if booking.deuty_end:
            return Response({'msg': 'Duty has already Ended', 'data': None}, status=status.HTTP_400_BAD_REQUEST)

        serializer=Agentbookingserailizer(booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['deuty_end']=end_deuty
            serializer.save()
            return Response({'msg':'Deuty Ended', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg':'Deuty Not Ended', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 


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
        
"""Guest Booking API endpoint"""
class Guestbookingapi(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            data=request.data
            user=request.user
            serializer=GuestBookingserialzer(data=data)
            if serializer.is_valid():
                serializer.validated_data['user']=user
                serializer.save()
                return Response({'msg':'Guest Booking done', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        except:
            # serializer=GuestBookingserialzer()
            return Response({'msg':'Unable to save'}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:
            guestbooking=GuestBooking.objects.all()
            serializer=GuestBookingserialzer(guestbooking, many=True)
            return Response({'msg':'All guest booking', 'data':serializer.data}, status=status.HTTP_200_OK)

        except:
            return Response({'msg': 'Error getting data'})
            

class SingleGuestbookingapi(APIView):
    def get(self, request,id):
        try:
            guestbooking=GuestBooking.objects.get(id=id)
            serializer=GuestBookingserialzer(guestbooking)
            return Response({'msg':'guest booking', 'data':serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'Data doesnot exist'})


class AllZoneData(APIView):
    def get(self, request):
        zone_a_data = ZoneA.objects.all()
        zone_b_data = ZoneB.objects.all()
        zone_c_data = ZoneC.objects.all()
        zone_d_data = ZoneD.objects.all()
        zone_e_data = ZoneE.objects.all()
        zone_f_data = ZoneF.objects.all()
        zone_g_data = ZoneG.objects.all()

        zone_a_serializer = ZoneASerializer(zone_a_data, many=True)
        zone_b_serializer = ZoneBSerializer(zone_b_data, many=True)
        zone_c_serializer = ZoneCSerializer(zone_c_data, many=True)
        zone_d_serializer = ZoneDSerializer(zone_d_data, many=True)
        zone_e_serializer = ZoneESerializer(zone_e_data, many=True)
        zone_f_serializer = ZoneFSerializer(zone_f_data, many=True)
        zone_g_serializer = ZoneGSerializer(zone_g_data, many=True)

        combined_data = zone_a_serializer.data + zone_b_serializer.data + zone_c_serializer.data + zone_d_serializer.data + zone_e_serializer.data + zone_f_serializer.data + zone_g_serializer.data
        sorted_data = sorted(combined_data, key=lambda x: x['location'])

        return Response(sorted_data)
