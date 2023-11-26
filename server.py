from twilio.rest import Client

account_sid="AC6f4f732526c69a332a6ebdd590c937d7"
auth_token="3091d4c88c51d11570c650e0aaf7c9b3"

client = Client(account_sid,auth_token)

def send_notification(phone_number):
    message = client.messages.create(
        body="An ambulance is approaching the area where you are currently driving. It is crucial to ensure a clear path for the ambulance to pass through swiftly and safely",
        from_="+18067311789",
        to=str(phone_number)
    )