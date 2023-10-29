# import firebase_admin
# from firebase_admin import messaging, credentials
# from base_site import settings


# cred = credentials.Certificate(settings.cred_path)
# firebase_admin.initialize_app(cred)

# def sendnotifications(trip_type,pickup_location,drop_location):
#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(trip_type=trip_type, pickup_location=pickup_location)
#     )

#     response = messaging.send_multicast(message)
#     print("Notification sent", response)


from twilio.rest import Client

# Your Twilio Account SID and Auth Token
account_sid = 'ACc1850c4cded33db1f98cd2219826ef66'
auth_token = "0ebe4b5681598dd871ac2e3239959957"

def send_whatsapp_message(to_number, message):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_='whatsapp:+919657847644',
        to=f'whatsapp:{to_number}'
    )

    print(f"WhatsApp message sent with SID: {message.sid}")

send=send_whatsapp_message(+917045630679, "Hi Abhishek")
