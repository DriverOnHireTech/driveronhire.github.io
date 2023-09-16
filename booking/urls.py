from django.urls import path

from . import views

urlpatterns=[
    path('userregistration/', views.userregistration.as_view(), name='userregistration'),

    path('userlogin/', views.Userlogin.as_view()),

    path('booking/', views.MyBookingList.as_view(), name='booking'),

    path('userbooking/<int:id>/', views.BookingListWithId.as_view(), name='booking-id'),

    path('invoce/', views.InvoiceGenerate.as_view(), name='invoice'),

    path('UserFeedback/', views.FeedbackApi.as_view(), name='UserFeedback'),

    path('userprofile/', views.userprofile.as_view(), name='userprofile'),

    path('pendingbookings/', views.PendingBooking.as_view(), name='pendingbookings'),

    path('userprofile/<int:id>/', views.UserProfileWithId.as_view(), name='user-id'),
]