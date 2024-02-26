import requests
def gupshupwhatsapp(self, phone, dname,dmobile, bdate, btime, bfor):

    url= "https://media.smsgupshup.com/GatewayAPI/rest"   #https://media.smsgupshup.com/GatewayAPI/rest
    payload={
        "method":"SendMessage",
        "send_to":phone,
        "msg":"""Dear Customer Mr.{} Mobile -{} Will be arriving at your destination. Date -{} Time -{} Local {} hrs duty 
        Cost 800 rupees Extra hrs 100 rupees 11 pm to 6 am 200 traveling allowance 
        Our rates - https://www.driveronhire.com/rates 
        *T&C Apply https://www.driveronhire.com/privacy-policy&""".format(dname,dmobile,bdate, btime,bfor),
        "userid": "2000237293",
        "auth_scheme": "PLAIN",
        "password":"vrgnLDKp",
        "format": "JSON",
        "msg_type": "TEXT",
        "isTemplate":"true",
        "header":"Booking Details",
        "footer":"Thanks Driveronhire.com"
    }

    response = requests.post(url, data=payload)
    print("Response:", response)
    return response
