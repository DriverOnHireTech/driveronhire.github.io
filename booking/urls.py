from django.urls import path

from . import views

urlpatterns = [

    path('booking/', views.MyBookingList.as_view(), name='booking'),

    path('allbooking/', views.getbooking.as_view(), name='all_booking'),

    path('book_leter/', views.ScheduleBookingView.as_view(), name='book_leter'),

    path('userbooking/', views.BookingListWithId.as_view(), name='booking-id'), # Get logged user booking

    path('userbooking/<int:id>/', views.BookingListWithId.as_view(), name='booking-id'),

    path('singlebooking/<int:id>/', views.get_bookingbyid.as_view(), name='single-booking'), # single Booking Get

    path('Acceptedride/<int:id>/', views.Acceptedride.as_view(), name='accepted-booking'),

    path('invoce/', views.InvoiceGenerate.as_view(), name='invoice'),

    path('UserFeedback/', views.FeedbackApi.as_view(), name='UserFeedback'),

    path('userprofile/', views.userprofile.as_view(), name='userprofile'),

    path('pendingbookings/', views.PendingBooking.as_view(), name='pendingbookings'),

    path('upcoming_booking/', views.UpcomingBooking.as_view(), name='upcoming_booking'),

    path('agent_booking/', views.Agentbookingview.as_view(), name='agent-booking'),

    path('agent_booking/<int:id>/', views.AgentDetailView.as_view(), name='agent-booking-id'),

    path('updaterecods/<int:id>/', views.Agentbookingview.as_view(), name='update_agentbooking'),

    path('deleteclinetbooking/<int:id>/', views.Agentbookingview.as_view(), name='delete'),

    path('agen_booking_status/', views.Agentbooking_bystatus.as_view(), name='agent_booking_status'),

    path('driverlineup/', views.driverlineupplacebooking.as_view(), name='driver_lineup'),

    path('guestbooking/', views.Guestbookingapi.as_view(), name='guest_booking'),

    path('guestbooking/<int:id>/', views.SingleGuestbookingapi.as_view(), name="get_guest_booking"),
]