from django.db import models
from datetime import date
from user_master.models import State, City, Location, Branch, Zone
from django.utils.html import mark_safe
from django.contrib.auth.models import User

class AddDriver(models.Model):
    image_upload = models.ImageField(upload_to='images/%Y/%m/', default=None)

    def img_preview(self):
        return mark_safe(f'<img src = "{self.image_upload.url}" '
                         f'width = "100" height = "100" style = "border-radius: 50%"/>')

    # General Details
    first_name = models.CharField(max_length=20, default=None)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(choices=(('Male', "Male"), ('Female', "Female")), max_length=10, default="Male")
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15)
    alt_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
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
    qualification = models.CharField(choices=(('5', '5th'), ('6', '6th'), ('7', '7th'),
                                              ('8', '8th'), ('9', '9th'), ('SSC', 'SSC'), ('HSC', 'HSC'),
                                              ('BC', 'BCOM'), ('BS', 'BSc'), ('BE', 'BE'), ('BA', 'BA')),
                                     default="SS", max_length=10)
    driver_type = models.CharField(choices=(('Temporary', 'Temporary'), ('Permanent', 'Permanent')), default="Temporary", max_length=10)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    language = models.CharField(choices=(('Hindi', 'Hindi'), ('English', 'English'), ('Bhojpuri', 'Bhojpuri')), default="Hindi", max_length=10)

    # Address
    t_address = models.CharField(max_length=200)
    p_address = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10)
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
    passport = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10)
    passport_no = models.CharField(max_length=20, null=True, blank=True)
    heavy_vehicle = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10)
    car_transmission = models.CharField(choices=(("Manual", "Manual"), ("Automatic", "Automatic"), ("Luxury", "Luxury")), max_length=10)
    start_doh_date = models.DateField()
    end_doh_date = models.DateField()

    # Car Details
    car_company_name = models.CharField(max_length=15)
    transmission_type = models.CharField(choices=(("Manual", "Manual"), ("Automatic", "Automatic"), ("Luxury", "Luxury")), max_length=10)
    car_type = models.CharField(choices=(("SUV", "SUV"), ("Sedan", "Sedan"), ("Luxury", "Luxury"), ("Hatchback", "Hatchback"),
                                         ("MVP", "MPV"), ("MUV", "MUV")),
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
    relationship = models.CharField(max_length=20)
    member_name = models.CharField(max_length=20)
    approx_age = models.IntegerField()
    mobile_no = models.CharField(max_length=20)
    education_details = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
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
    police_verification = models.CharField(choices=(("Yes", "Yes"), ("No", "No")), max_length=10)
    week_off = models.CharField(choices=(("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"),
                                         ("Thursday", "Thursday"), ("Friday", "Friday"), ("Saturday", "Saturday"), ("Sunday", "Sunday")),
                                max_length=10)
    scheme_type = models.CharField(choices=(("Platinum", "Platinum"), ("Gold", "Gold"), ("Silver", "Silver")), max_length=10)
    driver_status = models.CharField(choices=(("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected"), ("Suspended", "Suspended")),max_length=10)


    def __str__(self):
        return self.first_name
    

class ViewDriver(models.Model):
    pass


class DriverHistory(models.Model):
    pass


class ReferDriver(models.Model):
    pass



class Driverleave(models.Model):
    reason=models.CharField(max_length=100, null=True, blank=True)
    leave_from_date=models.DateField()

    leave_to_date=models.DateField()
    total_days_of_leave= models.IntegerField()


    def __str__(self):
        return self.reason



class DriverBalance(models.Model):
    pass


class Driverlocation(models.Model):
    driver= models.ForeignKey(User, on_delete=models.CASCADE)
    driver_lat= models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    driver_long= models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return str(self.driver)