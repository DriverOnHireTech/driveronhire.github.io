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

# account_sid = 'AC14ad4a6275663b2aeb6b65e0fb8211cb'
# auth_token = '[0ebe4b5681598dd871ac2e3239959957]'
# client = Client(account_sid, auth_token)

# message = client.messages.create(
#   from_='whatsapp:+14155238886',
#   body='Your Twilio code is 1238432',
#   to='whatsapp:+919657847644'
# )

# print(message.sid)
