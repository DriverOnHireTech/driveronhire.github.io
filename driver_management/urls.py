from django.urls import path

from .views import *

urlpatterns = [
    path('basic_detail/', BasicDetailView.as_view(), name='basic details'),

    path('api/driver/', MyDriverList.as_view(), name='driver-list'),

    path('api/get_single_driver/<int:id>/', getsingledriver.as_view(), name='get_sigle_driver'),

    path('all_drivers/', Getalldrivers.as_view(), name='all_drivers_list'),

    path('api/updatedriver/', updatedriver.as_view(), name='update_driver'),

    path('api/updatedriver/<int:id>/', updatedriverwithid.as_view(), name='update_driver_with_id'),

    path('api/driver_location', driverlocation.as_view(), name= 'driver-locationupdate'),

    path('api/driverprofile/', Driverprofile.as_view(), name='driverprofile'), # Driver Profile

    path('api/driverprofile/<int:id>/', Driverprofile.as_view(), name='delete_driverprofile'),

    path('api/search_driver/', Driversearch.as_view(), name='search_driver'),

    path('api/driverleave/', Driverleaveapi.as_view(), name='driver_leave'),

    path('api/booking_report/', Bookingreports.as_view(), name="booking_report"),

    path('api/driverrefer/', DriverreferView.as_view(), name='driver_refer'), 

    path('api/Driverappstatus/', DriverappstatusView.as_view(), name='driver_status'),

    path('api/scheme/', driverpackageapi.as_view(), name='driver_scheme'), # Get logged driver Scheme details

    path('api/UserWithDriver/', DriverWIthUserFilter.as_view(), name='driver_with_user'),
]
