from twilio.rest import Client

# Preset values:
accountSID = ''
authToken = ''
myTwilioNumber = ''
myCellPhone = ''


def textmyself(message):
    twilioCli = Client(accountSID, authToken)
    message = twilioCli.messages.create(body=message, from_=myTwilioNumber, to=myCellPhone)

    print(message.status)

    return None
