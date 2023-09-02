from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from .paginations import cutomepegination
from rest_framework import status
from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend
# from dateutil.relativedelta import relativedelta
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication



from datetime import date, datetime
from .utils import leavecalcu

class Driversignup(APIView):   # For Driver signup
    def post(self, request):
        data=request.data
        Dri_serializer= DriversignupSerializer(data=data)
        
        if Dri_serializer.is_valid():
            user=User(username=Dri_serializer.validated_data['username'],
                      email=Dri_serializer.validated_data['email'])
            password=Dri_serializer.validated_data['password']
            user.set_password(password)
            user.save()
            return Response({'msg':'Driver signup is done', 'data':Dri_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response ({'msg':'Some thing wrong', 'data':Dri_serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Driver Login
class Driverlogin(APIView): 
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'msg': 'Login Success'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

 # for Driver location update   
class driverlocation(APIView):  
    def post(self, request):
        user=request.user
        serializer= Driverlocationserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'location is update', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'unable to update', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:

            alllocation = Driverlocation.objects.all()
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
       

    

class MyDriverList(generics.ListCreateAPIView):
     
    queryset = AddDriver.objects.all().order_by('id').reverse()
    serializer_class = MyDriverSerializer
    parser_classes = [MultiPartParser, FormParser]


    

class Driversearch(ListAPIView):
    try:
        pagination_class=cutomepegination
        queryset = AddDriver.objects.all()
        serializer_class = MyDriverSerializer
        filter_backends = [DjangoFilterBackend]

        filterset_fields = ['driver_type', 'first_name', 'driver_status', 'branch']
    except AddDriver.DoesNotExist:
        pass


# Driver profile
class Driverprofile(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            driver = AddDriver.objects.get(driver_user=request.user)
            serializer = MyDriverSerializer(driver)
            return Response({'msg': 'Here is your profile', 'data':serializer.data})
        
        except AddDriver.DoesNotExist:
            return Response({'msg': 'No profile was found'})    
        

# Driver Leave API
class Driverleaveapi(APIView):
    def post(self, request):
        data=request.data
        serializer=DriverleaveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Driver Leave save'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'may be you missed some field'}, status=status.HTTP_400_BAD_REQUEST) 












# class MyDriverGetList(APIView):
#     def get(self, request, id):
#         try:
#             driver = AddDriver.objects.get(id=id)
#             serializer = MyDriverSerializer(driver)
#             return Response(serializer.data)
#         except AddDriver.DoesNotExist:
#             return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)

#     serializer_class = MyDriverSerializer

#     def put(self, request, id):
#         try:
#             driver = AddDriver.objects.get(id=id)
#             serializer = MyDriverSerializer(driver, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(request.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except AddDriver.DoesNotExist:
#             Response({'msg': 'Search value not present in database'}, status=status.HTTP_417_EXPECTATION_FAILED)
#             return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, id):
#         try:
#             driver = AddDriver.objects.get(id=id)
#             driver.delete()
#             return Response({'message': 'Object Deleted'}, status=status.HTTP_204_NO_CONTENT)
#         except AddDriver.DoesNotExist:
#             return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)