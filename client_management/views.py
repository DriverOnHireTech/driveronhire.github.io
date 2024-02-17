from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from booking.models import PlaceBooking

# Create your views here.

# User profile view
class Userprofileview(APIView):
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        
            data=request.data
            # user=request.user

            serializer=UserProfileSerializer(data=data)
            if serializer.is_valid():
                #serializer.validated_data['user']=user  
                serializer.save()
                add_driver_data = request.data.get('addfavoritedriver')
                if add_driver_data:
                # Assuming 'addfavoritedriver' contains a list of driver IDs
                    for driver_id in add_driver_data:
                        try:
                            driver = AddDriver.objects.get(id=driver_id)
                            serializer.instance.addfavoritedriver.add(driver)
                        except AddDriver.DoesNotExist:
                            return Response({'msg': f"Driver with id {driver_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'msg':'Profile updated', 'data':serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

       
    def get(self, request):
         try:
            #   user=request.user
            #   print("user: ", user.phone)
            #   user_profile=UserProfile.objects.get(user=user)
            #   user_profile.mobile_number = user.phone
            #   user_profile.save()
              user_profile=UserProfile.objects.all().order_by('-id')
              serializer=UserProfileSerializer(user_profile, many=True)
              return Response({'msg':'user profile', 'data':serializer.data}, status=status.HTTP_200_OK)
         except UserProfile.DoesNotExist:
              return Response({'msg':'No data found'}, status=status.HTTP_204_NO_CONTENT)
         
    def patch(self, request,id):
            data=request.data
            add_driver_data = request.data.get('addfavoritedriver')
            profile=UserProfile.objects.get(id=id)
            serializer=UserProfileSerializer(profile, partialy=True)
            if serializer.is_valid():
                 serializer.save()
            if add_driver_data:
            # Assuming 'addfavoritedriver' contains a list of driver IDs
                for driver_id in add_driver_data:
                    try:
                        driver = AddDriver.objects.get(id=driver_id)
                        serializer.instance.addfavoritedriver.add(driver)
                    except AddDriver.DoesNotExist:
                        return Response({'msg': f"Driver with id {driver_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Profile updated', 'data':serializer.data}, status=status.HTTP_201_CREATED)
# End User Profile
    
#get single user profile 
class getsingleuserprofile(APIView):
     def get(self, request, id):
          profile=UserProfile.objects.get(id=id)
          serializer=UserProfileSerializer(profile)
          return Response({'msg':'single profile', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)