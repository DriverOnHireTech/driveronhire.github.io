from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


# Create your views here.

# User profile view
class Userprofileview(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        
            data=request.data
            user=request.user
            serializer=UserProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data['user']=user
                serializer.save()
                return Response({'msg':'Profile updated', 'data':serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

       
        
# End User Profile