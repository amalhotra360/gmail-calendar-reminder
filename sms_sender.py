from twilio.rest import Client

# Replace these with your actual Twilio credentials
TWILIO_SID = "+18777804236"
TWILIO_AUTH = "your_auth_token_here"
TWILIO_FROM = "+1your_twilio_number"

def send_sms(to, message):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    message = client.messages.create(
        body=message,
        from_=TWILIO_FROM,
        to=to
    )
    print(f"✅ SMS sent! SID: {message.sid}")
