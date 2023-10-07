from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import NewUserSerializer, UserLoginserializer
import random
from twilio.rest import Client
from base_site import settings

from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .utils import username_gene


# Create your views here.


class Adduser(APIView):
    def post(self, request):
        data= request.data
        phone = request.data.get('phone')
        serailizer=NewUserSerializer(data=data)
        if serailizer.is_valid():
            otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            serailizer.validated_data['otp'] = otp
            serailizer.validated_data['username'] = username_gene()
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP is: {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )
            serailizer.save()
    
            return Response({'msg':'Data is saved', 'data': serailizer.data, 'message':"Otp has been sent."}, status=status.HTTP_201_CREATED)
        
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


       

class LoginView(APIView):
    def post(self, request):
        data =  request.data

        phone = data.get('phone')
        password = data.get('password')
        otp = data.get('otp')
        user = User.objects.filter(phone=phone).first()
        if (str(otp) == user.otp):
            login(request, user)
            token,created = Token.objects.get_or_create(user=user)
            return Response({"msg":'Welcome Customer', 'data':data ,'token':token.key}, status=status.HTTP_200_OK)
                
        else:
            return Response({"msg":"unable to login"}, status=status.HTTP_401_UNAUTHORIZED)
            

class Logoutapi(APIView):
    def post(self, request):
        try:
            user =  request.user.id
            logout(request)
            return Response({'msg':'Logout successfuly'}, status=status.HTTP_200_OK)
        
        except:
            return Response({'msg':'unable to logout'}, status=status.HTTP_404_NOT_FOUND)


class GenerateOTP(APIView):
    def post(self, request):
        phone = request.data.get('phone')

        if not phone:
            return Response({"message": "Mobile number is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(phone=phone).first()
        # Generate a 4-digit OTP
        otp = user.otp

        # Here, you should send the OTP to the provided mobile number using an SMS gateway or a library like twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )

        return Response({"message": "OTP generated and sent successfully."}, status=status.HTTP_200_OK)



class ValidateOTP(APIView):
    def post(self, request):
        entered_otp = request.data.get('otp')

        # Retrieve the generated OTP and mobile number from the session
        generated_otp = request.session.get('generated_otp')
        mobile_number = request.session.get('mobile_number')

        if not generated_otp or not mobile_number:
            return Response({"message": "OTP is not generated or mobile number is missing."},
                            status=status.HTTP_400_BAD_REQUEST)

        if entered_otp == generated_otp:
            # Clear the session data after successful OTP validation
            request.session.flush()
            # If the entered OTP is valid, redirect to the home page
            request.session['otp_validated'] = True
            return Response({"message": "OTP validated successfully. Redirecting to home page."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid OTP. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
        


