from twilio.rest import Client

account_sid="AC6f4f732526c69a332a6ebdd590c937d7"
auth_token="1e180840185f16f7323b6be71050e438"

client = Client(account_sid,auth_token)

# Phone number map
phone_map = {
    "car_1": {
        "phone":"+918529622974",
        "message":"An ambulance is approaching towards you in the area where you are currently driving. It is crucial to ensure a clear path for the ambulance to pass through swiftly and safely"
        },
    "car_2": {
        "phone":"+919993074778",
        "message":"An ambulance is approaching towards you in the area where you are currently driving. It is crucial to ensure a clear path for the ambulance to pass through swiftly and safely"
        },
    "car_3":{"phone":"",
             "message":"An ambulance is approaching from the left turn in the area you're driving. It is crucial to ensure a clear path for the ambulance to pass through swiftly and safely"
             },
    "car_4":{"phone":"",
             "message":"An ambulance is approaching from the right in the area you're driving. It is crucial to ensure a clear path for the ambulance to pass through swiftly and safely"
             }
}

def send_notification(car):
    client.messages.create(
        body=phone_map[car]["message"],
        from_="+12566678158",
        to=str(phone_map[car]["phone"])
    )
