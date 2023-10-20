from django.conf import settings
from django.core.mail import send_mail



def sendemail(phone_number, message):
    email = send_mail(phone_number, message,[settings.EMAIL_HOST_USER], fail_silently=False)
    print("Email has sent:",email)
    return email
