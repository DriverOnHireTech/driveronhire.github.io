from django.urls import path

from . import views
from .extra_charges import ExtraRate
from .rate_logic import *

urlpatterns = [
    path('agent_booking/', views.Agentbookingview.as_view(), name='agent-booking'), #for CRM
    path('agent_booking_app/', views.AgentBookingApp.as_view(), name='agent-booking-app'), # this is for get request for mobile app
    path('agent_booking/<int:id>/', views.AgentDetailView.as_view(), name='agent-booking-id'),
    path('agent_booking_reschedule/<int:id>/', views.AgentBookingReshedule.as_view(), name='reshudle_booking'), # if driver cancel then booking float again
    path('agent_booking_accept/<int:id>/', views.Agentbooking_accept.as_view(), name='agent_booking_accept'),  # agent booking accept by driver
    path('agen_booking_status/', views.Agentbooking_bystatus.as_view(), name='agent_booking_status'),  # Get agent booking by status
    path('agent_booking_filter/', views.Agentbookingfilterquary.as_view(), name='agent_booking_filter'), # endpoint for filter CRM booking
    path('age_start_deuty/<int:id>/', views.Agentstartjourny.as_view(), name='agent_deuty_started'), # Using this endpoint deuty will start
    path('age_end_deuty/<int:id>/', views.Agentendjourny.as_view(), name='agent_deuty_end'),     # Deuty End api endpoint
    path('Acceptedride/<int:id>/', views.Acceptedride.as_view(), name='accepted-booking'), # Accept booking from website 
    path('allbooking/', views.getbooking.as_view(), name='all_booking'),
    path('all_declinebooking/', views.all_refuse_booking.as_view(), name='all_decilnebooking'), # This url will fetch all refuse booking
    path('all_locations/', views.AllZonedata.as_view(), name='all_location'), #All locatins new endpoint
    path('booking/', views.MyBookingList.as_view(), name='booking'),
    path('booking/<int:id>/', views.MyBookingList.as_view(), name='booking'),
    path('book_leter/', views.ScheduleBookingView.as_view(), name='book_leter'),
    path('bookingcount/', views.dashboardbooking.as_view(), name='bookingcounts'), #Endpoint for show booking counting at dashboard
    path('combine_data/', views.AllZoneData.as_view(), name='combine-data'), # this is for combining zone data that can show on pickup and drop location
    path('decline_booking/', views.declineplacebooking.as_view(), name='decline_booking'),
    path('deleteclinetbooking/<int:id>/', views.Agentbookingview.as_view(), name='delete'),
    path('driverlineup/', views.driverlineupplacebooking.as_view(), name='driver_lineup'),
    path('extra-rate/', ExtraRate.as_view(), name="extra_rate"), #Calculate Extra rates
    path('end_deuty/<int:id>/', views.endjourny.as_view(), name='deuty_end'), #Deuty End api endpoint website booking
    path('guestbooking/', views.Guestbookingapi.as_view(), name='guest_booking'),
    path('guestbooking/<int:id>/', views.SingleGuestbookingapi.as_view(), name="get_guest_booking"),
    path('invoice/', InvoiceGenerate.as_view(), name='invoice'), # invoice for placebooking
    path('invoice/<int:id>/', InvoiceGenerate.as_view(), name='get_invoice'),
    path('invoice_agent/', InvoiceGenerateAgent.as_view(), name='invoice-agent'), # Invoice for agent booking
    path('invoice_agent/<int:id>/', InvoiceGenerateAgent.as_view(), name='invoice-agent'), # Invoice for agent booking
    path('pendingbookings/', views.PendingBooking.as_view(), name='pendingbookings'),
    path('singlebooking/<int:id>/', views.get_bookingbyid.as_view(), name='single-booking'), # single Booking Get
    path('start_deuty/<int:id>/', views.startjourny.as_view(), name='deuty_started'), # Using this end deuty will start for website booking
    path('test_decline_booking/', views.TestDeclineBooking.as_view(), name="Test-decline-booking"), # testing for decline booking
    path('test_agent_decline_booking/', views.TestAgentDeclineBooking.as_view(), name="Test-agent-decline-booking"), # testing for agent decline booking
    path('userbooking/', views.BookingListWithId.as_view(), name='booking-id'), # Get logged user booking
    path('userbooking/<int:id>/', views.BookingListWithId.as_view(), name='booking-id'),
    path('UserFeedback/', views.FeedbackApi.as_view(), name='UserFeedback'),
    path('userprofile/', views.userprofile.as_view(), name='userprofile'),
    path('upcoming_booking/', views.UpcomingBooking.as_view(), name='upcoming_booking'),
    path('updaterecods/<int:id>/', views.Agentbookingview.as_view(), name='update_agentbooking'),  
]