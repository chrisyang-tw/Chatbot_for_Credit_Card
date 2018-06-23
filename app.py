# coding: utf-8
import os
import json
from flask import Flask, request
from fbmq import Attachment, Template, QuickReply, Page
import csv
import random

# def cal1():
#     # 開啟 CSV 檔案
#     data = "/Users/chiaa/Desktop/money101.csv"
#     csvfile = open(data, mode='r', encoding='utf-8')
#     next(csvfile)
#     rows = csv.reader(csvfile)
#     answer = []
#     for row in rows:
#         #print (row[5])
#         if '里程累積' in row[5]:
#             answer +=[row]
#     number = []
#     answer1 = []
#     for i in range(0,len(answer)):
#         number.append(i)
#     random.shuffle(number)
#     #print(number)
#     for  i in range(0,len(answer)):
#         answer1.append(answer[number[i]])
#     #print(answer1)
#     answer1 = sorted(answer1, key=lambda y: answer[14], reverse=True)
#     answerstr =''
#     if len(answer1) >= 5:
#         for i in range(0,5):
#             answerstr += answer1[i][1]+answer1[i][2]+'\n'
#             #showinfo(answer1[i][1]+answer1[i][2],"信用卡名:"+answer1[i][1]+answer1[i][2]+"\n"+"\n"+"國內現金回饋："+answer1[i][3]+"\n"+"\n"+"國外現金回饋："+answer1[i][4]+"\n"+"\n"+"優惠內容："+answer1[i][6]
#             #+"\n"+"\n"+"優惠限制："+answer1[i][7]+"\n"+"\n"+"首刷禮："+answer1[i][8]+"\n"+"\n"+"首刷活動："+answer1[i][9]+"\n"+"\n"+"手續費："+answer1[i][10]+"\n"+"\n"+"年費："+answer1[i][11]+"\n"+"\n"
#             #+"年收入限制："+answer1[i][12]+"\n"+"\n"+"年齡限制："+answer1[i][13]+"\n"+"\n")
#     else:
#         for i in range(0,len(answer1)):
#             answerstr += answer1[i][1]+answer1[i][2]+'\n'
#             #showinfo(answer1[i][1]+answer1[i][2],answer1[i][1]+answer1[i][2] ).geoemtry("1080*1080")

#     return answerstr

####################################
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
page = Page(ACCESS_TOKEN)

## We will receive messages that Facebook sends our bot at this endpoint 
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

page.greeting("Welcome!")

####################################
##### 接收按鈕傳回的訊息
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload

    print("Received postback for user %s and page %s with payload '%s' at %s"
          % (sender_id, recipient_id, payload, time_of_postback))

    if payload == 'ABC':
        page.send(sender_id, '早安我的朋友')
    elif payload == 'DEF':
        page.send(sender_id, '晚安我的朋友')
    elif payload == 'DEVELOPED_DEFINED_PAYLOAD':
        page.send(sender_id, '噫！好了！我中了！')
    elif payload == 'MENU1':
        page.send(sender_id, '母湯喔')
    elif payload == 'MENU2':
        page.send(sender_id, '湯喔')
    elif payload == 'START_PAYLOAD':
        page.send(sender_id, '在想些什麼？')

####################################
##### 開始菜單(未完成)
page.show_starting_button("START_PAYLOAD")
# @page.callback(['START_PAYLOAD'])
# def start_callback(payload, event):
#     print("Let's start!")

page.show_persistent_menu([Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                           Template.ButtonPostBack('MENU1', 'MENU1'),
                           Template.ButtonPostBack('MENU2', 'MENU2')])

# @page.callback(['MENU_PAYLOAD/(.+)'])
# def click_persistent_menu(payload, event):
#     click_menu = payload.split('/')[1]
#     print("you clicked %s menu" % click_menu)

####################################
##### 
@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text

    ##### 按鈕
    if message == 'A':     
        buttons = [{'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
                   {'type': 'postback', 'title': 'trigger Postback', 'value': 'DEVELOPED_DEFINED_PAYLOAD'},
                   {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+886970119732'}]
        page.send(sender_id, Template.Buttons("hello", buttons))

    ##### 圖片
    elif message == 'B':
        page.send(sender_id, Attachment.Image('http://i.imgur.com/hKORBJK.jpg'))

    ##### 快速回覆
    elif message == 'C':
        quick_replies = [{'title': 'Action', 'payload': 'PICK_ACTION'},
                         {'title': 'Comedy', 'payload': 'PICK_COMEDY'}]
        page.send(sender_id, "What's your favorite movie genre?", quick_replies=quick_replies, metadata="DEVELOPER_DEFINED_METADATA")

    ##### Generic Template
    elif message == 'D':
        page.send(sender_id, Template.Generic([
                Template.GenericElement("rift",
                                subtitle="Next-generation virtual reality",
                                item_url="https://www.oculus.com/en-us/rift/",
                                # image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                                image_url='http://i.imgur.com/hKORBJK.jpg',
                                buttons=[{'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
                                        {'type': 'postback', 'title': 'BANK A', 'value': 'ABC'},
                                        {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+886970119732'}]),
                Template.GenericElement("touch",
                                subtitle="Your Hands, Now in VR",
                                item_url="https://www.oculus.com/en-us/touch/",
                                image_url='http://i.imgur.com/hKORBJK.jpg',
                                buttons=[
                                        {'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
                                        {'type': 'postback', 'title': 'BANK B', 'value': 'DEF'},
                                        {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+886970119732'}])
        ]))
        
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