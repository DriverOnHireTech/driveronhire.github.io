from django.contrib import admin
from .models import *


# class AddDriverImage(admin.ModelAdmin):
#     readonly_fields = ['img_preview']
#     list_display = ['img_preview', 'first_name', 'last_name']
#     fieldsets = (
#         ('General Details', {
#             'fields': ('image_upload',
#                        ('driver_type', 'branch', 'zone', 'language'),
#                        ('qualification', 'first_name', 'middle_name', 'last_name'),
#                        ('sex', 'date_of_birth', 'mobile', 'alt_mobile'),
#                        ('email', 'marital_status', 'religion', 'cast', ))
#         }),
#         ('Temporary Address', {
#             'fields': ('t_address', ('state', 'city', 'location', 'pincode'), 'aggrement_expiry_date')
#         }),
#         ('Permanent Address', {
#             'fields': ('p_address', )
#         }),
#         ('Licence Information', {
#             'fields': (('licence_no', 'licence_issued_from', 'licence_type'), ('date_of_issue', 'date_of_expiry'))
#         }),
#         ('Driver Screening', {
#             'fields': (('present_salary', 'expected_salary', 'pan_card_no', 'aadhar_card_no'),
#                        ('blood_group', 'passport', 'passport_no', 'heavy_vehicle'),
#                        ('car_transmission', 'start_doh_date', 'end_doh_date'))
#         }),
#         ('Car Details', {
#             'fields': (('car_company_name', 'transmission_type', 'car_type', 'driven_km'),)
#         }),
#         ('Attach Documents', {
#             'fields': (('driving_licence', 'ration_card', 'pan_card'),
#                        ('light_bill', 'aadhar_card', 'home_agreement', 'affidavit'))
#         }),
#         ('Previous Employment Details', {
#             'fields': (('company_name', 'address_location', 'contact_person', 'worked_from', 'worked_till'),
#                        ('monthly_salary', 'reason_for_leaving', 'car_driven'))
#         }),
#         ('Family Neighbour History', {
#             'fields': (('relationship', 'member_name', 'approx_age', 'mobile_no'),
#                        ('education_details', 'address', 'reference'))
#         }),
#         ('Driver Status Update', {
#             'fields': (('schedule_training', 'training_date', 'training_status', 'Purchase_uniform'),
#                        ('scheduled_driving_test', 'driving_test_date', 'driving_status', 'is_approval_done'),
#                        ('police_verification', 'week_off', 'scheme_type', 'driver_status'))
#         })
#     )
admin.site.register(BasicDetail)
admin.site.register(ViewDriver)
admin.site.register(AddDriver)
admin.site.register(DriverHistory)
admin.site.register(ReferDriver)
admin.site.register(Driverleave)
admin.site.register(DriverBalance)
admin.site.register(Driverlocation)