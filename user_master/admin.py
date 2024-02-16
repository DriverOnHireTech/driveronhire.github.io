from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

admin.site.site_header = 'Driver On Hire'


@admin.register(UserMaster)
class UserMaster(admin.ModelAdmin):
    list_display = ("user_name", "mobile", "email_id", "password","branch", "role", "status", "edit_option", "delete_option")
    search_fields = ("user_name__startswith", "mobile", "status")
    fields = ("user_name", "mobile", "email_id","password", ("branch", "role", "status"))
    # list_editable = ['email_id']

    def edit_option(self, obj):
        return format_html('<a class="btn" href="/admin/usermaster/usermaster/{}/change/">Edit</a>', obj.user_id)

    def delete_option(self, obj):
        return format_html('<a class="btn" href="/admin/usermaster/usermaster/{}/delete/">Delete</a>', obj.user_id)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(UserMaster, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False
        return formfield


@admin.register(Country)
class Country(admin.ModelAdmin):
    list_display = ("country_name", "country_code", "status")
    search_fields = ("country_name",)
    fields = (("country_code", "country_name", "status"),)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(Country, self).change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(State)
class State(admin.ModelAdmin):
    list_display = ("state", "state_code", "country", "status")
    search_fields = ("state",)
    fields = (("country", "state", "state_code", "status"),)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(State, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False
        return formfield


@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ("city", "city_code", "state", "country", "status")
    search_fields = ("city",)
    fields = (("country", "state"), ("city", "city_code", "status"))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(City, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False
        return formfield


@admin.register(Location)
class Location(admin.ModelAdmin):
    list_display = ("location", "city", "state", "country", "status")
    search_fields = ("location",)
    fields = (("country", "state"), ("city", "location", "status"))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(Location, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False
        return formfield


@admin.register(Branch)
class Branch(admin.ModelAdmin):
    list_display = ("branch_name", "branch_address", "branch_pin", "branch_contact", "city", "state", "country", "zone", "status")
    search_fields = ["branch_name", "branch_address", "branch_pin", "branch_contact"]
    fields = (("branch_name", "branch_address"), ("branch_pin", "branch_contact"), ("country", "state"), ("zone", "city", "status"))

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False  # can change this, too
        formfield.widget.can_view_related = False  # can change this, too
        return formfield

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(Branch, self).change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Zone)
class Zone(admin.ModelAdmin):
    list_display = ("zone_name", "city", "state", "country", "status")
    search_fields = ("zone_name",)
    fields = ("zone_name", ("country", "state"), ("city", "status"))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(Zone, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False
        return formfield


@admin.register(Reference)
class Reference(admin.ModelAdmin):
    list_display = ("reference_name", "status")
    search_fields = ("reference_name",)
    fields = (("reference_name", "status"),)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(Reference, self).change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Tax)
class Tax(admin.ModelAdmin):
    list_display = ("tax_name", "gst_rate", "cgst", "sgst", "igst", "cess", "status")
    search_fields = ("tax_name", "gst_rate", "cgst", "sgst", "igst", "cess")
    fields = (("tax_name", "gst_rate", "cgst"), ("sgst", "igst", "cess", "status"))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(Tax, self).change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Car)
class Car(admin.ModelAdmin):
    list_display = ("car_company", "car_model", "car_type", "car_transmission", "status")
    search_fields = ("car_company", "car_model", "car_type", "car_transmission")
    fields = (("car_company", "car_model"), ("car_type", "car_transmission", "status"))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(Car, self).change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(CouponList)
class CouponList(admin.ModelAdmin):
    list_display = ("booking_list", "coupon_name", "coupon_code", "discount_amount", "use_count", "valid_from", "valid_till", "status")
    search_fields = ("booking_list", "coupon_name", "coupon_code", "valid_from", "valid_till", "use_count")
    fields = (("booking_list", "coupon_name", "coupon_code"), ("discount_amount", "use_count"), ("valid_from", "valid_till", "status"))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(CouponList, self).change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    list_display = ("scheme_type", "duty_type", "car_transmission", "amount", "validity_in_days", "no_of_duties", "tax", "status")
    search_fields = ("scheme_type", "duty_type", "car_transmission", "amount", "validity_in_days", "no_of_duties")
    fields = (("scheme_type", "duty_type", "car_transmission"), ("amount", "validity_in_days", "no_of_duties", "tax", "status"))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(Subscription, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False
        return formfield

admin.site.register(region)

class loclatwohrsadmin(admin.ModelAdmin):
    list_display=("cartype", "charge", "perour_ot", "night_allownce", "drop_location_change")
admin.site.register(localtwohrscharges,loclatwohrsadmin)

class AdminZoneA(admin.ModelAdmin):
    list_display=('location', 'pincode')
admin.site.register(ZoneA,AdminZoneA)

class AdminZoneB(admin.ModelAdmin):
    list_display=('location', 'pincode')
admin.site.register(ZoneB,AdminZoneB)

class AdminZoneC(admin.ModelAdmin):
    list_display=('location', 'pincode')
admin.site.register(ZoneC,AdminZoneC)

class AdminZoneD(admin.ModelAdmin):
    list_display=('location', 'pincode')
admin.site.register(ZoneD,AdminZoneD)

class AdminZoneE(admin.ModelAdmin):
    list_display=('location', 'pincode')
admin.site.register(ZoneE,AdminZoneE)

class AdminZoneF(admin.ModelAdmin):
    list_display=('location', 'pincode')
admin.site.register(ZoneF,AdminZoneF)

class AdminZoneG(admin.ModelAdmin):
    list_display=('location', 'pincode')
admin.site.register(ZoneG,AdminZoneG)

admin.site.register(localfourhrscharges)
admin.site.register(localeigthhrscharges)
admin.site.register(out_stn_sday_returncharges)
admin.site.register(out_stn_charges_stay)

"""For Pune Locations"""
admin.site.register(pune_A_location)
admin.site.register(pune_B_location)
"""Pune Location End"""
admin.site.register(citylocation)

