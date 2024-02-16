from django.urls import path
from . import views

urlpatterns =[
    path('userprofile/',views.Userprofileview.as_view(),name='profile'), # it will get logged user profile also 
    path('userprofileupdate/<int:id>/', views.Userprofileview.as_view(), name='profileupdate')
    
] 