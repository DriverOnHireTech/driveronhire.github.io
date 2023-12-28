from django.contrib import admin
from .models import *


admin.site.register(PlaceBooking)
admin.site.register(Invoice)
admin.site.register(Feedback)
admin.site.register(userProfile)
admin.site.register(BookLater)
admin.site.register(Notifydrivers)
admin.site.register(GuestBooking)
admin.site.register(Zone)

class Addfavoritedriveradmin(admin.ModelAdmin):
    fields=['user', 'driver_name', 'add_favorite']

admin.site.register(AddfavoriteDriver, Addfavoritedriveradmin)


admin.site.register(AgentBooking)