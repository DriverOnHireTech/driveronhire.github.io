import random
import string
from django.conf import settings
from twilio.rest import Client  # Import the Twilio Client if using Twilio


def username_gene():
    phone=123456789
    generate=random.randint(0,phone)
    return generate

result= username_gene()
