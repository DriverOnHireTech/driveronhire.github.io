from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework import filters
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .utils import leavecalcu
from booking.models import PlaceBooking
from booking.serializers import PlacebookingSerializer
from rest_framework.pagination import PageNumberPagination




 # for Driver location update   


class driverlocation(APIView):  
    def post(self, request):
        user=self.request.user
        serializer= Driverlocationserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'location is update', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'unable to update', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:

            alllocation = Driverlocation.objects.all().order_by('driver')
            loc_seri =Driverlocationserializer(alllocation, many=True)
            return Response({'msg': 'All Location List', 'data':loc_seri.data}, status=status.HTTP_200_OK)
        
        except Driverlocation.DoesNotExist:
            return Response({'msg':'No driver location avalaible', 'data':loc_seri.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id):
        dlocation = Driverlocation.objects.get(id=id)
        serializer = Driverlocationserializer(dlocation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"location updated", "data":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class BasicDetailView(generics.ListCreateAPIView):
    queryset = BasicDetail.objects.all().order_by('id').reverse()
    serializer_class = BasicDetailSerializer


class MyDriverList(generics.ListCreateAPIView):
    pagination_class=PageNumberPagination
    queryset = AddDriver.objects.all().order_by('id').reverse()
    serializer_class = MyDriverSerializer
    parser_classes = [MultiPartParser, FormParser]


"""Update Driver"""
class updatedriver(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        data= request.data
        print("Data: ",data)
        user= request.user
        print("User: ",user.id)
        driver = AddDriver.objects.get(driver_user=user.id)
        print("Again Driver: ", driver.id)
        serializer =MyDriverSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid(): 
            serializer.save()
            print("Serializer Data: ", serializer.data)
            return Response({"msg":"location updated", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class updatedriverwithid(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        driver = AddDriver.objects.get(id=id)
        serializer = MyDriverSerializer(driver)
        return Response(serializer.data)

"""End update driver"""
class Driversearch(ListAPIView):
        try:

            # pagination_class=cutomepegination()
            model_data= AddDriver.objects.all()
            serializer_class = MyDriverSerializer 
            filter_backends = [DjangoFilterBackend]
            filterset_fields = ['mobile','driver_type', 'first_name', 'driver_status', 'branch']
            
            def get_queryset(self):
                queryset = AddDriver.objects.all()

            # You can further filter the queryset based on request parameters if needed
            # Example: filter by 'driver_type' from the request query parameters
                mobile = self.request.query_params.get('mobile')
                if mobile:
                    queryset =queryset.filter (mobile=mobile)
                    count=queryset.count()
    

                return queryset
        except AddDriver.DoesNotExist:
            Response({'msg':'No Record Founf'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Driver profile
class Driverprofile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user=request.user
            driver = AddDriver.objects.filter(driver_user=request.user)
            serializer = MyDriverSerializer(driver, many=True)
            return Response({'msg': 'Here is your profile', 'data':serializer.data}, status=status.HTTP_200_OK)
        
        except AddDriver.DoesNotExist:
            return Response({'msg': 'No profile was found', 'error':serializer.errors}, status=status.HTTP_204_NO_CONTENT)    


# Driver Leave API
class Driverleaveapi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user=self.request.user
        data=request.data
        leave_from_date = data.get('leave_from_date')
        leave_to_date = data.get('leave_to_date')

        if leave_from_date and leave_to_date:
            try:
                leave_from_date = datetime.strptime(leave_from_date, "%Y-%m-%d").date()
                leave_to_date = datetime.strptime(leave_to_date, "%Y-%m-%d").date()

                no_of_days = leavecalcu.get_difference(leave_from_date, leave_to_date)

                serializer = DriverleaveSerializer(data=data)
                if serializer.is_valid():
                    serializer.validated_data['total_days_of_leave'] = no_of_days
                    serializer.validated_data['driver_name_id'] = user.id
                    serializer.save()
                    return Response({'msg': 'Driver Leave saved'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'msg': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'msg': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'Missing date fields'}, status=status.HTTP_400_BAD_REQUEST)


"""Endpoint for filter booking between 2 dates"""
class Bookingreports(APIView):
    def get(self, request,*args, **kwargs):
        try:
            user=self.request.user
            booking_time= request.GET.get('booking_time')

            booking_time = datetime.strptime(booking_time, '%Y-%m-%d%H:%M:%S')  # Assuming date format 'YYYY-MM-DD'
            print(booking_time)
            end_date_time = booking_time + timedelta(days=30)
            print(end_date_time)

            #filter record between the dates
            if booking_time:
                booking_filter= PlaceBooking.objects.filter(booking_time__range=[booking_time, end_date_time])
                result_serializer=PlacebookingSerializer(booking_filter, many=True)
                return Response({'msg':'Your Booking Records', 'data':result_serializer.data}, status=status.HTTP_202_ACCEPTED)
            
        except PlaceBooking.DoesNotExist:
            return Response({'msg':'No Records Found', 'data':result_serializer.errors})
        return Response("Error")


class DriverreferView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user=self.request.user
        drefserializer= DriverReferserializer(data=request.data)
        if drefserializer.is_valid():
            drefserializer.validated_data['referdrivername_id'] = user.id
            drefserializer.save()
            return Response({'msg':'Driver Refer is saved', 'data':drefserializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'unable to save', 'data':drefserializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        driver_ref_data= ReferDriver.objects.all()

        if driver_ref_data: # Checking Driver Refrense in Databases
            Driver_ref_serialzer= DriverReferserializer(driver_ref_data, many=True)
            return Response({'msg':'All Driver Refrence list', 'data':Driver_ref_serialzer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'No Data Found'}, status=status.HTTP_424_FAILED_DEPENDENCY)


class DriverappstatusView(APIView):
    def post(self, request):
        data=request.data
        serializer=Driverappstatusserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Driver App status is created', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'Record Not created', 'error':serializer.errors}, status=status.HTTP_204_NO_CONTENT)
    

    def get(self, request):
        try:

            all_appstatus= Driverappstatus.objects.all()
            serializer= Driverappstatusserializer(all_appstatus, many=True)
            return Response({'msg':'All Data', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        
        except Driverappstatus.DoesNotExist:
            return Response({'msg':'No Record found', 'error':serializer.errors}, status=status.HTTP_204_NO_CONTENT)
