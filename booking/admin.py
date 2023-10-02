from django.contrib import admin
from .models import *


admin.site.register(PlaceBooking)
admin.site.register(Invoice)
admin.site.register(Feedback)
admin.site.register(Profile)

class Addfavoritedriveradmin(admin.ModelAdmin):
    fields=['user', 'driver_name', 'add_favorite']

admin.site.register(AddfavoriteDriver, Addfavoritedriveradmin)

