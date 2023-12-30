from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user_master.models import ZoneA, ZoneB, ZoneC
from .zone_logic import zone_get, return_charges

class ExtraRate(APIView):
    def get(self, request):
        # Assuming you have 'pickup_location' and 'drop_location' in your request query parameters
        pickup_location = request.query_params.get('pickup_location', None)
        drop_location = request.query_params.get('drop_location', None)

        if not pickup_location or not drop_location:
            return Response({'error': 'pickup_location and drop_location are required parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        pickup_location = zone_get(pickup_location)
        drop_location = zone_get(drop_location)

        if not pickup_location or not drop_location:
            return Response({'error': 'Invalid pickup_location or drop_location.'}, status=status.HTTP_400_BAD_REQUEST)

        extra_charge = return_charges(pickup_location, drop_location)

        return Response({'extra_charge': extra_charge}, status=status.HTTP_200_OK)
