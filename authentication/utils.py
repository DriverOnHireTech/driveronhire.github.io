import random
import string
from django.conf import settings
from twilio.rest import Client  # Import the Twilio Client if using Twilio


def username_gene():
    phone=1234567
    generate=random.randint(0,phone)
    return generate

result= username_gene()

# 
def twilio_whatsapp(self, message_body, to_number):
    account_sid = 'AC6131c8aa6b776f8b0cfb9c05bd1af0dc'
    auth_token = 'b893c17c59715ee9b35a29f12c7772c3'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=message_body,
    to=to_number
    )

    print(message.sid)
