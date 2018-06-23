# coding: utf-8
import os
import json
from flask import Flask, request
from fbmq import Attachment, Template, QuickReply, Page
import csv
import random
import urllib

##### 爬資料
def cal1(Type):
    webpage = urllib.urlopen('https://github.com/chrisyang-tw/PBC_Final/blob/master/data.csv')
    next(webpage)
    rows = csv.reader(webpage)
    
    # data = "/Users/chiaa/Desktop/data.csv"
    # csvfile = open(data, mode='r', encoding='utf-8')
    # next(csvfile)
    # rows = csv.reader(csvfile)
    answer = []
    for row in rows:
        #print (row[5])
        if Type in row[5]:
            answer +=[row]
    number = []
    answer1 = []
    for i in range(0,len(answer)):
        number.append(i)
    random.shuffle(number)
    #print(number)
    for  i in range(0,len(answer)):
        answer1.append(answer[number[i]])
    #print(answer1)
    answer1 = sorted(answer1, key=lambda y: answer[14], reverse=True)
    card = [[], [], [], []]
    if len(answer1) >= 5:
        for i in range(0,5):
            card[0].append(answer1[i][1]+answer1[i][2])
            card[1].append(answer1[i][1]+answer1[i][2]+'\n'+"信用卡名:"+answer1[i][1]+answer1[i][2]+"\n"+"\n"+"國內現金回饋："+answer1[i][3]+"\n"+"\n"+"國外現金回饋："+answer1[i][4]+"\n"+"\n"+"優惠內容："+answer1[i][6]
            +"\n"+"\n"+"優惠限制："+answer1[i][7]+"\n"+"\n"+"首刷禮："+answer1[i][8]+"\n"+"\n"+"首刷活動："+answer1[i][9]+"\n"+"\n"+"手續費："+answer1[i][10]+"\n"+"\n"+"年費："+answer1[i][11]+"\n"+"\n"
            +"年收入限制："+answer1[i][12]+"\n"+"\n"+"年齡限制："+answer1[i][13]+"\n"+"\n")
            card[2].append(answer1[i][15])
            card[3].append(answer1[i][16])
            print('hohoho')
    else:
        for i in range(0,len(answer1)):
            card[0].append(answer1[i][1]+answer1[i][2]+'\n')
            card[1].append(answer1[i][1]+answer1[i][2],"信用卡名:"+answer1[i][1]+answer1[i][2]+"\n"+"\n"+"國內現金回饋："+answer1[i][3]+"\n"+"\n"+"國外現金回饋："+answer1[i][4]+"\n"+"\n"+"優惠內容："+answer1[i][6]
            +"\n"+"\n"+"優惠限制："+answer1[i][7]+"\n"+"\n"+"首刷禮："+answer1[i][8]+"\n"+"\n"+"首刷活動："+answer1[i][9]+"\n"+"\n"+"手續費："+answer1[i][10]+"\n"+"\n"+"年費："+answer1[i][11]+"\n"+"\n"
            +"年收入限制："+answer1[i][12]+"\n"+"\n"+"年齡限制："+answer1[i][13]+"\n"+"\n")
            card[2].append(answer1[i][15])
            card[3].append(answer1[i][16])

    return card

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

    if payload == 'START':
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

page.show_starting_button('START')

page.show_persistent_menu([Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                           Template.ButtonPostBack('開始使用', 'START'),
                           Template.ButtonPostBack('Undefined', 'MENU2')])

####################################
##### 
@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text

    ## 第一次判斷
    sub_features = {'高額現金回饋': [{'title': '國內現金回饋', 'payload': 'in'},
                                    {'title': '國外現金回饋', 'payload': 'out'}],
                    '旅遊交通': [{'title': '里程累積', 'payload': 'meter'},
                                {'title': '旅遊優惠', 'payload': 'travel'},
                                {'title': '國外刷卡優惠', 'payload': 'outside'},
                                {'title': '高鐵', 'payload': 'hsr'},
                                {'title': '加油停車', 'payload': 'oil'},
                                {'title': 'eTag', 'payload': 'etag'}],
                    '休閒娛樂': [{'title': '美食', 'payload': 'food'},
                                {'title': '電影', 'payload': 'movie'}],
                    '購物': [{'title': '通路聯名', 'payload': 'chain'},
                            {'title': '網路購物', 'payload': 'shopee'}]
                    }

    if message == '想！':
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
    elif message in sub_features:
        page.send(sender_id, '再選擇一個子項目吧', quick_replies=sub_features[message])
    # if message == 'A':     
    #     buttons = [{'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
    #                {'type': 'postback', 'title': 'trigger Postback', 'value': 'DEVELOPED_DEFINED_PAYLOAD'},
    #                {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+886970119732'}]
    #     page.send(sender_id, Template.Buttons("hello", buttons))

    # ##### 圖片
    # elif message == 'B':
    #     page.send(sender_id, Attachment.Image('http://i.imgur.com/hKORBJK.jpg'))

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
    elif message == 'D':
        answer = cal1('加油停車')
        page.send(sender_id, Template.Generic([
                Template.GenericElement(answer[0][0],
                                subtitle=answer[0][0],
                                item_url=answer[3][0],
                                # image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                                image_url=answer[2][0],
                                buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': 'card1'},
                                        {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][0]}])
                # Template.GenericElement(answer[0][1],
                #                 subtitle=answer[0][1],
                #                 item_url=answer[3][1],
                #                 # image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                #                 image_url=answer[2][1],
                #                 buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': 'card2'},
                #                         {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][1]}]),
                # Template.GenericElement(answer[0][2],
                #                 subtitle=answer[0][2],
                #                 item_url=answer[3][2],
                #                 # image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                #                 image_url=answer[2][2],
                #                 buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': 'card3'},
                #                         {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][2]}]),
                # Template.GenericElement(answer[0][3],
                #                 subtitle=answer[0][3],
                #                 item_url=answer[3][3],
                #                 # image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                #                 image_url=answer[2][3],
                #                 buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': 'card4'},
                #                         {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][3]}]),
                # Template.GenericElement(answer[0][4],
                #                 subtitle=answer[0][4],
                #                 item_url=answer[3][4],
                #                 # image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                #                 image_url=answer[2][4],
                #                 buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': 'card5'},
                #                         {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][4]}])
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