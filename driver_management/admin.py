from django.contrib import admin
from .models import *

admin.site.register(BasicDetail)
admin.site.register(ViewDriver)
# admin.site.register(AddDriver)
# admin.site.register(Bookingstatus)
admin.site.register(ReferDriver)
admin.site.register(Driverleave)
admin.site.register(DriverBalance)
admin.site.register(Driverlocation)



class Adddriveradmin(admin.AdminSite):
    fields=['first_name','driver_type', 'mobile']
    list_filter=('mobile')

admin.site.register(AddDriver, Adddriveradmin)


class Driverappstatusadmin(admin.ModelAdmin):
    fields=['drivername', 'package', 'paymentamount', 'is_paid', 'status']
admin.site.register(Driverappstatus, Driverappstatusadmin)


