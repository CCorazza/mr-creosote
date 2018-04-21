import random
import os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET', 'POST'])


def receive_message():
    if request.method == 'GET':
        #Verify Token by FB
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
    # getting message from user
       output = request.get_json()
       log(output)
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = create_answer()
                    send_message(recipient_id, response_sent_text)
                if message['message'].get('attachments'):
                # in case message is an attachment and not text
                    response_sent_nontext = create_answer()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def create_answer():
    sample_responses = ["Fetch me a bucket!"
                        , "No mint, thank you."
                        , "Be a gourmet"
                        , "You need to eat, son"]
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print datetime.now + msg
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
sys.stdout.flush()

if __name__ == "__main__":
    app.run()
