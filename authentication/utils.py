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
def twilio_whatsapp(message_body, to_number):
    account_sid = 'AC5c39741c6c06ec1915938a3065465e46'
    auth_token = 'a1715dfe516b118117334960626c30ca'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=message_body,
    to=to_number
    )

    print(message.sid)
