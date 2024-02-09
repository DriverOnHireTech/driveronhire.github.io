import random
import string
from django.conf import settings
from twilio.rest import Client  # Import the Twilio Client if using Twilio
import requests



def username_gene():
    phone=1234567
    generate=random.randint(0,phone)
    return generate

result= username_gene()

# Created function with 2 argument where its take to number&message 
def twilio_whatsapp(to_number, message):
    account_sid =settings.TWILIO_ACCOUNT_SID                            #'AC5c39741c6c06ec1915938a3065465e46' 
    auth_token =settings.TWILIO_AUTH_TOKEN                             #'a1715dfe516b118117334960626c30ca'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+918424054497',
    body=message,
    to=to_number
    )

    print(message.sid)
    

def generate_otp(length=4):
    # Generate a random OTP with the specified length (default is 6 digits)
    otp = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return otp


def twilio_message(to_number, message):
    account_sid = 'AC5c39741c6c06ec1915938a3065465e46'
    auth_token = 'a1715dfe516b118117334960626c30ca'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_='+12107141446',
        to=to_number
    )

    print(message.sid)

# Send OTP using infobip
# utils.py



def send_otp_via_infobip(phone_number, otp):
    api_key = settings.INFOBIP_API_KEY
    base_url = settings.INFOBIP_BASE_URL

    headers = {
        'Authorization': f'App {api_key}',
        'Content-Type': 'application/json',
    }

    message = f'Your OTP is: {otp}'

    payload = {
        'from': '447491163443',
        'to': phone_number,
        'text': message,
    }

    response = requests.post(base_url, json=payload, headers=headers)

    return response.json()

# # Gupshup service
def gupshupWhatsapp(phone, msg):
    url = "https://enterprise.smsgupshup.com/GatewayAPI/rest"
    payload =f"method=sendMessage&send_to=91{phone}&msg={msg}\
            GupShup&msg_type=TEXT&userid=setting.user_id&auth_scheme=PLAIN&settings.password=vrgnLDKp&format=JSON"
    response = requests.request("POST", url, data=payload)
    print(response.text)
    return response
    
