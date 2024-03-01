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
def gupshupsms(self, phone, otp):
    url = "https://enterprise.smsgupshup.com/GatewayAPI/rest"
    payload = {
        "method": "sendMessage",
        "send_to": phone,
        "msg": """Your OTP is {} for booking a driver from driveronhire""".format(otp),
        "msg_type": "TEXT",
        "userid": "2000142458",
        "auth_scheme": "PLAIN",
        "password": "9892098920",
        "format": "JSON"
    }

    response = requests.post(url, data=payload)
    return print("OTP sent")

#Booking confirmantion 
def driverdetailssent(self, userphone,drivername, drivernumber):
    url = "https://enterprise.smsgupshup.com/GatewayAPI/rest"
    payload = {
        "method": "sendMessage",
        "send_to": userphone,
        "msg": """Driver Details, Driver name-{} Mob no-{} Would arrive at ur destination on ur mentioned date & time.
Driveronhire
""".format(drivername,drivernumber),
        "msg_type": "TEXT",
        "userid": "2000142458",
        "auth_scheme": "PLAIN",
        "password": "9892098920",
        "format": "JSON"
    }

    response = requests.post(url, data=payload)
    return response

def agnbookingpro(self, phone, to_date, start_time):
    url = "https://enterprise.smsgupshup.com/GatewayAPI/rest"
    payload = {
        "method": "sendMessage",
        "send_to": phone,
        "msg": """Dear Customer, Your booking for {} at {} has been processed, we will share the driver details shortly. Driveronhire.""".format(to_date,start_time),
        "msg_type": "TEXT",
        "userid": "2000142458",
        "auth_scheme": "PLAIN",
        "password": "9892098920",
        "format": "JSON"
    }

    response = requests.post(url, data=payload)
    print("reponse agnet:", response.json())
    return response

"""
https://media.smsgupshup.com/GatewayAPI/rest?userid=2000237293&password=vrgnLDKp&send_to=919372792693&v=1.1&format=json&msg_type=TEXT&method=SENDMESSAGE&msg=Dear+Customer%2C%0A%0AMr.Satish%0AMobile+-+9657847644%0AWill+be+arriving+at+your+destination.%0A%0ADate+-12-03-2024%0ATime+-4%3A00+pm%0ALocal+4+hrs+duty%0ACost++800+rupees%0AExtra+hrs+100+rupees%0A11+pm+to+6+am+200+traveling+allowance+%0A%0AOur+rates+-+https%3A%2F%2Fwww.driveronhire.com%2Frates%0A%0A%2AT%26C+Apply%0Ahttps%3A%2F%2Fwww.driveronhire.com%2Fprivacy-policy&isTemplate=true&header=Booking+Details&footer=Thanks++Driveronhire.com
"""



#Gupshup whatsapp function
def gupshupwhatsapp(self, to_number, dname, dnumber, bdate, btime, bhrs,charge):
    url= "http://media.smsgupshup.com/GatewayAPI/rest"   #https://media.smsgupshup.com/GatewayAPI/rest
    payload={
        "userid":"2000237293",
        "password":"vrgnLDKp",
        "send_to":f"91{to_number}",
        "v":"1.1",
        "format":"json",
        "msg_type":"TEXT",
        "method":"SendMessage",
        "template_id":"6916349",
        "var1":dname,
        "var2":dnumber,
        "var3":bdate,
        "var4":btime,
        "var5":bhrs,
        "var6":charge,
        "isTemplate":"true",
        "header":"Booking Details",
        "footer":"Thanks  Driveronhire.com"
    }
    response = requests.post(url, data=payload)
    return response
