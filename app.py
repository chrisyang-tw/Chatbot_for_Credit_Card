# coding: utf-8
import os
import json
from flask import Flask, request
from fbmq import Attachment, Template, QuickReply, Page

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
page = Page(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET'])
def hello():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return 'Invalid verification token'

@app.route('/', methods=['POST'])
def webhook():
    page.handle_webhook(request.get_data(as_text=True))
    return "ok"

####################################

@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text
    if message == 'A':     
        buttons = [{'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
                {'type': 'postback', 'title': 'trigger Postback', 'value': 'DEVELOPED_DEFINED_PAYLOAD'},
                {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+886970119732'}]
        page.send(sender_id, Template.Buttons("hello", buttons))
    elif message == 'B':
        page.send(sender_id, Attachment.Image('http://i.imgur.com/hKORBJK.jpg'))
    elif message == 'C':
        quick_replies = [
            QuickReply(title="Action", payload="PICK_ACTION"),
            QuickReply(title="Comedy", payload="PICK_COMEDY")
        ]
        page.send(sender_id, "What's your favorite movie genre?", quick_replies=quick_replies, metadata="DEVELOPER_DEFINED_METADATA")
    else:
        page.send(sender_id, "你傳的訊息是 '%s'" % message)

@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    print("complete")

if __name__ == '__main__':
    app.run()