from django.contrib import admin
from .models import User
# # Register your models here.

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['usertype', 'phone']
    list_filter=['phone']

admin.site.register(User, LogEntryAdmin)