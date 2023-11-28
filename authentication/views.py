from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import NewUserSerializer, UserLoginserializer, Fcmserializer
import random
from twilio.rest import Client
from base_site import settings
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .utils import username_gene, generate_otp
# from base_site.backend import authenticate
from fcm_django.models import FCMDevice
from django.core.exceptions import ObjectDoesNotExist


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
        all_user= User.objects.all()
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

class LoginView(APIView):
    def post(self, request):
        data =  request.data
        phone = data.get('phone')
        password = data.get('password')
        user = authenticate(request, phone,password)
        if user is not None:
            login(request, user)
            token,created = Token.objects.get_or_create(user=user)
            fcm_token = data.get('fcm_token')

            if FCMDevice.objects.filter(registration_id=fcm_token).exists() and fcm_token is not None:
                ("If line")
                return Response({'msg':'Fcm device token allready generated', 'data':data ,'token':token.key}, status=status.HTTP_200_OK) 
            else:
                ("else part")
                # Create and save the FCM device for the user
                device, created = FCMDevice.objects.get_or_create(user=user)
                device.registration_id = fcm_token
                device.type = "android"
                device.name = user.get_username()
                device.save()
                return Response({"msg":'Welcome Customer', 'data':data ,'token':token.key}, status=status.HTTP_200_OK) 
                  
        else:
            return Response({"msg":"unable to login"}, status=status.HTTP_401_UNAUTHORIZED)

            

class Logoutapi(APIView):
    def post(self, request):
        try:
            user =  request.user.id
            logout(request)
            request.user.auth_token.delete()
            return Response({'msg':'Logout successfuly'}, status=status.HTTP_200_OK)
        
        except:
            return Response({'msg':'unable to logout'}, status=status.HTTP_404_NOT_FOUND)
    

class SendOTPAPIView(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        send_phone = f"+91{phone}"
        
        try:
            driver = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP and save it in the user profile
        otp = generate_otp()  # Replace with your OTP generation logic
        print("otp: ",otp)

        # Save the OTP in the  user model
        driver.otp = otp
        driver.save()

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
        print("Phone number",phone)

        try:
            user = User.objects.get(phone=phone)
            print("User data: ",user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve OTP from the session
        saved_otp = user.otp
        print("otp_attempt", otp_attempt)
        print("saved_otp", saved_otp)

        if saved_otp == otp_attempt:
             # Clear the OTP from the User model after successful verification
            print("Before authentication")
            # Authenticate and login the driver
            user = authenticate(request, phone=phone, saved_otp=saved_otp)
            print("After authentication")
            print("User",user)

            if user:
                login(request, user)
                # Generate or retrieve a token for the authenticated user
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)