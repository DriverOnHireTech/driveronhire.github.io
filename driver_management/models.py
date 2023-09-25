"""
Driver management models
"""
# from datetime import date
from django.db import models
# from django.utils.html import mark_safe
from django.contrib.gis.db import models as gis_point
from user_master.models import region

from django.conf import settings
from user_master.models import State, City, Branch, Zone, Location

# from user_master.models import region
# from booking.models import PlaceBooking


class BasicDetail(models.Model):
    """ Basic details model """
    image_upload = models.ImageField(upload_to='media', default=None)
    first_name = models.CharField(max_length=20, default=None)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True, default="Male")
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15, unique=True)
    alt_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    religion = models.CharField(max_length=30, null=True, blank=True)
    qualification = models.CharField(default="SS", max_length=20, null=True, blank=True)
    language = models.CharField(default="Hindi", max_length=100, null=True, blank=True)
      # Address
    temp_address = models.CharField(max_length=200)
    permanent_address = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10, null=True,blank=True)
    aggrement_expiry_date = models.DateField(null=True, blank=True)

    # Licence Information
    licence_no = models.CharField(max_length=20)
    licence_issued_from = models.CharField(max_length=20)
    licence_type = models.CharField(max_length=20, null=True, blank=True)
    date_of_issue = models.DateField()
    date_of_expiry = models.DateField()

    def __str__(self):
        return str(self.mobile)


class BgVerification(models.Model):
    """Model for background verification """
    driver_number = models.OneToOneField(BasicDetail, on_delete=models.CASCADE)
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
    driver_number = models.OneToOneField(BasicDetail, on_delete=models.CASCADE)
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


class AddDriver(models.Model):
    """Add driver model"""
    image_upload = models.ImageField(upload_to='media', default=None)
    # General Details
    #driver_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default=None)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(
        choices=(('Male', "Male"), ('Female', "Female")),
        max_length=10,
        default="Male"
    )
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15)
    alt_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(default="info@driveronhire.com")
    
    marital_status = models.CharField(choices=(('Married', 'Married'), ('Single', 'Single')),
                                      max_length=10)
    religion = models.CharField(choices=(('Hindu', 'Hindu'), ('Muslim', 'Muslim'),
                                         ('Christian', 'Christian'), ('Sikh', 'Sikh')),
                                max_length=10)
    cast = models.CharField(choices=(('Marathi', 'Marathi'),
                                     ('Muslim', 'Muslim'), ('Gujrati', 'Gujarati'),
                                     ('SO', 'SouthIndian'), ('Punjabi', 'Punjabi'),
                                     ('UP', 'UP'), ('Bihari', 'Bihari'), ('Other', 'Other')),
                            max_length=20,
                            default='MA')
    region= models.CharField(max_length=200, null=True, blank=True)
    
    qualification = models.CharField(choices=(('5', '5th'), ('6', '6th'), ('7', '7th'),
                                              ('8', '8th'), ('9', '9th'), ('SSC', 'SSC'), ('HSC', 'HSC'),
                                              ('BC', 'BCOM'), ('BS', 'BSc'), ('BE', 'BE'), ('BA', 'BA')),
                                     default="SS", max_length=10)
    driver_type = models.CharField(choices=(('Part Time', 'Part Time'), ('Full Time', 'Full Time')), max_length=10)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True,blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True,blank=True)
    language = models.CharField(choices=(('Hindi', 'Hindi'), ('English', 'English'), ('Bhojpuri', 'Bhojpuri')), default="Hindi", max_length=100)

    # Address
    t_address = models.CharField(max_length=200)
    p_address = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10, null=True,blank=True)
    aggrement_expiry_date = models.DateField()

    # Licence Information
    licence_no = models.CharField(max_length=20)
    licence_issued_from = models.CharField(max_length=20)
    licence_type = models.CharField(choices=(('LMV-TR', 'LMV-TR'), ('LMV-NT', 'LMV-NT')), default="TR", max_length=10)
    date_of_issue = models.DateField()
    date_of_expiry = models.DateField()

    # Driver Screening
    present_salary = models.FloatField(null=True, blank=True)
    expected_salary = models.FloatField()
    pan_card_no = models.CharField(max_length=15, blank=True, null=True)
    aadhar_card_no = models.CharField(max_length=20)
    blood_group = models.CharField(choices=(("O+", "O+"), ("O-", "O-"), ("A+", "A+"), ("A-", "A-"), ("B+", "B+"),
                                            ("B-", "B-"), ("AB+", "AB+"), ("AB-", "AB-")),
                                   max_length=10)
    passport = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10,null=True,blank=True)
    passport_no = models.CharField(max_length=20, null=True, blank=True)
    heavy_vehicle = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10, null=True,blank=True)
    car_transmission = models.CharField(choices=(("Manual", "Manual"), ("Automatic", "Automatic"), ("Luxury", "Luxury")), max_length=10)
    start_doh_date = models.DateField()
    # end_doh_date = models.DateField(null=True, blank=True)

    # Car Details
    car_company_name = models.CharField(max_length=15, null=True,blank=True)
    transmission_type = models.CharField(choices=(("Manual", "Manual"), ("Automatic", "Automatic"), ("Luxury", "Luxury"), ('All', 'All')), max_length=10)
    car_type = models.CharField(choices=(("SUV", "SUV"), ("Sedan", "Sedan"), ("Luxury", "Luxury"), ("Hatchback", "Hatchback"),
                                         ("MPV", "MPV"), ("MUV", "MUV")),
                                max_length=10)
    driven_km = models.FloatField()

    # Attach Document
    driving_licence = models.FileField(upload_to='documents/%Y/%m/', default=None)
    ration_card = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    pan_card = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    light_bill = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    aadhar_card = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    home_agreement = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    affidavit = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)
    pcc_certificate = models.FileField(upload_to='documents/%Y/%m/', default=None, null=True, blank=True)

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

    # Driver status update
    schedule_training = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10)
    training_date = models.DateField()
    training_status = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10)
    Purchase_uniform = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10)
    scheduled_driving_test = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10)
    driving_test_date = models.DateField()
    driving_status = models.CharField(choices=(("Approve", "Approve"), ("Reject", "Reject")), max_length=10)
    is_approval_done = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10)
    police_verification = models.CharField(choices=(("Processing", "Processing"), ("Certified", "Certified"), ("Rejected", "Rejected")), max_length=10)
    week_off = models.CharField(choices=(("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"),
                                         ("Thursday", "Thursday"), ("Friday", "Friday"), ("Saturday", "Saturday"), ("Sunday", "Sunday")),
                                max_length=10)
    scheme_type = models.CharField(choices=(("Platinum", "Platinum"), ("Gold", "Gold"), ("Silver", "Silver")), max_length=10)
    driver_status = models.CharField(choices=(("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected"), ("Suspended", "Suspended")),max_length=10)
    driver_rating= models.PositiveBigIntegerField()

    driverlocation = gis_point.PointField(
        "Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(longitude latitude)")

    def __str__(self):
        return self.first_name


class ViewDriver(models.Model):
    """This is for viewing driver"""


# class Bookingstatus(models.Model):
#     STATUS=(
#         ('accept','accept'),
#         ('decline', 'decline'),
#         ('pending', 'pending'),
#         ('completed', 'completed')
#     )
#     #booking_details = models.ForeignKey(PlaceBooking, on_delete=models.CASCADE)
#     drivername= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     booking_status= models.CharField(choices=STATUS, max_length=50, null=True, blank=True)


class ReferDriver(models.Model):
    """Refer driver class"""
    referdrivername= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name= models.CharField(max_length=100, null=True, blank=True)
    mobile = models.PositiveBigIntegerField()
    location= models.CharField(max_length=200, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def save(self):
        pass

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
    # driver_details = models.ForeignKey(AddDriver, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.driver.phone)
