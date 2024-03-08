from django.urls import path
from .views import *

urlpatterns = [
    path('country/', MyCountryList.as_view(), name='country_list'),
    path('country/<str:pk>/', MyCountryGetList.as_view(), name='country-list-id'),
    path('state/', MyStateList.as_view(), name='state_list'),
    path('state/<str:pk>/', MyStateGetList.as_view(), name='state-list-id'),
    path('city/', MyCityList.as_view(), name='city_list'),
    path('city/<str:pk>/', MyCityGetList.as_view(), name='city-list-id'),
    path('location/', MyLocationList.as_view(), name='location_list'),
    path('location/<int:id>/', MyLocationGetList.as_view(), name='location-list-id'),
    path('zone/', MyZoneList.as_view(), name='Zone-list'),
    path('zone/<int:id>/', MyZoneGetList.as_view(), name='Zone-list-id'),
    path('branch/', MyBranchList.as_view(), name='branch_list'),
    path('branch/<int:id>/', MyBranchGetList.as_view(), name='branch-list-id'),
    path('reference/', MyReferenceList.as_view(), name='reference_list'),
    path('reference/<int:id>', MyReferenceGetList.as_view(), name='reference-list-id'),
    path('tax/', MyTaxList.as_view(), name='tax_list'),
    path('tax/<int:id>/', MyTaxGetList.as_view(), name='tax-list-id'),
    path('car/', MyCarList.as_view(), name='car_list'),
    path('car/<int:id>/', MyCarGetList.as_view(), name='car-list-id'),
    path('coupon/', MyCouponList.as_view(), name='coupon_list'),
    path('coupon/<int:id>/', MyCouponGetList.as_view(), name='coupon-list-id'),
    path('subscription/', MySubscriptionList.as_view(), name='subscription_list'),
    path('subscription/<int:id>/', MySubscriptionGetList.as_view(), name='subscription-list-id'),
    path('region/', Regionapi.as_view(), name='region'),
    
    # Charges 
    path('twohrs/', twohrscharges.as_view(), name='two_hrs_charges'),
    path('fourhrscharges/', fourhrscharges.as_view(), name='four_hrs_charges'),

    # URL for User
    path('createuser/', createUsermaster.as_view(), name='createuser'),
    # path('login/', Loginuser.as_view(), name='login'),
]
