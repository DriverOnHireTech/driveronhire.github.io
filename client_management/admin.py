from django.contrib import admin
from .models import AddClient, UserCar, UserProfile

admin.site.register(AddClient)
admin.site.register(UserCar)
admin.site.register(UserProfile)