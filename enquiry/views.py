from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Enquiry, driverenquiry
from .serializers import MyEnquirySerializer, DriverEnquiryserializer
from utils.email import sendemail
from django.core.mail import send_mail
from django.conf import settings


class MyEnquiryList(generics.ListCreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = MyEnquirySerializer


class MyEnquiryGetList(generics.ListAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = MyEnquirySerializer
    lookup_field = 'id'


class MyEnquiryUpdate(generics.UpdateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = MyEnquirySerializer
    lookup_field = 'id'


class MyEnquiryDelete(generics.DestroyAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = MyEnquirySerializer
    lookup_field = 'id'


class senddriverenquiry(APIView):
    def post(self, request):
        data= request.data
        message= request.data['message']
        phone_number= request.data['phone_number']
        email=request.data['email']

        serializer = DriverEnquiryserializer(data=data)
        if serializer.is_valid():
            mail_send= send_mail(phone_number, message, email, [settings.EMAIL_HOST_USER], fail_silently=False)
            serializer.save()
            return Response({'msg':'Enquiry has been sent', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'Not sent', 'data':serializer.errors}, status= status.HTTP_406_NOT_ACCEPTABLE)
        