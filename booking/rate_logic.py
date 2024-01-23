from rest_framework.views import APIView 
from .models import *
from .serializers import *
from datetime import datetime, timedelta, time, timezone
from rest_framework.response import Response
from rest_framework import status

class InvoiceGenerate(APIView):
    
    def post(self, request):
        data = request.data
        driver_id= data['driver']
        placebooking_id = data['placebooking']
        Placebooking_data = PlaceBooking.objects.values().get(id=placebooking_id)
        Placebooking_data_id = PlaceBooking.objects.get(id=placebooking_id)
        print("Place booking data: ", Placebooking_data)
        booking_type = Placebooking_data['booking_type']
        print("booking type: ", booking_type)
        trip_type = Placebooking_data['trip_type']
        print("Trip type: ", trip_type)
        car_type = Placebooking_data['car_type']   
        print("Car type: ", car_type)   

        user = request.user

        if booking_type == "local":
            packege = Placebooking_data['packege']
            outskirt_charge = Placebooking_data['outskirt_charge']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_end_datetime = Placebooking_data.get('deuty_end')

            # Convert deuty_started to a datetime object with timezone information
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)

            # Make sure deuty_end_datetime has timezone information (if not already)
            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)

            # Calculate the time difference
            time_difference = deuty_end_datetime - deuty_started_datetime

            # Printing the time difference
            print("Time Difference:", time_difference)
            def base_price():
                if trip_type == "roundTrip":
                    if car_type == "Luxury":
                        if packege == "2hrs":
                            if time_difference < timedelta(hours=2):
                                print("This is luxury car 2 hour")
                                return 500
                            else:
                                # Calculate the number of additional hours (rounded up)
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                # Add 100 for each additional hour beyond 4 hours
                                additional_cost = (additional_hours * 100) -200
                                bill = 500 + additional_cost
                                print("This is luxury car 2 hour with addition hour")
                                return bill
                        elif packege == "4hrs":
                            if time_difference < timedelta(hours=4):
                                print("This is luxury car 4 hour")
                                return 600
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                print(additional_hours)
                                additional_cost = (additional_hours * 100) - 400
                                bill = 600 + additional_cost
                                print("This is luxury car 4 hour with addition hour")
                                return bill
                        elif packege == "8hrs":
                            if time_difference < timedelta(hours=8):
                                print("This is luxury car 8 hour")
                                return 900
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 900 + additional_cost
                                print("This is luxury car 8 hour with addition hour")
                                return bill
                    else:
                        if packege == "2hrs":
                            if time_difference < timedelta(hours=2):
                                print("This is Normal car 2 hour")
                                return 400
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100)-200
                                bill = 400 + additional_cost
                                print("This is Normal car 2 hour with addition hour")
                                return bill
                        elif packege == "4hrs":
                            if time_difference < timedelta(hours=4):
                                print("This is Normal car 4 hour")
                                return 500
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) -400
                                bill = 500 + additional_cost
                                print("This is Normal car 4 hour with addition hour")
                                return bill
                        elif packege == "8hrs":
                            if time_difference < timedelta(hours=8):
                                print("This is Normal car 8 hour")
                                return 800
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 800 + additional_cost
                                print("This is Normal car 8 hour with addition hour")
                                return bill

                elif trip_type == "oneWay":
                    print("One way")
                    if car_type == "Luxury":
                        if packege == "2hrs":
                            if time_difference < timedelta(hours=2):
                                return 600
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 200
                                bill = 600 + additional_cost
                                return bill
                        elif packege == "4hrs":
                            if time_difference < timedelta(hours=4):
                                return 700
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 400
                                bill = 700 + additional_cost
                                return bill
                        elif packege == "8hrs":
                            if time_difference < timedelta(hours=8):
                                return 1000
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 1000 + additional_cost
                                return bill
                    else:
                        if packege == "2hrs":
                            if time_difference < timedelta(hours=2):
                                return 500
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 200
                                bill = 500 + additional_cost
                                return bill
                        elif packege == "4hrs":
                            if time_difference < timedelta(hours=4):
                                return 600
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 400
                                bill = 600 + additional_cost
                                return bill
                        elif packege == "8hrs":
                            if time_difference < timedelta(hours=8):
                                return 900
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 900 + additional_cost
                                return bill
                            
            def total_price():
                base_charge = base_price()
                print("Base charge: ",base_charge)
                if deuty_started_datetime.date() != deuty_end_datetime.date():
                    if deuty_end_datetime.time() > time(23, 0) or deuty_started_datetime.time() < time(6, 0):
                        charge_with_night_allowance = base_charge + 200
                        print("Night charge: ",charge_with_night_allowance)
                        total_charge = charge_with_night_allowance + outskirt_charge
                        print("outskirt charge: ", total_charge)
                        return total_charge
                    else:
                        total_charge = base_charge + outskirt_charge
                        print("outskirt charge without nigt: ", total_charge)
                        return total_charge
                else:
                    charge_with_night_allowance = base_charge + 200
                    print("Night charge: ",charge_with_night_allowance)
                    total_charge = charge_with_night_allowance + outskirt_charge
                    print("outskirt charge: ", total_charge)
                    return total_charge
                        
            
            price = total_price()
            print(price)
        
        if booking_type == "outstation":
            no_of_days = Placebooking_data['no_of_days']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_started_time += timedelta(hours=5, minutes=30)
            print("duty start time: ", deuty_started_time)
            deuty_end_datetime = Placebooking_data.get('deuty_end')
            deuty_end_datetime += timedelta(hours=5, minutes=30)
            print("duty end time: ", deuty_end_datetime)
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)
            print("duty start: ", deuty_started_datetime)

            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)
            time_difference = deuty_end_datetime - deuty_started_datetime
            print("Time Difference:", time_difference)
            print("number os days: ", no_of_days)

            if car_type == "Luxury":
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                    print("Extra day added")
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                    print(f"Night charge added: {night_charge}")
                else:
                    print("Normal charges")
            else:
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    no_of_days += 1
                    print("Extra day added")
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                    print(f"Night charge added: {night_charge}")
                else:
                    print("Normal charge.")


        if booking_type == "outstation_drop":
            no_of_days = Placebooking_data['no_of_days']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_started_time += timedelta(hours=5, minutes=30)
            print("duty start time: ", deuty_started_time)
            deuty_end_datetime = Placebooking_data.get('deuty_end')
            deuty_end_datetime += timedelta(hours=5, minutes=30)
            print("duty end time: ", deuty_end_datetime)
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)
            print("duty start: ", deuty_started_datetime)

            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)
            time_difference = deuty_end_datetime - deuty_started_datetime
            print("Time Difference:", time_difference)
            print("number os days: ", no_of_days)

            if car_type == "Luxury":
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                    print("Extra day added")
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                    print(f"Night charge added: {night_charge}")
                else:
                    print("Normal charges")
            else:
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                    print("Extra day added")
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                    print(f"Night charge added: {night_charge}")
                else:
                    print("Normal charge.")
            

        inv_seri =  InvoiceSerializer(data = data)
        if inv_seri.is_valid():
            inv_seri.validated_data['placebooking'] = Placebooking_data_id
            # inv_seri.validated_data['user_id'] = user.id
            # print("data: ", data)
            inv_seri.save()
            print("serializer data: ", inv_seri.validated_data )

            return Response({'msg': 'invice is generate', 'data':inv_seri.data}, status=status.HTTP_201_CREATED)
        else:
             return Response({'msg': 'Unable to generate', 'data':inv_seri.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def get(self, request, id):
        try:
            get_all_inv = Invoice.objects.get(id=id)
            get_seri= InvoiceSerializer(get_all_inv)
            return Response({'msg': 'All invoice list', 'data':get_seri.data}, status=status.HTTP_200_OK)
        
        except Invoice.DoesNotExist:
            raise serializers.ValidationError("No Data Found")