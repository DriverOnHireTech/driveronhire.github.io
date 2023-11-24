from django.urls import path
from . import views
# from djoser.views import (
#     TokenCreateView, TokenRefreshView, TokenDestroyView, UserCreateView, UserDeleteView, UserDetailView
# )
from rest_framework.authtoken.views import obtain_auth_token 


urlpatterns = [
    path('adduser/', views.Adduser.as_view(), name='adduser'),
    path('adduser/<int:id>/', views.Adduser.as_view(), name='resetpassword'),
    path('adduser/<int:id>/', views.Adduser.as_view(), name='delete'),
    path('login/',views.LoginView.as_view(), name="login"),
    path('logout/', views.Logoutapi.as_view(), name='logout'),
    path('token-auth/', obtain_auth_token, name='api_token_auth'),  
    path('generate_otp/', views.SendOTPAPIView.as_view(), name='generate_otp'),
    path('validate_otp/', views.VerifyOTPAPIView.as_view(), name='validate_otp'),
    path('delete/<int:id>/', views.Adduser.as_view(), name="Delete-user"),
]