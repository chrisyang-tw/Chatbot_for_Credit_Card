# coding: utf-8
import os
import json
from flask import Flask, request
from fbmq import Attachment, Template, QuickReply, Page
import csv
import random
import urllib.request
import codecs

##### 爬資料
webpage = urllib.request.urlopen('https://raw.githubusercontent.com/chrisyang-tw/PBC_Final/master/data.csv')
next(webpage)
rows = csv.reader(codecs.iterdecode(webpage, 'utf-8'))

####################################
def cal1(Type):
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
    for i in range(0,len(answer)):
        answer1.append(answer[number[i]])
    #print(answer1)
    answer1 = sorted(answer1, key=lambda y: y[14], reverse=True)
    card = [[], [], [], []]
    if len(answer1) >= 5:
        for i in range(0,5):
            card[0].append(answer1[i][1]+answer1[i][2])
            card[1].append(answer1[i][1]+answer1[i][2]+'\n'+"信用卡名:"+answer1[i][1]+answer1[i][2]+"\n"+"\n"+"國內現金回饋："+answer1[i][3]+"\n"+"\n"+"國外現金回饋："+answer1[i][4]+"\n"+"\n"+"優惠內容："+answer1[i][6]
            +"\n"+"\n"+"優惠限制："+answer1[i][7]+"\n"+"\n"+"首刷禮："+answer1[i][8]+"\n"+"\n"+"首刷活動："+answer1[i][9]+"\n"+"\n"+"手續費："+answer1[i][10]+"\n"+"\n"+"年費："+answer1[i][11]+"\n"+"\n"
            +"年收入限制："+answer1[i][12]+"\n"+"\n"+"年齡限制："+answer1[i][13]+"\n"+"\n")
            card[2].append(answer1[i][15])
            card[3].append(answer1[i][16])
            # print('hohoho')
    else:
        for i in range(0,len(answer1)):
            card[0].append(answer1[i][1]+answer1[i][2]+'\n')
            card[1].append(answer1[i][1]+answer1[i][2]+'\n'+"信用卡名:"+answer1[i][1]+answer1[i][2]+"\n"+"\n"+"國內現金回饋："+answer1[i][3]+"\n"+"\n"+"國外現金回饋："+answer1[i][4]+"\n"+"\n"+"優惠內容："+answer1[i][6]
            +"\n"+"\n"+"優惠限制："+answer1[i][7]+"\n"+"\n"+"首刷禮："+answer1[i][8]+"\n"+"\n"+"首刷活動："+answer1[i][9]+"\n"+"\n"+"手續費："+answer1[i][10]+"\n"+"\n"+"年費："+answer1[i][11]+"\n"+"\n"
            +"年收入限制："+answer1[i][12]+"\n"+"\n"+"年齡限制："+answer1[i][13]+"\n"+"\n")
            card[2].append(answer1[i][15])
            card[3].append(answer1[i][16])

    return card

def cal2(Type):
    for row in rows:
        if Type == str(row[1]) + str(row[2]):
            ans = ("信用卡名:"+row[1]+row[2]+"\n"+"\n"+"國內現金回饋："+row[3]+"\n"+"\n"+"國外現金回饋："+row[4]+"\n"+"\n"+"優惠內容："+row[6]
            +"\n"+"\n"+"優惠限制："+row[7]+"\n"+"\n"+"首刷禮："+row[8]+"\n"+"\n"+"首刷活動："+row[9]+"\n"+"\n"+"手續費："+row[10]+"\n"+"\n"+"年費："+row[11]+"\n"+"\n"
            +"年收入限制："+row[12]+"\n"+"\n"+"年齡限制："+row[13]+"\n"+"\n")
        return ans

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
    
    elif payload == card1:
        page.send(sender_id, cal2(card1))
    elif payload == card2:
        page.send(sender_id, cal2(card2))
    elif payload == card3:
        page.send(sender_id, cal2(card3))
    elif payload == card4:
        page.send(sender_id, cal2(card4))
    elif payload == card5:
        page.send(sender_id, cal2(card5))
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
    sub_features_all = ['國內現金回饋', '國外現金回饋', '里程累積', '旅遊優惠', '國外刷卡優惠', '高鐵', '加油停車', 'eTag', '美食', '電影', '通路聯名', '網路購物', '電子支付功能(悠遊卡、一卡通、iCash)', '宗教']

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

    ## 輸出
    elif message in sub_features_all:
        answer = cal1(message)
        global card1, card2, card3, card4, card5
        card1, card2, card3, card4, card5 = answer[0][0], answer[0][1], answer[0][2], answer[0][3], answer[0][4]
        if len(answer[0]) == 5:
            page.send(sender_id, Template.Generic([
                    Template.GenericElement(answer[0][0],
                                    subtitle=answer[0][0],
                                    item_url=answer[3][0],
                                    image_url=answer[2][0],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card1},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][0]}]),
                    Template.GenericElement(answer[0][1],
                                    subtitle=answer[0][1],
                                    item_url=answer[3][1],
                                    image_url=answer[2][1],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card2},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][1]}]),
                    Template.GenericElement(answer[0][2],
                                    subtitle=answer[0][2],
                                    item_url=answer[3][2],
                                    image_url=answer[2][2],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card3},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][2]}]),
                    Template.GenericElement(answer[0][3],
                                    subtitle=answer[0][3],
                                    item_url=answer[3][3],
                                    image_url=answer[2][3],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card4},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][3]}]),
                    Template.GenericElement(answer[0][4],
                                    subtitle=answer[0][4],
                                    item_url=answer[3][4],
                                    image_url=answer[2][4],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card5},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][4]}])
            ]))
        ## eTag 是特例，只會有四個
        else:
            page.send(sender_id, Template.Generic([
                    Template.GenericElement(answer[0][0],
                                    subtitle=answer[0][0],
                                    item_url=answer[3][0],
                                    image_url=answer[2][0],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card1},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][0]}]),
                    Template.GenericElement(answer[0][1],
                                    subtitle=answer[0][1],
                                    item_url=answer[3][1],
                                    image_url=answer[2][1],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card2},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][1]}]),
                    Template.GenericElement(answer[0][2],
                                    subtitle=answer[0][2],
                                    item_url=answer[3][2],
                                    image_url=answer[2][2],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card3},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][2]}]),
                    Template.GenericElement(answer[0][3],
                                    subtitle=answer[0][3],
                                    item_url=answer[3][3],
                                    image_url=answer[2][3],
                                    buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card4},
                                            {'type': 'web_url', 'title': '我要辦卡', 'value': answer[3][3]}])
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