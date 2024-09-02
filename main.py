from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()  # Get the message body and convert to lowercase
    resp = MessagingResponse()

    if 'abc' in incoming_msg:
        resp.message("ABC")
    else:
        # Do nothing
        pass

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
