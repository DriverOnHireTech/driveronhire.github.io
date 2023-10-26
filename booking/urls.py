from django.urls import path

from . import views

urlpatterns = [

    path('booking/', views.MyBookingList.as_view(), name='booking'),

    path('book_leter/', views.ScheduleBookingView.as_view(), name='book_leter'),

    path('userbooking/<int:id>/', views.BookingListWithId.as_view(), name='booking-id'),

    path('Acceptedride/<int:id>/', views.Acceptedride.as_view(), name='accepted-booking'),

    path('invoce/', views.InvoiceGenerate.as_view(), name='invoice'),

    path('UserFeedback/', views.FeedbackApi.as_view(), name='UserFeedback'),

    path('userprofile/', views.userprofile.as_view(), name='userprofile'),

    path('pendingbookings/', views.PendingBooking.as_view(), name='pendingbookings'),

    path('userprofile/<int:id>/', views.UserProfileWithId.as_view(), name='user-id'),

    path('upcoming_booking/', views.UpcomingBooking.as_view(), name='upcoming_booking'),

    path('agent_booking/', views.Agentbookingview.as_view(), name='agent-booking'),

    path('updaterecods/<int:id>/', views.Agentbookingview.as_view(), name='update_agentbooking'),

    path('deleteclinetbooking/<int:id>/', views.Agentbookingview.as_view(), name='delete'),

    path('driverlineup/', views.driverlineupplacebooking.as_view(), name='driver_lineup'),
]