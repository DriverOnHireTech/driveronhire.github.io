from rest_framework.views import APIView 
from .models import *
from .serializers import *
from datetime import datetime, timedelta, time, timezone
from rest_framework.response import Response
from rest_framework import status
import math

class InvoiceGenerate(APIView):
    
    def post(self, request):
        data = request.data
        driver_id= data['driver']
        placebooking_id = data['placebooking']
        Placebooking_data = PlaceBooking.objects.values().get(id=placebooking_id)
        Placebooking_data_id = PlaceBooking.objects.get(id=placebooking_id)
        booking_type = Placebooking_data['booking_type']
        trip_type = Placebooking_data['trip_type']
        car_type = Placebooking_data['car_type']   

        user = request.user

        if booking_type == "local":
            packege = Placebooking_data['packege']
            outskirt_charge = Placebooking_data['outskirt_charge']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_end_datetime = Placebooking_data.get('deuty_end')
            package_value = Placebooking_data.get('packege')

            # Convert deuty_started to a datetime object with timezone information
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)

            # Make sure deuty_end_datetime has timezone information (if not already)
            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)

            # Calculate the time difference
            time_difference = deuty_end_datetime - deuty_started_datetime

            # Printing the time difference
            
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
                    else:
                        if packege == "2hrs":
                            if time_difference < timedelta(hours=2):
                                return 400
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100)-200
                                bill = 400 + additional_cost
                                return bill
                        elif packege == "4hrs":
                            if time_difference < timedelta(hours=4):
                                return 500
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) -400
                                bill = 500 + additional_cost
                                return bill
                        elif packege == "8hrs":
                            if time_difference < timedelta(hours=8):
                                return 800
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 800 + additional_cost
                                return bill

                elif trip_type == "oneWay":
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
                if deuty_started_datetime.date() == deuty_end_datetime.date():
                    if deuty_end_datetime.time() > time(23, 0) or deuty_started_datetime.time() < time(6, 0):
                        night_charge = 200
                        charge_with_night_allowance = base_charge + 200
                        
                        total_charge = charge_with_night_allowance + outskirt_charge
                        return total_charge, base_charge, night_charge, outskirt_charge
                    else:
                        night_charge = 0
                        total_charge = base_charge + outskirt_charge
                        return total_charge, base_charge, night_charge, outskirt_charge
                else:
                    night_charge = 200
                    print("Night charge: ",night_charge)

                total_charge = base_charge + night_charge + outskirt_charge 
                

                return total_charge, base_charge

            price = total_price()
            total_price_value = price[0]
            base_price = price[1]
            night_charge = price[2]
            outskirt_charge = price[3]
            # additional_hours = price[4]
            # extra_hour_charge = additional_hours*100
            inv_seri =  InvoiceSerializer(data = data)
            if inv_seri.is_valid():
                inv_seri.validated_data['placebooking'] = Placebooking_data_id
                inv_seri.validated_data['base_charge'] = base_price
                inv_seri.validated_data['total_charge'] = total_price_value
                inv_seri.validated_data['night_charge'] = night_charge
                inv_seri.validated_data['outskirt_charge'] = outskirt_charge
                # inv_seri.validated_data['additional_hours'] = additional_hours
                # inv_seri.validated_data['extra_hour_charge'] = extra_hour_charge
                inv_seri.validated_data['driver'] = AddDriver.objects.get(id=driver_id)
                # print("data: ", data)
                inv_seri.save()

                return Response({'msg': 'invice is generate', 'data':inv_seri.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Unable to generate', 'data':inv_seri.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if booking_type == "outstation":
            no_of_days = Placebooking_data['no_of_days']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_started_time += timedelta(hours=5, minutes=30)
            deuty_end_datetime = Placebooking_data.get('deuty_end')
            deuty_end_datetime += timedelta(hours=5, minutes=30)
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)


            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)
            time_difference = deuty_end_datetime - deuty_started_datetime

            if car_type == "Luxury":
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                else:
                    print("Normal charges")
            else:
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    no_of_days += 1
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                else:
                    print("Normal charge.")


        if booking_type == "outstation_drop":
            no_of_days = Placebooking_data['no_of_days']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_started_time += timedelta(hours=5, minutes=30)
            deuty_end_datetime = Placebooking_data.get('deuty_end')
            deuty_end_datetime += timedelta(hours=5, minutes=30)
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)

            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)
            time_difference = deuty_end_datetime - deuty_started_datetime

            if car_type == "Luxury":
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                else:
                    print("Normal charges")
            else:
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                    print(f"Night charge added: {night_charge}")
                else:
                    print("Normal charge.")

        
    

    def get(self, request, id):
        try:
            get_all_inv = Invoice.objects.get(id=id)
            get_seri= InvoiceSerializer(get_all_inv)
            return Response({'msg': 'All invoice list', 'data':get_seri.data}, status=status.HTTP_200_OK)
        
        except Invoice.DoesNotExist:
            raise serializers.ValidationError("No Data Found")


class InvoiceGenerateAgent(APIView):
    
    def post(self, request):
        data = request.data
        driver_id= data['driver']
        placebooking_id = data['agentbooking']
        Placebooking_data = AgentBooking.objects.values().get(id=placebooking_id)
        Placebooking_data_id = AgentBooking.objects.get(id=placebooking_id)
        booking_type = Placebooking_data['bookingfor']
        trip_type = Placebooking_data['trip_type']
        car_type = Placebooking_data['car_type']   

        user = request.user

        if booking_type == "local":
            packege = Placebooking_data['packege']
            outskirt_charge = Placebooking_data['outskirt_charge']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_end_datetime = Placebooking_data.get('deuty_end')
            package_value = Placebooking_data.get('packege')

            # Convert deuty_started to a datetime object with timezone information
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)

            # Make sure deuty_end_datetime has timezone information (if not already)
            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)

            # Calculate the time difference
            time_difference = deuty_end_datetime - deuty_started_datetime

            # Printing the time difference
            
            def base_price():
                if trip_type == "Round":
                    if car_type == "Luxury" or "SUV Luxury" or "Sedan Luxury":
                        if packege == "2":
                            if time_difference < timedelta(hours=2):
                                print("This is luxury car 2 hour")
                                return 500
                            else:
                                # Calculate the number of additional hours (rounded up)
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                # Add 100 for each additional hour beyond 4 hours
                                additional_cost = (additional_hours * 100) -200
                                bill = 500 + additional_cost
                                return bill
                        elif packege == "4":
                            if time_difference < timedelta(hours=4):
                                return 600
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 400
                                bill = 600 + additional_cost
                                return bill
                        elif packege == "8":
                            if time_difference < timedelta(hours=8):
                                return 900
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 900 + additional_cost
                                return bill
                    else:
                        if packege == "2":
                            if time_difference < timedelta(hours=2):
                                return 400
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100)-200
                                bill = 400 + additional_cost
                                return bill
                        elif packege == "4":
                            if time_difference < timedelta(hours=4):
                                return 500
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) -400
                                bill = 500 + additional_cost
                                return bill
                        elif packege == "8":
                            if time_difference < timedelta(hours=8):
                                return 800
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 800 + additional_cost
                                return bill

                elif trip_type == "One Way":
                    if car_type == "Luxury" or "SUV Luxury" or "Sedan Luxury":
                        if packege == "2":
                            if time_difference < timedelta(hours=2):
                                return 600
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 200
                                bill = 600 + additional_cost
                                return bill
                        elif packege == "4":
                            if time_difference < timedelta(hours=4):
                                return 700
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 400
                                bill = 700 + additional_cost
                                return bill
                        elif packege == "8":
                            if time_difference < timedelta(hours=8):
                                return 1000
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 1000 + additional_cost
                                return bill
                    else:
                        if packege == "2":
                            if time_difference < timedelta(hours=2):
                                return 500
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 200
                                bill = 500 + additional_cost
                                return bill
                        elif packege == "4":
                            if time_difference < timedelta(hours=4):
                                return 600
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 400
                                bill = 600 + additional_cost
                                return bill
                        elif packege == "8":
                            if time_difference < timedelta(hours=8):
                                return 900
                            else:
                                additional_hours = int((time_difference.total_seconds() - 1) // 3600) + 1
                                additional_cost = (additional_hours * 100) - 800
                                bill = 900 + additional_cost
                                return bill
                            
            def total_price():
                base_charge = base_price()
                print("base charge: ", base_charge)
                if deuty_started_datetime.date() == deuty_end_datetime.date():
                    if deuty_end_datetime.time() > time(23, 0) or deuty_started_datetime.time() < time(6, 0):
                        night_charge = 200
                        charge_with_night_allowance = base_charge + 200
                        total_charge = charge_with_night_allowance + outskirt_charge
                        return total_charge, base_charge, night_charge, outskirt_charge
                    else:
                        night_charge = 0
                        total_charge = base_charge + outskirt_charge
                        return total_charge, base_charge, night_charge, outskirt_charge
                else:
                    night_charge = 200
                    print("Night charge: ",night_charge)

                total_charge = base_charge + night_charge + outskirt_charge 
                

                return total_charge, base_charge

            price = total_price()
            total_price_value = price[0]
            base_price = price[1]
            night_charge = price[2]
            outskirt_charge = price[3]
            # additional_hours = price[4]
            # extra_hour_charge = additional_hours*100
            inv_seri =  InvoiceSerializerAgent(data = data)
            if inv_seri.is_valid():
                inv_seri.validated_data['agentbooking'] = Placebooking_data_id
                inv_seri.validated_data['base_charge'] = base_price
                inv_seri.validated_data['total_charge'] = total_price_value
                inv_seri.validated_data['night_charge'] = night_charge
                inv_seri.validated_data['outskirt_charge'] = outskirt_charge
                # inv_seri.validated_data['additional_hours'] = additional_hours
                # inv_seri.validated_data['extra_hour_charge'] = extra_hour_charge
                inv_seri.validated_data['driver'] = AddDriver.objects.get(id=driver_id)
                # print("data: ", data)
                inv_seri.save()

                return Response({'msg': 'invice is generate', 'data':inv_seri.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Unable to generate', 'data':inv_seri.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if booking_type == "outstation":
            no_of_days = Placebooking_data['no_of_days']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_started_time += timedelta(hours=5, minutes=30)
            deuty_end_datetime = Placebooking_data.get('deuty_end')
            deuty_end_datetime += timedelta(hours=5, minutes=30)
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)


            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)
            time_difference = deuty_end_datetime - deuty_started_datetime

            if car_type == "Luxury":
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                else:
                    print("Normal charges")
            else:
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    no_of_days += 1
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                else:
                    print("Normal charge.")


        if booking_type == "outstation_drop":
            no_of_days = Placebooking_data['no_of_days']
            deuty_started_time = Placebooking_data.get('deuty_started')
            deuty_started_time += timedelta(hours=5, minutes=30)
            deuty_end_datetime = Placebooking_data.get('deuty_end')
            deuty_end_datetime += timedelta(hours=5, minutes=30)
            deuty_started_datetime = deuty_started_time.replace(tzinfo=timezone.utc)

            if deuty_end_datetime.tzinfo is None:
                deuty_end_datetime = deuty_end_datetime.replace(tzinfo=timezone.utc)
            time_difference = deuty_end_datetime - deuty_started_datetime

            if car_type == "Luxury":
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                else:
                    print("Normal charges")
            else:
                if deuty_end_datetime.date() > deuty_started_datetime.date() and deuty_end_datetime.time() >= time(6, 0):
                    # Add 1 extra day if duty ended tomorrow
                    # Add 1 extra day
                    no_of_days += 1
                elif deuty_end_datetime.time() > time(23, 0) or deuty_end_datetime.time() < time(6, 0):
                    # Add 200 for night charge
                    night_charge = 200
                    print(f"Night charge added: {night_charge}")
                else:
                    print("Normal charge.")

        
    

    def get(self, request, id):
        try:
            get_all_inv = Invoice.objects.get(id=id)
            get_seri= InvoiceSerializer(get_all_inv)
            return Response({'msg': 'All invoice list', 'data':get_seri.data}, status=status.HTTP_200_OK)
        
        except Invoice.DoesNotExist:
            raise serializers.ValidationError("No Data Found")