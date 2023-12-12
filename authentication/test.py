import requests
def send_otp_via_infobip(phone_number, otp):
    # api_key = settings.INFOBIP_API_KEY
    # base_url = settings.INFOBIP_BASE_URL
    INFOBIP_BASE_URL = "https://vv1yd1.api.infobip.com"
    INFOBIP_API_KEY = "1f9d940b581346389b8b853128de460c-b4c1a547-e85a-42d2-b32f-5ef8696765d0"


    headers = {
        'Authorization': f'App {INFOBIP_API_KEY}',
        'Content-Type': 'application/json',
    }

    message = f'Your OTP is: {otp}'

    payload = {
        'from': '447491163443',
        'to': phone_number,
        'text': message,
    }

    response =requests.post(INFOBIP_BASE_URL, json=payload, headers=headers)
    # print("response",response)

    return response.json()

sms=send_otp_via_infobip("919657847644", "2345")
print("message send:", sms)