from django.contrib import admin
from .models import *

admin.site.register(BasicDetail)
admin.site.register(ViewDriver)
admin.site.register(AddDriver)
# admin.site.register(Bookingstatus)
admin.site.register(ReferDriver)
admin.site.register(Driverleave)
admin.site.register(DriverBalance)
admin.site.register(Driverlocation)

class Driverappstatusadmin(admin.ModelAdmin):
    fields=['drivername', 'package', 'paymentamount', 'is_paid', 'status']
admin.site.register(Driverappstatus, Driverappstatusadmin)


