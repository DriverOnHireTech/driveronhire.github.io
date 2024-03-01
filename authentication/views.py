from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import NewUserSerializer, UserLoginserializer, Fcmserializer
import random
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from twilio.rest import Client
from base_site import settings
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .utils import username_gene, generate_otp, gupshupsms
# from base_site.backend import authenticate
from fcm_django.models import FCMDevice
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed



class Adduser(APIView):
    def post(self, request):
        data= request.data
        phone=request.data['phone']
        if User.objects.filter(phone=phone).exists():
            return Response({'msg':'Number already exists'})
            
        
        else:
            serailizer=NewUserSerializer(data=data)
            if serailizer.is_valid():
                serailizer.validated_data['username'] = username_gene()
                user = serailizer.save()    
                return Response({'msg':'Data is saved', 'data': serailizer.data}, status=status.HTTP_201_CREATED)
            
        return Response({'msg':'Error in sav data', 'data': serailizer.errors})
       
    def get(self, request):
        all_user= User.objects.all().order_by('-id')
        serializer= NewUserSerializer(all_user, many=True)
        return Response({'msg':'Here is your data', 'data':serializer.data}, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        data = request.data
        phone = data.get('phone')
        new_password = data.get('password')  # Change to 'password'

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the provided phone matches the user's phone
        if user.phone != phone:
            return Response({'error': 'Phone number does not match the user'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.password = make_password(new_password)
        user.save()

        serializer = NewUserSerializer(user)

        return Response({'msg': 'User password is updated', 'data': serializer.data}, status=status.HTTP_200_OK)
    


    def delete(self, request, id):
        try:
            user_data = User.objects.get(id=id)
            user_data.delete()
            serializer = NewUserSerializer(user_data)
            return Response({'msg': 'User Deleted', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

class getsingleuser(APIView):
    def get(self, request, id):
        user_data = User.objects.get(id=id)
        serializer=NewUserSerializer(user_data)
        return Response({'msg':'record', 'data':serializer.data}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        data =  request.data
        phone = data.get('phone')
        password = data.get('password')
        user = authenticate(request, phone=phone,password=password)

        if user is not None:
            login(request, user)
            token,created = Token.objects.get_or_create(user=user)
            fcm_token = data.get('fcm_token')
            if fcm_token:
                try:
                    device = FCMDevice.objects.get(registration_id=fcm_token)
                except FCMDevice.DoesNotExist:
                    device = FCMDevice.objects.create(user=user, registration_id=fcm_token, type="android", name=user.get_username())
                    return Response({"msg": 'Welcome Customer', 'data': data, 'token': token.key}, status=status.HTTP_200_OK)
                
                # FCM device token already exists for another user
                return Response({'msg': 'FCM device token already generated', 'data': data, 'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": 'Welcome Customer', 'data': data, 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Unable to login"}, status=status.HTTP_401_UNAUTHORIZED)
    


class Logoutapi(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            user = request.user
            logout(request)
            request.auth.delete()  # Delete the token directly
            return Response({'msg': 'Logout successful'}, status=status.HTTP_200_OK)
        except AuthenticationFailed:
            return Response({'msg': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'msg': f'Unable to logout: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SendOTPAPIView(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        send_phone = f"91{phone}"
        
        try:
            driver = User.objects.get(phone=phone)
            otp = generate_otp()  # Replace with your OTP generation logic
            print("otp: ",otp)

            # Save the OTP in the  user model
            driver.otp = otp
            driver.save()
            # Send otp via Gupshup
            gupshupsms(self, send_phone,otp)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


        # Send OTP via Twilio
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # message = client.messages.create(
        #     body=f'Your OTP is: {otp}',
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=send_phone
        # )

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)

class VerifyOTPAPIView(APIView):
    
    def post(self, request):
        otp_attempt = request.data.get('otp')
        phone = request.data.get('phone')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve OTP from the session
        saved_otp = user.otp

        if saved_otp == otp_attempt:
             # Clear the OTP from the User model after successful verification
            user.otp = None
            user.save()

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'msg':F"Your OTP {saved_otp}",'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        

#Patch request for first name update
class firtsnameupdate(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request):
        user = request.user
        data=request.data
        first_name=data.get('first_name')
        serializer=NewUserSerializer(instance=user,data=data,partial=True)
        if serializer.is_valid():
            serializer.validated_data['first_name']=first_name
            serializer.save()
            return Response ({'msg':'First name updated', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response ({'msg':'First name not updated'}, status=status.HTTP_204_NO_CONTENT)
