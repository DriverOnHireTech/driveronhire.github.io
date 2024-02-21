from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
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
from rest_framework.pagination import PageNumberPagination
from driver_management.paginations import cutomepegination
from authentication import utils
from geopy import Nominatim
from user_master.models import ZoneA, ZoneB
from .zone_logic import zone_get, return_charges
from client_management.models import UserProfile
from driver_management.models import AddDriver

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


        pickup_zone = zone_get(pickup_location)
        drop_zone = zone_get(drop_location)
        extra_charges = return_charges(pickup_zone, drop_zone)
        serializer=PlacebookingSerializer(data=data)
        
        if serializer.is_valid():
                car_type= serializer.validated_data.get('car_type')
                transmission_type=serializer.validated_data.get('gear_type')
                serializer.validated_data['mobile'] = user.phone
                serializer.validated_data['user']=user
                serializer.validated_data['outskirt_charge']=extra_charges

                # Converting Current location latitude and longitude to user address using geopy
                currant_location = serializer.validated_data.get('currant_location')
                currant_location_str = str(currant_location)
                coordinates_str = currant_location_str.split("(")[1].split(")")[0]
                latitude, longitude = map(float, coordinates_str.split())

                def get_address(latitude, longitude):
                    """ Function for getting address using latitude and longitude"""
                    geolocator = Nominatim(user_agent="MyGeocodingApp") 
                    location = geolocator.reverse((latitude, longitude), language="en")
                    return location.address if location else "Location not found"

                # address = get_address(latitude, longitude)
                # serializer.validated_data['user_address'] = address # saving address in user address
                

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
                    serializer.save()
                    driver_id = []
                    if driver.exists():
                        for drive in driver_data:
                            add_driver = AddDriver.objects.filter(id=drive['id'])
                            for new_driver in add_driver:
                                new_driver.has_received_notification = True
                                driver_id.append(new_driver.driver_user)
                                
                                #Saving driver name whos received notification
                                

                        devices = FCMDevice.objects.filter(user__in=driver_id)

                        
                        # serializer.save()
                        booking_id = serializer.data['id']
                        
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
                                    body=f"Trip Type:{trip_type}\n Car Type:{car_type}\n Gear Type:{gear_type}\n Pickup Location:{pickup_location}\nDrop Location:{drop_location}"
                                    
                                ),
                                token= token 
                            )
                            # Send the message
                            try:

                                response = messaging.send(message)
                            except Exception as e:
                                print(f"Error sending notification to token {token}:{e}")
                    
                # serializer.save()
                return Response({'data':serializer.data, 'drivers':driver_data}, status=status.HTTP_201_CREATED)
                        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id, format=None):
        """
        Update booking status to pending, clear driver_name and accepted_driver fields,
        and send notifications to the drivers.
        """
        try:
            booking = PlaceBooking.objects.get(id=id)
            booking.status = "pending"
            booking.accepted_driver_name = None
            booking.accepted_driver = None
            booking.accepted_driver_number = None
            booking.save()

            # Send notifications to drivers
            drivers = AddDriver.objects.filter(id__in=booking.notifydrivers_set.values_list('driver', flat=True))
            users = drivers.values_list('driver_user', flat=True)
            registration_ids = FCMDevice.objects.filter(user__in=users).values_list('registration_id', flat=True)

            for token in registration_ids:
                if token is None or not token.strip():
                    print("Invalid token")
                    continue

                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Booking Reposted",
                        body=f"Booking ID: {booking.id} is again posted."
                    ),
                    token=token
                )
                # Send the message
                try:
                    response = messaging.send(message)
                    print(response)
                except Exception as e:
                    print(f"Error sending notification to token {token}: {e}")

            return Response({'message': 'Booking updated successfully'}, status=status.HTTP_200_OK)

        except PlaceBooking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        
        if booking.status == "accept":
                return Response({'msg': 'booking already accepted by other driver'})
        
        elif booking.status == "pending":
            # Update booking status and accepted driver
            booking.status = "accept"
            booking.accepted_driver = user
            booking.save()

            # Get client information
            client_name=booking.user
            client_mobile=booking.mobile

            # Get driver information
            driver_mobile = user.phone
            driver_name = AddDriver.objects.get(driver_user=user)

            serializer= PlacebookingSerializer(booking, data=data, partial=True)
            #booking.accepted_driver= user
            if serializer.is_valid():
                serializer.validated_data['accepted_driver']=user
                serializer._validated_data['accepted_driver_name'] = user.first_name
                serializer._validated_data['accepted_driver_number'] = user.phone
                driver_name = AddDriver.objects.get(driver_user=user)
                serializer.validated_data['driver'] = driver_name
                whatsapp_number = f"91{client_mobile}"
                # msg="""Dear {client_name}

                #                 Mr. {driver_name}
                #                 Mobile - {driver_mobile}
                #                 Will be arriving at your destination.

                #                 Date -{date}
                #                 Time -{time}

                #                 Our rates - https://www.driveronhire.com/rates

                #                 *T&C Apply
                #                 https://www.driveronhire.com/privacy-policy

                #                 Thanks 
                #                 Driveronhire.com
                #                 Any issue or feedback call us 02243439090"""
                #message=msg.format(client_name="sir/Madam", driver_name=driver_name, driver_mobile=driver_mobile,date=date, time=time)
                data.setdefault("accepted_driver",user.id) 
                #utils.twilio_whatsapp(to_number=whatsapp_number, message=message)
                utils.driverdetailssent(self, whatsapp_number, driver_name, driver_mobile)
                # gupshup='https://media.smsgupshup.com/GatewayAPI/rest?userid=2000237293&password=vrgnLDKp&send_to={{whatsapp_number}}\
                #     &v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg={{msg}}'
                serializer.save()

            # Compose message
            date = booking.booking_date
            time = booking.client_booking_time
            whatsapp_number = f"whatsapp:+91{client_mobile}"
            msg="""Dear {client_name}

                            Mr. {driver_name}
                            Mobile - {driver_mobile}
                            Will be arriving at your destination.

                            Date -{date}
                            Time -{time}

                            Our rates - https://www.driveronhire.com/rates

                            *T&C Apply
                            https://www.driveronhire.com/privacy-policy

                            Thanks 
                            Driveronhire.com
                            Any issue or feedback call us 02243439090"""
            message=msg.format(client_name="sir/Madam", driver_name=driver_name, driver_mobile=driver_mobile,date=date, time=time)
            data.setdefault("accepted_driver",user.id)
            #utils.twilio_whatsapp(to_number=whatsapp_number, message=message)
            #utils.gupshupWhatsapp(self, whatsapp_number, message)
            # gupshup='https://media.smsgupshup.com/GatewayAPI/rest?userid=2000237293&password=vrgnLDKp&send_to={{whatsapp_number}}\
            #     &v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg={{msg}}'
            return Response({'msg':'bookking Updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
      
        else:
            return Response({'msg':'Not Accpeted', 'error':serializer.errors})
        return Response({'msg': 'No booking to accept'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Decline Booking by driver"""
class declineplacebooking(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        data=request.data
        user=request.user
        agentbooking_id = None
        placebooking_id = None
        placebooking = None
        agentbooking = None
        if 'placebooking' not in data and 'agentbooking' in data:
            agentbooking_id = data['agentbooking']
        elif 'placebooking' in data:
            placebooking_id = data['placebooking']

        if placebooking_id:
            try:
                placebooking = PlaceBooking.objects.get(id=placebooking_id)
            except PlaceBooking.DoesNotExist:
                return Response({'msg': 'PlaceBooking not found'}, status=status.HTTP_404_NOT_FOUND)
        if agentbooking_id:
            try:
                agentbooking = AgentBooking.objects.get(id=agentbooking_id)
            except AgentBooking.DoesNotExist:
                return Response({'msg': 'Agentbooking not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=DeclinebookingSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['placebooking']=placebooking
            serializer.validated_data['agentbooking']=agentbooking
            serializer.validated_data['refuse_driver_user']=user
            serializer.save()
            return Response({'msg':'Duty decline', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            #serializer=PlacebookingSerializer()
            return Response({'msg':'Unable to decline'}, status=status.HTTP_400_BAD_REQUEST) 

    def get(self, request):
          user=request.user
          declinebooking=Declinebooking.objects.filter(refuse_driver_user=user).order_by('-id')
          serializer=DeclinebookingSerializer(declinebooking, many=True)
          return Response({'msg':'decline booking data', 'data':serializer.data})
"""End decline"""


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
        request_type=data['request_type']
        id=data['id']
        user=request.user
        if request_type=="Normal":
            client_name =data['client_name']

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
                                body=f"Booking id:{id}\n Trip Type:{booking_for}\n Car Type:{car_type} \n Trip type:{trip_type}",
                                
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
        else:
            data=request.data
            user=request.user
            request_type=data['request_type']
            mobile_number=request.data['mobile_number']
            bookingfor = data['bookingfor']
            car_type = request.data['car_type']
            
            # checking request type
            if request_type=="Guest":
                client_info = UserProfile.objects.filter(mobile_number=mobile_number).first()
                if client_info is None:
                    return Response({'msg':'User number profile not created'}, status=status.HTTP_204_NO_CONTENT)

                fav_drivers = client_info.addfavoritedriver.all()
                if fav_drivers:
                    fav_driver_ids = list(fav_driver.id for fav_driver in fav_drivers)
                    drivers = AddDriver.objects.filter(id__in=fav_driver_ids)
                    driver_users = [driver.driver_user for driver in drivers]
                    serializer=Agentbookingserailizer(data=data)
                    if serializer.is_valid():
                        serializer.validated_data['booking_created_by_name']=user.first_name
                        serializer.save()
                        if fav_drivers.exists():
                            devices = FCMDevice.objects.filter(user__in=driver_users)
                            #serializer.validated_data['user_id'] = user
                            booking_id = serializer.data.get('id')
                        
                            notify=NotifydriversAgent.objects.create()
                            notify.agent_booking = AgentBooking.objects.get(id=booking_id)
                            notify.save()
                            notify.driver.set(fav_driver_ids)
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
                                        title="New Guest Booking",
                                        body=f"Booking for: {bookingfor}\n car type: {car_type} ",       
                                    ),
                                    token= token 
                                )
                                    # Send the message
                                try:

                                    response = messaging.send(message)
                                    print("Notification sent:", response) 
                                except Exception as e:
                                    print(f"Error sending notification to token {token}:{e}")
                    else:
                        print("No favorite drivers found for this user.")

                
                    
                    return Response({'msg':'Guest booking done', 'data':serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'msg':'Guest booking not done'}, status=status.HTTP_204_NO_CONTENT)

        
        

    pagination_class = PageNumberPagination

    def get(self, request):
        page = request.query_params.get('page', 1)

        try:
            alldata=AgentBooking.objects.filter(Q(guest_booking=False) | Q(guest_booking=True, status="active")).order_by('-id')
            number_of_booking=alldata.count()
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
        data=request.data
        user = request.user
        agent_booking= AgentBooking.objects.get(id=id)
        serializer= Agentbookingserailizer(agent_booking, data=data, partial=True)
        if serializer.is_valid():
                serializer.validated_data['booking_created_by_name'] = user.first_name
                serializer.save()
                return Response({'msg':'Booking is updated', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Data not found', 'error':serializer.errors}, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, id):
        agentdata=AgentBooking.objects.get(id=id)
        agentdata.delete()
        return Response({'msg':'Data Delete'}, status=status.HTTP_200_OK)


class AgentBookingReshedule(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, format=None):
        """
        Update booking status to pending, clear driver-related fields,
        and send notifications to the drivers.
        """
        try:
            booking = AgentBooking.objects.get(id=id)
            booking.status = "pending"
            booking_for=booking.bookingfor
            package=booking.packege
            booking.driver_name = None
            booking.accepted_driver = None
            booking.save()

            # Send notifications to drivers
            drivers = AddDriver.objects.filter(id__in=booking.notifydriversagent_set.values_list('driver', flat=True))
            users = drivers.values_list('driver_user', flat=True)
            registration_ids = FCMDevice.objects.filter(user__in=users).values_list('registration_id', flat=True)

            for token in registration_ids:
                if token is None or not token.strip():
                    print("Invalid token")
                    continue

                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Booking Updated",
                        body=f"Booking ID: {booking.id} \n Booking type:{booking_for}\n Booking package:{package}."
                    ),
                    token=token
                )
                # Send the message
                try:
                    response = messaging.send(message)
                    print(response)
                except Exception as e:
                    print(f"Error sending notification to token {token}: {e}")

            return Response({'message': 'Booking updated successfully'}, status=status.HTTP_200_OK)

        except AgentBooking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                    booking = AgentBooking.objects.filter(Q(id=booking_idd.agent_booking.id) & Q(status="pending"))
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
                pending_booking=AgentBooking.objects.filter(status=booking_status, accepted_driver=user)
                number_of_booking= pending_booking.count()
                
                serializer =Agentbookingserailizer(pending_booking, many=True)
                
                return Response({'msg':'Your bookings', 'data':serializer.data}, status=status.HTTP_200_OK)
            
            else:
                bookings = AgentBooking.objects.all()

                serializer = Agentbookingserailizer(bookings, many=True)
                return Response({'msg':'No Data found', 'data':serializer.data, 'number_of_booking':number_of_booking.data}, status=status.HTTP_200_OK)
        
        except AgentBooking.DoesNotExist:
            return Response({'msg':'No Data found', 'data':serializer.data}, status=status.HTTP_204_NO_CONTENT)
        
# For CRM quary filter
class Agentbookingfilterquary(APIView):
    def get(self, request, *args, **kwargs):
        try:
            mobile_number= request.GET.get('mobile_number')
            status=request.GET.get('status')
            bookingfor=request.GET.get('bookingfor')
            to_date=request.GET.get('to_date')
            id = request.GET.get('id')         

            if id:
                pending_booking=AgentBooking.objects.filter(id=id)
                number_of_booking= pending_booking.count()
                serializer =Agentbookingserailizer(pending_booking,many=True)
                return Response({'msg':'Your id search bookings', 'number_of_booking':number_of_booking,'data':serializer.data})
            
            elif mobile_number and status and bookingfor and to_date:
                pending_booking=AgentBooking.objects.filter(mobile_number=mobile_number, status=status, bookingfor=bookingfor, to_date=to_date)
                number_of_booking= pending_booking.count()
                
                serializer =Agentbookingserailizer(pending_booking,many=True)
                
                return Response({'msg':'Your mobile search bookings', 'number_of_booking':number_of_booking,'data':serializer.data})
            
            elif status and to_date:
                bookingstatus= AgentBooking.objects.filter(status=status, to_date=to_date)
                countstatus=bookingstatus.count()
                serializer=Agentbookingserailizer(bookingstatus, many=True)
                return Response({'msg':'Your search status bookings', 'number_of_booking':countstatus,'data':serializer.data})         
            elif bookingfor:
                pending_booking=AgentBooking.objects.filter(bookingfor=bookingfor)
                number_of_booking= pending_booking.count()
                
                serializer =Agentbookingserailizer(pending_booking, many=True)
                
                return Response({'msg':'Your search type bookings', 'number_of_booking':number_of_booking,'data':serializer.data})

            elif to_date:
                pending_booking=AgentBooking.objects.filter(to_date=to_date)
                number_of_booking= pending_booking.count()
                serializer =Agentbookingserailizer(pending_booking, many=True)
                return Response({'msg':'Your search date wise', 'number_of_booking':number_of_booking,'data':serializer.data})
            
            
            else:
                bookings = AgentBooking.objects.all()
                number_of_booking= bookings.count()
                serializer = Agentbookingserailizer(bookings, many=True)
                return Response({'msg':'No Data found', 'data':serializer.data})
        
        except AgentBooking.DoesNotExist:
             Response({'msg':'No Data found', 'number_of_booking':number_of_booking,'data':serializer.data}, status=status.HTTP_204_NO_CONTENT)     
    


class Agentbooking_accept(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        data = request.data
        user = request.user
        booking= AgentBooking.objects.get(id=id)
        client_name=booking.client_name
        client_mobile=booking.mobile_number
        # driver_mobile=user.phone
        # driver=booking.accepted_driver
        # date=booking.booking_date
        # time=booking.client_booking_time
        if booking.status == "active":
                return Response({'msg': 'booking already accepted by other driver'})
        
        elif booking.status == "pending":
            serializer= Agentbookingserailizer(booking, data=data, partial=True)
        #     #booking.accepted_driver= user
            if serializer.is_valid():
                serializer.validated_data['accepted_driver']=user
                serializer.validated_data['driver_name'] = AddDriver.objects.get(driver_user=user)
                # print("driver name: ", driver_name)
                # print(type(driver_name))
        #         whatsapp_number = f"whatsapp:+91{client_mobile}"
        #         msg="""Dear {client_name}

        #                         Mr. {driver_name}
        #                         Mobile - {driver_mobile}
        #                         Will be arriving at your destination.

        #                         Date -{date}
        #                         Time -{time}

        #                         Our rates - https://www.driveronhire.com/rates

        #                         *T&C Apply
        #                         https://www.driveronhire.com/privacy-policy

        #                         Thanks 
        #                         Driveronhire.com
        #                         Any issue or feedback call us 02243439090"""
        #         message=msg.format(client_name="Sir/Madam", driver_name=driver_name, driver_mobile=driver_mobile,date=date, time=time)
                # data.setdefault("accepted_driver",user.id)
        #         # utils.twilio_whatsapp(to_number=whatsapp_number, message=message)
                serializer.save()
                return Response({'msg':'bookking Updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
      
        else:
            return Response({'msg':'Not Accpeted', 'error':serializer.errors})
        # return Response({'msg': 'No booking to accept'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        start_deuty=currenttime.strftime("%H:%M:%S")
        booking= AgentBooking.objects.get(id=id)
        if booking.deuty_started:
            return Response({'msg': 'Duty has already started', 'data': None}, status=status.HTTP_200_OK)

        serializer=Agentbookingserailizer(booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['deuty_started']=start_deuty
            serializer.save()
            return Response({'msg':'Deuty Started', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg':'Deuty Not Started', 'data':serializer.errors}, status=status.HTTP_200_OK)


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
            return Response({'msg': 'Duty has already Ended', 'data': None})

        serializer=Agentbookingserailizer(booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['deuty_end']=end_deuty
            serializer.save()
            return Response({'msg':'Deuty Ended', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg':'Deuty Not Ended', 'data':serializer.errors}) 


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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # try:
            data = request.data
            user = request.user
            driver_instance = AddDriver.objects.get(driver_user=user.id)
            driver_mobile = User.objects.get(id=user.id)
            serializer = Agentbookingserailizer(data=data)

            if serializer.is_valid():
                serializer.validated_data['booking_created_by'] = user
                serializer.validated_data['driver_name'] = driver_instance
                serializer.validated_data['accepted_driver'] = driver_mobile
                serializer.validated_data['guest_booking'] = True
                serializer.validated_data['request_type']="Guest"
                serializer.validated_data['status']="pending"
                
                serializer.save()
                return Response({'msg': 'Guest Booking done', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Guest booking not done', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # except:
        #     # Handle the specific exception and return an error response
        #     return Response({'msg': 'Error message'}, status=status.HTTP_400_BAD_REQUEST)

        
    def get(self, request):
        try:
            guestbooking=AgentBooking.objects.filter(guest_booking=True, status='pending').order_by('-id')
            serializer=Agentbookingserailizer(guestbooking, many=True)
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
        location_city=request.GET.get('location_city')
        zone_a_data = ZoneA.objects.all()
        zone_b_data = ZoneB.objects.all()
        zone_c_data = ZoneC.objects.all()
        zone_d_data = ZoneD.objects.all()
        zone_e_data = ZoneE.objects.all()
        zone_f_data = ZoneF.objects.all()
        zone_g_data = ZoneG.objects.all()
        # Pune location A model
        pune_b=pune_B_location.objects.all() # Pune Location B model

        zone_a_serializer = ZoneASerializer(zone_a_data, many=True)
        zone_b_serializer = ZoneBSerializer(zone_b_data, many=True)
        zone_c_serializer = ZoneCSerializer(zone_c_data, many=True)
        zone_d_serializer = ZoneDSerializer(zone_d_data, many=True)
        zone_e_serializer = ZoneESerializer(zone_e_data, many=True)
        zone_f_serializer = ZoneFSerializer(zone_f_data, many=True)
        zone_g_serializer = ZoneGSerializer(zone_g_data, many=True)

        """Pune location serializer"""
        pune_a_queryset = pune_A_location.objects.filter(location_city=location_city)
        
        pune_a_exists = pune_a_queryset.exists()
       
        if pune_a_exists:
            pune_a_serializer = punelocationASerializer(pune_a_queryset, many=True)
        else:
            pune_a_serializer = punelocationASerializer([], many=True)

        pune_b_serializer=punelocationBSerializer(pune_b, many=True)
        """End pune location serializer"""
         
        
        combined_data = (zone_a_serializer.data + 
                        zone_b_serializer.data + zone_c_serializer.data + zone_d_serializer.data + zone_e_serializer.data + 
                        zone_f_serializer.data + zone_g_serializer.data + pune_a_serializer.data+ pune_b_serializer.data)
        
        # Filter only data for the specified city
        filtered_data = [item for item in combined_data if ('location_city' not in item and location_city is None) or(item.get('location_city') == location_city)]
        
        sorted_data = sorted(filtered_data, key=lambda x: x['location'])

        return Response(sorted_data)
    

# Test decline booking api
class TestDeclineBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        xyz = AddDriver.objects.filter(driver_user=user)
        driver_ids = [driver.id for driver in xyz]
        one_hour_ago = datetime.now() - timedelta(hours=1)


        # Check if the user is a notified driver
        try:
            is_notified_driver = Notifydrivers.objects.filter(driver=driver_ids[0]).exists()
            notify_driver_data = Notifydrivers.objects.filter(driver=driver_ids[0])
            
           
            if is_notified_driver:
                data_list = []
                for booking_idd in notify_driver_data:
                    booking = PlaceBooking.objects.filter(Q(id=booking_idd.place_booking.id) & Q(status="pending"))
                    decline_data = Declinebooking.objects.filter(placebooking=booking_idd.place_booking.id,refuse_driver_user=user).exists()
                    if not decline_data:
                        serializer = PlacebookingSerializer(booking, many=True)
                        data_list.extend(serializer.data)
                # Filter out bookings older than 1 hour
                filtered_data_list = []
                print("Blank list")
                for booking in data_list:
                    booking_time = datetime.strptime(booking['booking_time'], '%Y-%m-%dT%H:%M:%S.%f%z')
                    if booking_time >= one_hour_ago:
                        filtered_data_list.append(booking)
                        print("After list")

                if not data_list:  # No bookings accepted by any driver
                    return Response({'data': []}, status=status.HTTP_200_OK)
                else:
                    revers_records = data_list[::-1]
                    return Response({'data': revers_records}, status=status.HTTP_200_OK)
                    
                # revers_recors= data_list[::-1]
                # return Response({'data':revers_recors}, status=status.HTTP_200_OK)
            
            else:
                return Response({'error': 'Access forbidden. You are not a notified driver.'}, status=status.HTTP_403_FORBIDDEN)
            
        except:
            return Response({'error': 'You dont have any booking data.'}, status=status.HTTP_403_FORBIDDEN)


# Test Agent decline booking api
class TestAgentDeclineBooking(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        xyz = AddDriver.objects.filter(driver_user=user)
        driver_ids = [driver.id for driver in xyz]
        one_hour_ago = datetime.now() - timedelta(hours=1)

        # Check if the user is a notified driver
        #try:
        is_notified_driver = NotifydriversAgent.objects.filter(driver=driver_ids[0]).exists()
        notify_driver_data = NotifydriversAgent.objects.filter(driver=driver_ids[0])
        
        
        if is_notified_driver:
            
            data_list = []
            for booking_idd in notify_driver_data:
                
                booking = AgentBooking.objects.filter(Q(id=booking_idd.agent_booking.id) & Q(status="pending"))
                
                decline_data = Declinebooking.objects.filter(agentbooking=booking_idd.agent_booking.id, refuse_driver_user=user).exists()
                
                if not decline_data:
                    serializer = Agentbookingserailizer(booking, many=True)
                    data_list.extend(serializer.data)
                # serializer = PlacebookingSerializer(booking, many=True)
                
                # data_list.extend(serializer.data)
                
                
            revers_recors= data_list[::-1]

            return Response({'data':revers_recors}, status=status.HTTP_200_OK)
        
        
        else:
            return Response({'error': 'Access forbidden. You are not a notified driver.'}, status=status.HTTP_403_FORBIDDEN)
            
class dashboardbooking(APIView):
    """
    Using this api we are getting live booking analytics
    """
    def get(self, request):
        bookingfor="local"
        outstation_booking="outstation"
        drop="drop"
        filter_booking=AgentBooking.objects.filter(bookingfor=bookingfor)
        local_booking_count=filter_booking.count()
        print("Local count:", local_booking_count)

        #OutStation booking count
        outs_booking=AgentBooking.objects.filter(bookingfor=outstation_booking)
        outcount=outs_booking.count()
        print("Out count:", outcount)

        #Drop Booking Count
        drop_booking=AgentBooking.objects.filter(bookingfor=drop)
        dropcount=drop_booking.count()
        print("Drop booking:", dropcount)

        #serializer=Agentbookingserailizer(filter_booking,many=True)
        return Response({'msg':'Local booking', 'local_booking_count':local_booking_count, 'outcount':outcount, 'dropcount':dropcount})