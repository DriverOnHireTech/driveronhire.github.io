from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from .serializers import NewUserSerializer, UserLoginserializer
import random
from twilio.rest import Client
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


# Create your views here.


class Adduser(APIView):
    def post(self, request):
        data= request.data
        serailizer=NewUserSerializer(data=data)
        if serailizer.is_valid():
            serailizer.save()
            print("Serializer Data:",serailizer.data)
            return Response({'msg':'Data is saved', 'data': serailizer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'msg':'Error in sav data', 'data': serailizer.errors})
       
    def get(self, request):
        all_user= User.objects.all()
        serializer= NewUserSerializer(all_user, many=True)
        return Response({'msg':'Here is your data', 'data':serializer.data}, status=status.HTTP_200_OK)
    

class LoginView(APIView):
    def post(self, request):
        data =  request.data

        phone = data.get('phone')
        password = data.get('password')
       
           
        user = authenticate(phone=phone, password=password)
        if user is not None:
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
        mobile_number = request.data.get('mobile_number')

        if not mobile_number:
            return Response({"message": "Mobile number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a 4-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        # print(otp)

        # Clear the previous session data
        request.session.flush()
        # print(mobile_number)
        # print(otp)

        # Save the OTP in the session for validation later
        request.session['generated_otp'] = otp
        request.session['mobile_number'] = mobile_number

        # Here, you should send the OTP to the provided mobile number using an SMS gateway or a library like twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=mobile_number
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
