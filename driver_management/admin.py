from django.contrib import admin
from .models import *

admin.site.register(BasicDetail)

admin.site.register(ReferDriver)
admin.site.register(Driverleave)
admin.site.register(DriverBalance)
admin.site.register(Driverlocation)



class Adddriveradmin(admin.ModelAdmin):
    list_display=['id','first_name','mobile', 'driver_type', 'scheme_type']
    list_filter=['mobile', 'driver_type', 'scheme_type', 'first_name']

admin.site.register(AddDriver, Adddriveradmin)


class Driverappstatusadmin(admin.ModelAdmin):
    list_display=['driver_name', 'package', 'paymentamount', 'is_paid', 'status']
admin.site.register(Driverappstatus, Driverappstatusadmin)


