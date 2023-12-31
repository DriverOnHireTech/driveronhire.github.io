from django.urls import path

from . import views
from .extra_charges import ExtraRate

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

    path('agent_booking_app/', views.AgentBookingApp.as_view(), name='agent-booking-app'), # this is for get request for mobile app

    path('agent_booking/<int:id>/', views.AgentDetailView.as_view(), name='agent-booking-id'),

    path('updaterecods/<int:id>/', views.Agentbookingview.as_view(), name='update_agentbooking'),

    path('deleteclinetbooking/<int:id>/', views.Agentbookingview.as_view(), name='delete'),

    path('agen_booking_status/', views.Agentbooking_bystatus.as_view(), name='agent_booking_status'),  # Get agent booking by status

    path('driverlineup/', views.driverlineupplacebooking.as_view(), name='driver_lineup'),

    path('guestbooking/', views.Guestbookingapi.as_view(), name='guest_booking'),

    path('guestbooking/<int:id>/', views.SingleGuestbookingapi.as_view(), name="get_guest_booking"),

    path('combine_data/', views.AllZoneData.as_view(), name='combine-data'), # this is for combining zone data that can show on pickup and drop location

    path('extra-rate/', ExtraRate.as_view(), name="extra_rate"),

    path('start_deuty/<int:id>/', views.startjourny.as_view(), name='deuty_started'), # Using this end deuty will start

    path('end_deuty/<int:id>/', views.endjourny.as_view(), name='deuty_end') #Deuty End api endpoint
]