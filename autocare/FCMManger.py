import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("C:\Users\MAVERICK\Documents\HRMS\AutoCareCar\autocare\auto-car-care-30970-firebase-adminsdk-pjaom-b8e0909aec.json")
firebase_admin.initialize_app(cred)

def sendPush(title, msg, registration_token, dataObject=None):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObject,
        tokens=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)