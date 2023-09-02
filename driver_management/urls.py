from django.urls import path

from .views import *

urlpatterns = [
    path('api/signup', Driversignup.as_view(), name='driver-signup'),

    path('api/login', Driverlogin.as_view(), name='driver-login'),

    path('api/driver/', MyDriverList.as_view(), name='driver-list'),

    path('api/driver_location/', driverlocation.as_view(), name= 'driver-locationupdate'),

    path('api/driver_location/<int:id>/', driverlocation.as_view()),

    path('api/driverprofile/', Driverprofile.as_view(), name='driverprofile'),

    # path('api/driver/<int:id>/', MyDriverGetList.as_view(), name='driver-list-id'),

    path('api/search/', Driversearch.as_view(), name='search_driver'),

    

    path('api/driverleave/', Driverleaveapi.as_view(), name='driver_leave'),
]