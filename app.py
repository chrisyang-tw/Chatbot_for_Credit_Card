import os
from flask import Flask, request
from fbmq import Attachment, Template, QuickReply, Page
from search_card import recommend_card, card_detail
import random

########################################################
## 設置事件終點、通關密碼和認證密碼
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
page = Page(ACCESS_TOKEN)

## 設置webhook
@app.route("/", methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        else:
            return 'Invalid verification token'
    else:
        page.handle_webhook(request.get_data(as_text=True))
        return 'ok'

########################################################
## 判讀payload內容
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    payload = event.postback_payload

    ## 讓機器人在使用者傳送訊息後立刻已讀訊息並開啟輸入指示器(點點點符號)
    page.mark_seen(sender_id)
    page.typing_on(sender_id)

    ## 當使用者第一次打開機器人按下'開始使用'時
    if payload == 'START':
        text = '各位潮潮的菁英們，實習都已經賺了那麼多錢，是不是覺得沒地方花呢？想不想Bang成一個快樂的卡奴呢？'
        page.send(sender_id, text, quick_replies=[{'title': '想！', 'payload': 'Y'},
                                                  {'title': '不想', 'payload': 'N'}])
    ## 當使用者按下選單中的'重新查詢'時
    elif payload == 'REFRESH':
        text = '你希望想擁有的信用卡特色？'
        page.send(sender_id, text, quick_replies=[{'title': '高額現金回饋', 'payload': 'cash'},
                                                  {'title': '旅遊交通', 'payload': 'traffic'},
                                                  {'title': '休閒娛樂', 'payload': 'entertain'},
                                                  {'title': '購物', 'payload': 'shopping'},
                                                  {'title': '電子支付功能(悠遊卡、一卡通)', 'payload': 'easycard'},
                                                  {'title': '宗教', 'payload': 'religion'}])
    ## 當使用者按下卡片中的'詳細資訊'時
    else:
        page.send(sender_id, card_detail(payload))

########################################################
## 設置起始按鈕與常駐選單
page.greeting('我們是一群致力於讓各位elite成為卡奴的學生，想變卡奴找我們準沒錯！')
page.show_starting_button('START')
page.show_persistent_menu([Template.ButtonPostBack('重新查詢', 'REFRESH'),
                           Template.ButtonWeb('前往此網頁以獲得更多資訊', 'https://money101.com.tw'),
                           Template.ButtonWeb('讓你看看我們的資料庫！', 'https://github.com/chrisyang-tw/PBC_Final/blob/master/data.csv')])

########################################################
## 訊息傳送與判斷
@page.handle_message
def message_handler(event):
    sender_id = event.sender_id
    message = event.message_text

    ## 讓機器人在使用者傳送訊息後立刻已讀訊息並開啟輸入指示器(點點點符號)
    page.mark_seen(sender_id)
    page.typing_on(sender_id)
    
    ## 子特色字典，等一下會用到
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
                            {'title': '網路購物', 'payload': 'shopee'}]}
    sub_features_all = ['國內現金回饋', '國外現金回饋', '里程累積', '旅遊優惠', '國外刷卡優惠', '高鐵', '加油停車', 'eTag', '美食', '電影', '通路聯名', '網路購物', '電子支付功能(悠遊卡、一卡通)', '宗教']

    ## 當使用者一開始回答'想！'的回應
    if message == '想！':
        text = '那讓我們開始吧！在開始之前有個小叮嚀。如果你傳了訊息但我沒回你，可能是太多人在玩我，我負荷不了 >///<，這時候你可以按選單中的重新查詢我應該就會聽到你的呼喚了～'
        text2 = '首先先問問你希望想擁有的信用卡特色？'
        page.send(sender_id, text2, quick_replies=[{'title': '高額現金回饋', 'payload': 'cash'},
                                                  {'title': '旅遊交通', 'payload': 'traffic'},
                                                  {'title': '休閒娛樂', 'payload': 'entertain'},
                                                  {'title': '購物', 'payload': 'shopping'},
                                                  {'title': '電子支付功能(悠遊卡、一卡通)', 'payload': 'easycard'},
                                                  {'title': '宗教', 'payload': 'religion'}])
    
    ## 當使用者回答不想時的回應
    elif message == '不想':
        text = '相信我，卡奴也是可以過得很快樂的，給你最後一次機會，你想不想成為卡奴？'
        page.send(sender_id, text, quick_replies=[{'title':'想！', 'payload':'Y'}])

    ## 當使用者回答了主要特色，且該特色有子特色的回應
    elif message in sub_features:
        text = '再選擇一個子項目吧'
        page.send(sender_id, text, quick_replies=sub_features[message])

    ## 當使用者回答了子特色的回應
    elif message in sub_features_all:

        ## 宗教卡可觸發特殊開關
        if message == '宗教':
            page.send(sender_id, '嗯，看來你觸發了開關。')
            img = ['https://i.imgur.com/XdUQHNs.jpg', 'http://i.imgur.com/uZ8Kccr.jpg', 'http://i.imgur.com/Sug8VqH.jpg', 'http://i.imgur.com/VVIpqY3.jpg', 'http://i.imgur.com/CbBZu4i.jpg']
            for i in img:
                page.send(sender_id, Attachment.Image(i))

        text = '以下是推薦給你的四張卡片！按詳細資訊查看卡片資訊，按我要辦卡連結至銀行官網。'
        answer = recommend_card(message)
        card1, card2, card3, card4 = answer[0][0], answer[0][1], answer[0][2], answer[0][3]

        page.send(sender_id, text)
        page.send(sender_id, Template.Generic([
                Template.GenericElement(answer[0][0],
                                subtitle=answer[0][0],
                                item_url=answer[2][0],
                                image_url=answer[1][0],
                                buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card1},
                                        {'type': 'web_url', 'title': '我要辦卡', 'value': answer[2][0]}]),
                Template.GenericElement(answer[0][1],
                                subtitle=answer[0][1],
                                item_url=answer[2][1],
                                image_url=answer[1][1],
                                buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card2},
                                        {'type': 'web_url', 'title': '我要辦卡', 'value': answer[2][1]}]),
                Template.GenericElement(answer[0][2],
                                subtitle=answer[0][2],
                                item_url=answer[2][2],
                                image_url=answer[1][2],
                                buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card3},
                                        {'type': 'web_url', 'title': '我要辦卡', 'value': answer[2][2]}]),
                Template.GenericElement(answer[0][3],
                                subtitle=answer[0][3],
                                item_url=answer[2][3],
                                image_url=answer[1][3],
                                buttons=[{'type': 'postback', 'title': '詳細資訊', 'value': card4},
                                        {'type': 'web_url', 'title': '我要辦卡', 'value': answer[2][3]}])
            ]))
    
    ## 若使用者輸入其他訊息，則從以下這些話中隨機回覆。
    else:
        rand = ['你當我是AI？', 
                '樓下rrro。噢不對，樓上rrro。', 
                '你的訊息被藏在光頭葛格的紅色內褲裡，我找不到。', 
                '[問卦] 有沒有邊緣到只能和聊天機器人聊天的八卦？',
                '早安我的朋友，窩聽不懂中文。']

        page.send(sender_id, random.choice(rand))


########################################################
## 執行程式
if __name__ == '__main__':
    app.run()

