from twilio.rest import Client

account_sid="your account Sid"
auth_token="your auth token"

client = Client(account_sid,auth_token)

def send_notification(phone_number):
    message = client.messages.create(
        body="An ambulance is approaching the area where you are currently driving. It is crucial to ensure a clear path for the ambulance to pass through swiftly and safely",
        from_="+18067311789",
        to=str(phone_number)
    )
