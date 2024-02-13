"""
Driver management models
"""
# from datetime import date
from django.db import models
# from django.utils.html import mark_safe
from django.contrib.gis.db import models as gis_point
from user_master.models import region
from django.utils import timezone
from django.conf import settings
from user_master.models import State, City, Branch, Zone, Location
from multiselectfield import MultiSelectField
from django.db.models.signals import pre_save
from django.dispatch import receiver

# from user_master.models import region
# from booking.models import PlaceBooking

TRANSMISSION_OPTIONS=(('Manual', 'Manual'), ('Automatic', 'Automatic'), ('Luxury', 'Luxury'))
CAR_OPTIONS=(('SUV', 'SUV'), ('Sedan', 'Sedan'), ('Luxury', 'Luxury'), ('Hatchback', 'Hatchback'),('MPV', 'MPV'), ('MUV', 'MUV'), ('Sedan Luxury', 'Sedan Luxury'), ('SUV Luxury','SUV Luxury'))


class AddDriverNew(models.Model):
    """ Driver adding new model """
    first_name = models.CharField(max_length=30, default=None, null=True, blank=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True, default="Male")
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    alt_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    religion = models.CharField(max_length=30, null=True, blank=True)
    qualification = models.CharField(default="SS", max_length=20, null=True, blank=True)
    language = models.CharField(default="Hindi", max_length=100, null=True, blank=True)
      # Address
    temp_address = models.CharField(max_length=200, null=True, blank=True)
    permanent_address = models.CharField(max_length=200, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True,blank=True)
    aggrement_expiry_date = models.DateField(null=True, blank=True)
    transmission_type = MultiSelectField(choices=TRANSMISSION_OPTIONS, max_length=500, null=True, blank=True)
    car_type = MultiSelectField(choices=CAR_OPTIONS, max_length=500, null=True, blank=True)

    # Licence Information
    licence_no = models.CharField(max_length=20, null=True, blank=True)
    licence_issued_from = models.CharField(max_length=20, null=True, blank=True)
    licence_type = models.CharField(max_length=20, null=True, blank=True)
    date_of_issue = models.DateField(null=True, blank=True)
    date_of_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.mobile)


class BgVerification(models.Model):
    """Model for background verification """
    driver_number = models.OneToOneField(AddDriverNew, on_delete=models.CASCADE)
    pan_card_no = models.CharField(max_length=15, blank=True, null=True)
    aadhar_card_no = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=10)
    passport = models.CharField(max_length=10,null=True,blank=True)
    passport_no = models.CharField(max_length=20, null=True, blank=True)
    heavy_vehicle = models.CharField(max_length=10, null=True,blank=True)
    car_transmission = models.CharField(max_length=10)
    start_doh_date = models.DateField()

    # Car Details
    car_company_name = models.CharField(max_length=15, null=True,blank=True)
    transmission_type = models.CharField(max_length=10)
    car_type = models.CharField(max_length=10)
    driven_km = models.FloatField()

    # Attach Document
    driving_licence = models.FileField(
        upload_to='documents/%Y/%m/',
        default=None
    )
    ration_card = models.FileField(
        upload_to='documents/%Y/%m/',
        default=None,
        null=True,
        blank=True
    )
    pan_card = models.FileField(
        upload_to='documents/%Y/%m/',
        default=None,
        null=True,
        blank=True
    )
    light_bill = models.FileField(
        upload_to='documents/%Y/%m/',
        default=None,
        null=True,
        blank=True
    )
    aadhar_card = models.FileField(
        upload_to='documents/%Y/%m/',
        default=None,
        null=True,
        blank=True
    )
    home_agreement = models.FileField(
        upload_to='documents/%Y/%m/',
        default=None,
        null=True,
        blank=True
    )
    affidavit = models.FileField(
        upload_to='documents/%Y/%m/',
        default=None,
        null=True,
        blank=True
    )

    # Previous Employment details
    company_name = models.CharField(max_length=30)
    address_location = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=20)
    worked_from = models.DateField()
    worked_till = models.DateField()
    monthly_salary = models.FloatField()
    reason_for_leaving = models.CharField(max_length=30)
    car_driven = models.CharField(max_length=20)

    # Family/Neighbour history detail
    relationship = models.CharField(max_length=100)
    member_name = models.CharField(max_length=100)
    approx_age = models.IntegerField()
    mobile_no = models.CharField(max_length=20)
    education_details = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    reference = models.CharField(max_length=15)


class RmVerification(models.Model):
    """RM verification model"""
    driver_number = models.OneToOneField(AddDriverNew, on_delete=models.CASCADE)
    pcc_certificate = models.FileField(
        upload_to='documents/%Y/%m/',
        default=None,
        null=True,
        blank=True
    )
    driver_type = models.CharField(max_length=15)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    region = models.CharField(max_length=30)
    car_transmission = models.CharField(max_length=20)

    # Driver status update
    schedule_training = models.CharField(max_length=10)
    training_date = models.DateField()
    training_status = models.CharField(max_length=10)
    Purchase_uniform = models.CharField(max_length=10)
    scheduled_driving_test = models.CharField(max_length=10)
    driving_test_date = models.DateField()
    driving_status = models.CharField(max_length=10)
    is_approval_done = models.CharField(max_length=10)
    police_verification = models.CharField(max_length=10)
    week_off = models.CharField(max_length=10)
    scheme_type = models.CharField(max_length=10)
    driver_status = models.CharField(max_length=10)
    driver_rating= models.PositiveBigIntegerField()




transmission_option=(("Manual", "Manual"), ("Automatic", "Automatic"), ("Luxury", "Luxury"))
car_option=(("SUV", "SUV"), ("Sedan", "Sedan"), ("Luxury", "Luxury"), 
            ("Hatchback", "Hatchback"),("MPV", "MPV"), ("MUV", "MUV"),
              ("Sedan Luxury", "Sedan Luxury"), ("SUV Luxury","SUV Luxury"))


class AddDriver(models.Model):
    """Add driver model"""
    image_upload = models.ImageField(upload_to='media', default=None, blank=True, null=True)
    # General Details
    driver_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, default=None)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(
        choices=(('Male', "Male"), ('Female', "Female")),
        max_length=10,
        default="Male",
        blank=True, null=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    alt_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(default="info@driveronhire.com", blank=True, null=True)
    
    marital_status = models.CharField(choices=(('Married', 'Married'), ('Single', 'Single')),
                                      max_length=10, blank=True, null=True)
    religion = models.CharField(choices=(('Hindu', 'Hindu'), ('Muslim', 'Muslim'),
                                         ('Christian', 'Christian'), ('Sikh', 'Sikh')),
                                max_length=10, blank=True, null=True)
    cast = models.CharField(choices=(('Marathi', 'Marathi'),
                                     ('Muslim', 'Muslim'), ('Gujrati', 'Gujarati'),
                                     ('SO', 'SouthIndian'), ('Punjabi', 'Punjabi'),
                                     ('UP', 'UP'), ('Bihari', 'Bihari'), ('Other', 'Other')),
                            max_length=20,
                            default='MA', blank=True, null=True)
    region= models.CharField(max_length=200, null=True, blank=True)
    
    qualification = models.CharField(choices=(('5', '5th'), ('6', '6th'), ('7', '7th'),
                                              ('8', '8th'), ('9', '9th'), ('SSC', 'SSC'), ('HSC', 'HSC'),
                                              ('BC', 'BCOM'), ('BS', 'BSc'), ('BE', 'BE'), ('BA', 'BA')),
                                     default="SS", max_length=10, blank=True, null=True)
    driver_type = models.CharField(choices=(('Part Time', 'Part Time'), ('Full Time', 'Full Time')), max_length=10, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True,blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True,blank=True)
    language = models.CharField(choices=(('Hindi', 'Hindi'), ('English', 'English'), ('Bhojpuri', 'Bhojpuri')), default="Hindi", max_length=100, blank=True, null=True)

    # Address
    t_address = models.CharField(max_length=200, null=True, blank=True)
    p_address = models.CharField(max_length=200, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True,blank=True)
    aggrement_expiry_date = models.DateField(blank=True, null=True)

    # Licence Information
    licence_no = models.CharField(max_length=100, blank=True, null=True)
    licence_issued_from = models.CharField(max_length=100, null=True, blank=True)
    licence_type = models.CharField(choices=(('LMV-TR', 'LMV-TR'), ('LMV-NT', 'LMV-NT')), default="TR", max_length=10, blank=True, null=True)
    date_of_issue = models.DateField(blank=True, null=True)
    date_of_expiry = models.DateField(blank=True, null=True)

    # Driver Screening
    present_salary = models.FloatField(null=True, blank=True)
    expected_salary = models.FloatField(blank=True, null=True)
    pan_card_no = models.CharField(max_length=100, blank=True, null=True)
    aadhar_card_no = models.CharField(max_length=100)
    blood_group = models.CharField(choices=(("O+", "O+"), ("O-", "O-"), ("A+", "A+"), ("A-", "A-"), ("B+", "B+"),("B-", "B-"), ("AB+", "AB+"), ("AB-", "AB-")), max_length=10, blank=True, null=True)
    passport = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10,null=True,blank=True)
    passport_no = models.CharField(max_length=100, null=True, blank=True)
    heavy_vehicle = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10, null=True,blank=True)
    car_transmission = models.CharField(choices=(("Manual", "Manual"), ("Automatic", "Automatic"), ("Luxury", "Luxury")), max_length=10, blank=True, null=True)
    start_doh_date = models.DateField(blank=True, null=True)
    

    # Car Details
    car_company_name = models.CharField(max_length=100, null=True,blank=True)
    transmission_type = MultiSelectField(choices=transmission_option, max_length=500, null=True, blank=True)
    car_type = MultiSelectField(choices=car_option, max_length=500, null=True, blank=True)
    driven_km = models.FloatField(blank=True, null=True)

    # Attach Document
    driving_licence = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    ration_card = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    pan_card = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    light_bill = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    aadhar_card = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    home_agreement = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    affidavit = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    pcc_certificate = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)

    # Previous Employment details
    company_name = models.CharField(max_length=30, blank=True, null=True)
    address_location = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=20, blank=True, null=True)
    worked_from = models.DateField(blank=True, null=True)
    worked_till = models.DateField(blank=True, null=True)
    monthly_salary = models.FloatField(blank=True, null=True)
    reason_for_leaving = models.CharField(max_length=30, blank=True, null=True)
    car_driven = models.CharField(max_length=20, blank=True, null=True)

    # Family/Neighbour history detail
    relationship = models.CharField(max_length=100, blank=True, null=True)
    member_name = models.CharField(max_length=100, blank=True, null=True)
    approx_age = models.IntegerField(blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    education_details = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    reference = models.CharField(max_length=15, blank=True, null=True)

    # Driver status update
    schedule_training = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10, blank=True, null=True)
    training_date = models.DateField(blank=True, null=True)
    training_status = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10, blank=True, null=True)
    Purchase_uniform = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10, blank=True, null=True)
    scheduled_driving_test = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10,blank=True, null=True)
    driving_test_date = models.DateField(blank=True, null=True)
    driving_status = models.CharField(choices=(("Approve", "Approve"), ("Reject", "Reject")), max_length=10, blank=True, null=True)
    is_approval_done = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10, blank=True, null=True)
    police_verification = models.CharField(choices=(("Processing", "Processing"), ("Certified", "Certified"), ("Rejected", "Rejected")), max_length=10, blank=True, null=True)
    week_off = models.CharField(choices=(("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"),
                                         ("Thursday", "Thursday"), ("Friday", "Friday"), ("Saturday", "Saturday"), ("Sunday", "Sunday")),
                                max_length=10, blank=True, null=True)
    scheme_type = models.CharField(choices=(("Platinum", "Platinum"), ("Gold", "Gold"), ("Silver", "Silver"), ("Diwali", "Diwali"), ("Gold2", "Gold2"), ("Platinum2", "Platinum2"), ("Bronze", "Bronze")), max_length=10, blank=True, null=True)
    driver_status = models.CharField(choices=(("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected"), ("Suspended", "Suspended")),max_length=10, blank=True, null=True)
    driver_rating= models.PositiveBigIntegerField(blank=True, null=True)

    driverlocation = gis_point.PointField(
        "Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(latitude longitude)")
    total_exp=models.IntegerField(null=True, blank=True)
    #driver_app_status=models.ForeignKey(Driverappstatus, on_delete=models.CASCADE, null=True, blank=True)
    driver_update_date= models.DateField(auto_now_add=True, null=True,blank=True)
    has_received_notification = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.first_name


"""Driver App Status"""
class Driverappstatus(models.Model):
    PACKAGE=(("Gold", "Gold"),("Gold2", "Gold2"),("Platinium", "Platinium"), ("Platinium2", "Platinium2"), ("Bronze", "Bronze"), ("silver", "silver"),("DiwaliScheme", "DiwaliScheme"))
    Status=(('active','active'), ('inactive', 'inactive'))
    driver_name=models.ForeignKey(AddDriver ,on_delete=models.CASCADE,null=True, blank=True)
    # driver_
    driverusername=models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE,null=True, blank=True)
    driver_name1=models.CharField(max_length=100, null=True, blank=True)
    driver_mobile = models.CharField(max_length=100, null=True, blank=True)
    package=models.CharField(choices=PACKAGE,max_length=100, null=True, blank=True)
    paymentamount=models.BigIntegerField(null=True, blank=True)
    tax_amount=models.BigIntegerField(null=True, blank=True)
    total_amount_paid=models.BigIntegerField(null=True, blank=True)
    is_paid=models.BooleanField(null=True, blank=True, default=False)
    status=models.CharField(choices=Status, max_length=100, null=True, blank=True)
    recharge_date=models.DateField(auto_now_add=False,null=True, blank=True)
    expiry_date=models.DateField(auto_now_add=False,null=True, blank=True)


    def __str__(self):
        return str(self.is_paid)
    
# Define the signal receiver function to update status
@receiver(pre_save, sender=Driverappstatus)
def update_package_status(sender, instance, **kwargs):
    # Check if the expiry date has passed and the status is active
    if instance.expiry_date and instance.expiry_date < timezone.now().date() and instance.status == 'active':
        # If conditions met, update status to inactive
        instance.status = 'inactive'

"""End App Status"""

class ReferDriver(models.Model):
    """Refer driver class"""
    referdrivername= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name= models.CharField(max_length=100, null=True, blank=True)
    mobile = models.PositiveBigIntegerField()
    location= models.CharField(max_length=200, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Driverleave(models.Model):
    """Driver leave class"""
    STATUS_CHOICES = (('Pending', 'Pending'),('Accepted', 'Accepted'),('Rejected', 'Rejected'),
    )

    driver_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason=models.CharField(max_length=100, null=True, blank=True)
    leave_from_date=models.DateField()
    leave_to_date=models.DateField()
    total_days_of_leave= models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending') 

    def __str__(self):
        return f'{self.reason}'


class DriverBalance(models.Model):
    """Driver Balance class"""


class Driverlocation(models.Model):
    """ Class for driver Location """
    driver= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driverlocation = gis_point.PointField(
        "Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(longitude latitude)")
    
    def __str__(self):
        return str(self.driver.phone)


