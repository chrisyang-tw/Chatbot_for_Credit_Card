# coding: utf-8
import os
import json
from flask import Flask, request
from fbmq import Attachment, Template, QuickReply, Page
import csv
import random

##### 爬資料

####################################
##### 設置 webhook
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
page = Page(ACCESS_TOKEN)

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



####################################
##### 接收按鈕傳回的訊息
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    payload = event.postback_payload

    if payload == 'START_PAYLOAD':
        page.send(sender_id, '各位潮潮的菁英們，實習都已經賺了那麼多錢，是不是覺得沒地方花呢？想不想Bang成一個快樂的卡奴呢？',
                  quick_replies=[{'title': '想！', 'payload': 'Y'},
                                 {'title': '不想', 'payload': 'N'}])
    # if payload == 'ABC':
    #     page.send(sender_id, '早安我的朋友')
    # elif payload == 'DEF':
    #     page.send(sender_id, '晚安我的朋友')
    # elif payload == 'DEVELOPED_DEFINED_PAYLOAD':
    #     page.send(sender_id, '噫！好了！我中了！')

####################################
##### 開始訊息與菜單
page.greeting('想變卡奴找我們準沒錯！')

page.show_starting_button('START_PAYLOAD')

page.show_persistent_menu([Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                           Template.ButtonPostBack('開始使用', 'START_PAYLOAD'),
                           Template.ButtonPostBack('Undefined', 'MENU2')])

####################################
##### 
@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text

    ## 第一次判斷

    
    if message == '想':
        page.send(sender_id, '那讓我們開始吧！首先先問問你希望想擁有的信用卡特色？',
                  quick_replies=[{'title': '高額現金回饋', 'payload': 'cash'},
                                 {'title': '旅遊交通', 'payload': 'traffic'},
                                 {'title': '休閒娛樂', 'payload': 'entertain'},
                                 {'title': '購物', 'payload': 'shopping'},
                                 {'title': '電子支付功能', 'payload': 'easycard'},
                                 {'title': '宗教', 'payload': 'religion'}])
    elif message == '不想':
        page.send(sender_id, '相信我，卡奴也是可以過得很快樂的，給你最後一次機會，你想不想成為卡奴？',
                  quick_replies=[{'title':'想！', 'payload':'Y'}])

    ## 第二次判斷
    # sub_features = {'高額現金回饋': [{'title': '國內現金回饋', 'payload': 'in'},
    #                                 {'title': '國外現金回饋', 'payload': 'out'}],
    #                 '旅遊交通': [{'title': '里程累積', 'payload': 'meter'},
    #                             {'title': '旅遊優惠', 'payload': 'travel'},
    #                             {'title': '國外刷卡優惠', 'payload': 'outside'},
    #                             {'title': '高鐵', 'payload': 'hsr'},
    #                             {'title': '加油停車', 'payload': 'oil'},
    #                             {'title': 'eTag', 'payload': 'etag'}],
    #                 '休閒娛樂': [{'title': '美食', 'payload': 'food'},
    #                             {'title': '電影', 'payload': 'movie'}],
    #                 '購物': [{'title': '通路聯名', 'payload': 'chain'},
    #                         {'title': '網路購物', 'payload': 'shopee'}]
    #                 }
    
    # elif message in sub_features:
    #     page.send(sender_id, '再選擇一個子項目吧', quick_replies=sub_features[message])
    # if message == 'A':     
    #     buttons = [{'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
    #                {'type': 'postback', 'title': 'trigger Postback', 'value': 'DEVELOPED_DEFINED_PAYLOAD'},
    #                {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+886970119732'}]
    #     page.send(sender_id, Template.Buttons("hello", buttons))

    # ##### 圖片
    # elif message == 'B':
    #     page.send(sender_id, Attachment.Image('http://i.imgur.com/hKORBJK.jpg'))

    # ##### 快速回覆
    # elif message == 'C':
    #     quick_replies = [{'title': 'Action', 'payload': 'PICK_ACTION'},
    #                      {'title': 'Comedy', 'payload': 'PICK_COMEDY'}]
    #     page.send(sender_id, "What's your favorite movie genre?", quick_replies=quick_replies, metadata="DEVELOPER_DEFINED_METADATA")

    # ##### Generic Template
    # elif message == 'D':
    #     page.send(sender_id, Template.Generic([
    #             Template.GenericElement("rift",
    #                             subtitle="Next-generation virtual reality",
    #                             item_url="https://www.oculus.com/en-us/rift/",
    #                             # image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
    #                             image_url='http://i.imgur.com/hKORBJK.jpg',
    #                             buttons=[{'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
    #                                     {'type': 'postback', 'title': 'BANK A', 'value': 'ABC'},
    #                                     {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+886970119732'}]),
    #             Template.GenericElement("touch",
    #                             subtitle="Your Hands, Now in VR",
    #                             item_url="https://www.oculus.com/en-us/touch/",
    #                             image_url='http://i.imgur.com/hKORBJK.jpg',
    #                             buttons=[
    #                                     {'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
    #                                     {'type': 'postback', 'title': 'BANK B', 'value': 'DEF'},
    #                                     {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+886970119732'}])
    #     ]))
        
    ##### 鸚鵡
    else:
        page.send(sender_id, "你傳的訊息是 '%s'" % message)

####################################
@page.after_send
def after_send(payload, response):
    """:type payload: fbmq.Payload"""
    print("complete")

if __name__ == '__main__':
    app.run()