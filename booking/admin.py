from django.contrib import admin
from .models import *



#admin.site.register(Invoice)
admin.site.register(Feedback)
admin.site.register(userProfile)
admin.site.register(BookLater)

admin.site.register(NotifydriversAgent)
admin.site.register(GuestBooking)
admin.site.register(Zone)
admin.site.register(Invoice)



class Placebookingadmin(admin.ModelAdmin):
    list_display=['id','user', 'booking_date','booking_type', 'packege', 'trip_type','user_address','car_type','pickup_location', 'drop_location', 'status']
    list_filter=['id','user', 'status', 'trip_type']

admin.site.register(PlaceBooking, Placebookingadmin)

class Addfavoritedriveradmin(admin.ModelAdmin):
    fields=['user', 'driver_name', 'add_favorite']

admin.site.register(AddfavoriteDriver, Addfavoritedriveradmin)

class DeclineplaceagnebookingAdmin(admin.ModelAdmin):
    list_display=['id', 'placebooking',  'refuse_driver_user', 'refuse_time']

admin.site.register(Declinebooking,DeclineplaceagnebookingAdmin)

class Decline1PlaceBooking(admin.ModelAdmin):
    fields=['placebooking', 'refuse_driver_user']

admin.site.register(Declinebooking1, Decline1PlaceBooking)

class Placebookingnotisent(admin.ModelAdmin):
    list_display=['id','user', 'place_booking']

admin.site.register(Notifydrivers, Placebookingnotisent)

admin.site.register(AgentBooking)