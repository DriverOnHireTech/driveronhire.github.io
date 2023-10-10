import random
import string
from django.conf import settings
from twilio.rest import Client  # Import the Twilio Client if using Twilio


def username_gene(phone):
    phone=123456789
    generate=random.randint(0,phone)
    return generate

result= username_gene(12365478)


# def generate_otp(length=4):
#     characters = string.digits
#     otp = ''.join(random.choice(characters) for _ in range(length))
#     return otp

# def send_otp_phone(phone_number, otp):
#     account_sid = 'AC6131c8aa6b776f8b0cfb9c05bd1af0dc'  # Replace with your Twilio account SID
#     auth_token = 'b893c17c59715ee9b35a29f12c7772c3'  # Replace with your Twilio auth token
#     twilio_phone_number = '+13203616540'  # Replace with your Twilio phone number

#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         body=f'Your OTP is: {otp}',
#         from_=twilio_phone_number,
#         to=phone_number
#     )