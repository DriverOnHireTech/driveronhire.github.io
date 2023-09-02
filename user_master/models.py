from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password


class Country(models.Model):
    country_code = models.CharField(max_length=5, primary_key=True)
    country_name = models.CharField(max_length=30, unique=True)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = "Country"
        verbose_name_plural = "Country"

    def __str__(self):
        return self.country_code


class State(models.Model):
    state_code = models.CharField(max_length=30, primary_key=True)
    state = models.CharField(max_length=30, unique=True)
    country = models.ForeignKey(Country, to_field='country_code', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("State")
        verbose_name_plural = "State"

    def __str__(self):
        return self.state


class City(models.Model):
    city_code = models.CharField(max_length=5, primary_key=True)
    city = models.CharField(max_length=30, unique=True)
    state = models.ForeignKey(State, to_field='state', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, to_field='country_code', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = "City"
        verbose_name_plural = "City"

    def __str__(self):
        return self.city


class Location(models.Model):
    location = models.CharField(max_length=30)
    city = models.ForeignKey(City, to_field='city', on_delete=models.CASCADE)
    state = models.ForeignKey(State, to_field='state', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, to_field='country_code', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("Location")
        verbose_name_plural = "Location"

    def __str__(self):
        return self.location


class Zone(models.Model):
    zone_name = models.CharField(max_length=30, unique=True)
    city = models.ForeignKey(City, to_field='city', on_delete=models.CASCADE)
    state = models.ForeignKey(State, to_field='state', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, to_field='country_code', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("Zone")
        verbose_name_plural = "Zone"

    def __str__(self):
        return self.zone_name


class Branch(models.Model):
    country = models.ForeignKey(Country, to_field='country_code', on_delete=models.CASCADE)
    state = models.ForeignKey(State, to_field='state', on_delete=models.CASCADE)
    city = models.ForeignKey(City, to_field='city', on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=30, unique=True)
    branch_address = models.CharField(max_length=100)
    branch_pin = models.CharField(max_length=10)
    branch_contact = models.CharField(max_length=20)
    zone = models.ForeignKey(Zone, to_field='zone_name', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("Branch")
        verbose_name_plural = "Branch"

    def __str__(self):
        return self.branch_name


class UserMaster(models.Model):
    user_role =( 
    ("Admin", "Admin"), 
    ("Temprory", "Temprory"), 
    ("Permanent", "Permanent"),
    ("Recruit", "Recruit") 
  )
  
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    password=models.CharField(max_length=300, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email_id = models.EmailField(max_length=50, null=True, blank=True)
    branch = models.ForeignKey(Branch, to_field='branch_name', on_delete=models.CASCADE)
    # role = models.ForeignKey(Group, on_delete=models.CASCADE)
    role=models.CharField(choices=user_role, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = "User Master"
        verbose_name_plural = "User Master"
        permissions = (
           ("view_UserMaster", "Can view the UserMaster"),
           ("can_publish_UserMaster", "Can publish a UserMaster"),
     )
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        
        super(UserMaster, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_name


class ZoneMapping(models.Model):
    zone = models.ForeignKey(Zone, to_field='zone_name', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, to_field='country_code', on_delete=models.CASCADE)
    state = models.ForeignKey(State, to_field='state', on_delete=models.CASCADE)
    city = models.ForeignKey(City, to_field='city', on_delete=models.CASCADE)

    class Meta:
        # verbose_name = ("Zone Mapping")
        verbose_name_plural = "Zone Mapping"


class Reference(models.Model):
    reference_name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("Reference")
        verbose_name_plural = "Reference"

    def __str__(self):
        return self.reference_name


class Tax(models.Model):
    tax_name = models.CharField(max_length=50, unique=True)
    gst_rate = models.FloatField()
    cgst = models.FloatField()
    sgst = models.FloatField()
    igst = models.FloatField()
    cess = models.FloatField()
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("Tax")
        verbose_name_plural = "Tax"

    def __str__(self):
        return self.tax_name


car_transmission_type = (
    (1, 'Manual'),
    (2, 'Automatic'),
    (3, 'Luxury')
)


class Car(models.Model):
    car_company = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50)
    car_transmission = models.IntegerField(choices=car_transmission_type)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("Car")
        verbose_name_plural = "Car"

    def __str__(self):
        return self.car_company 


booking_type_list = (
    (1, "Local"),
    (2, "Drop"),
    (3, "Outstation"),
    (4, "Permanent")
)


class CouponList(models.Model):
    booking_list = models.IntegerField(choices=booking_type_list)
    coupon_name = models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=50)
    discount_amount = models.FloatField()
    use_count = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_till = models.DateTimeField()
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("Coupon List")
        verbose_name_plural = "Coupon List"
        
    def __str__(self):
        return self.coupon_name


duty_list = (
    (1, "Day"),
    (2, "Drop"),
    (3, "Night"),
    (4, "Outstation")
)


class Subscription(models.Model):
    scheme_type = models.CharField(max_length=50)
    duty_type = models.IntegerField(choices=duty_list)
    car_transmission = models.IntegerField(choices=car_transmission_type)
    amount = models.FloatField()
    validity_in_days = models.IntegerField()
    no_of_duties = models.IntegerField()
    tax = models.ForeignKey(Tax, to_field='tax_name', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        # verbose_name = ("Subscription")
        verbose_name_plural = "Subscription"

    def __str__(self):
        return self.scheme_type
    

class region(models.Model):
    region_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.region_name
    
