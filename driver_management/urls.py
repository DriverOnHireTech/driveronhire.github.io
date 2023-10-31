from django.urls import path

from .views import *

urlpatterns = [
    path('basic_detail/', BasicDetailView.as_view(), name='basic details'),

    path('api/driver/', MyDriverList.as_view(), name='driver-list'),

    path('api/updatedriver/<int:id>/', updatedriver.as_view(), name='update_driver'),

    path('api/driver_location', driverlocation.as_view(), name= 'driver-locationupdate'),

    path('api/driverprofile/', Driverprofile.as_view(), name='driverprofile'), # Driver Profile


    path('api/search_driver/', Driversearch.as_view(), name='search_driver'),

    path('api/driverleave/', Driverleaveapi.as_view(), name='driver_leave'),

    path('api/booking_report/', Bookingreports.as_view(), name="booking_report"),

    path('api/driverrefer/', DriverreferView.as_view(), name='driver_refer'), 

    path('api/Driverappstatus/', DriverappstatusView.as_view(), name='driver_status'),
]