#Python libraries that we need to import for our bot
import os
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

def send_quick(recipient_id, message_text):
    params = {
           "access_token": ACCESS_TOKEN
    }

    headers = {
            "Content-Type": "application/json"
    }

    data = json.dumps({
               "recipient": {
                      "id": recipient_id
               },
               "message": {
                  "text": message_text
                  "quick_replies":[{
                            "content_type":"text",
                            "title":"Search",
                            "payload":"Search",
                            },
                            {
                             "content_type":"text",
                             "title":"Something Else",
                             "payload":"Something Else"
                             }
                   ]
               }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        # Before allowing people to message your bot, Facebook has implemented a verify token that confirms all requests that your bot receives came from Facebook.""" 
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'
    
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    if request.method == 'POST':
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for m in messaging:
                if m.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = m['sender']['id']
                    if m['message'].get('text'):
                        message = m['message']['text']
                        if message == 'Mail':
                            bot.send_button_message(recipient_id, message, [
                                {
                                    'type':'web_url',
                                    'url':'https://mail.ntu.edu.tw',
                                    'title':'NTU Mail'
                                },
                                {
                                    'type':'postback',
                                    'title':'NTUGALA',
                                    'payload':'NTUGALA'
                                }
                            ])
                        elif message == '母湯':
                            send_quick(recipient_id, message)
                            # bot.send_text_message(recipient_id, '幹')
                        # bot.send_text_message(recipient_id, message)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    else:
                        bot.send_text_message(recipient_id, 'BANG')
                    
                else:
                    pass
        return 'Success'

if __name__ == "__main__":
    app.run()