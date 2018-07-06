# 利用 Python 製作 Facebook Chatbot（聊天機器人）

聊天機器人是現在很流行的商業行銷或宣傳手法，許多商家的臉書粉絲專頁都設有聊天機器人可以自動回覆使用者傳送的訊息，甚至還能做到交易、遊戲等功能。聊天機器人的流行一方面也是因為透過機器學習方法，聊天機器人可以做到自然語言處理（NLP）而成為人工智慧下的產物，雖然現今多半的聊天機器人並還不支援讓使用者隨意輸入訊息就能如真人一般的回應。

開發聊天機器人花費了我們很多的時間和心力。Messenger 官方技術文件使用的是PHP，所以我們必須尋找 Python 開發者開發的第三方套件。我們發現網路上有非常多聊天機器人相關的套件，而且幾乎沒有一個是完善的，例如我們最一開始使用的 *PyMessenger*，該套件就沒有製作快速回覆的功能（我們推測可能是因為 Facebook 功能推陳出新，有些開發者做完套件後可能沒有持續維護所致）。所以我們換了兩、三個套件才包含了所有我們需要用到的功能，同時研讀了數篇教學文章與技術文件後才終於開發出來（而且做好後才發現要先讓 Facebook 審核程式通過後才能使用程式…）。

下面附上 fbmq 的套件開發者寫的技術文件，以及 Facebook Messenger Platform 的官方文件，大家可以自行研讀。

+ [fbmq](https://github.com/conbus/fbmq)

+ [Messenger Platform](https://developers.facebook.com/docs/messenger-platform/)

## 用途：信用卡推薦機器人

+ 開場問候：使用者開始一使用時，聊天機器人會發送一段招呼語問候使用者，並簡單介紹我們提供的服務以及操作說明。

+ 選擇想要的信用卡特色：根據上表我們整理的信用卡五大類信用卡優惠，讓使用者從旅遊交通、休閒娛樂、購物、電子支付、宗教五大特色中，選擇一項喜好的信用卡特色。

+ 選擇子項目特色：如果使用者選擇旅遊交通、休閒娛樂、購物這三類別，機器人會引導使用者再選擇一項母項目下的子項目。（如表一架構）

+ 推薦信用卡：根據使用者選擇的產品特色，機器人隨機推薦4張資料庫中的信用卡，並在每張信用卡下顯示詳細資訊、辦卡連結兩個按鍵。

    > 詳細資訊：機器人傳送此張信用卡的詳細相關資訊給使用者，其中包含國內／外現金回饋、產品特色／限制、首刷禮／活動、年費、年收入／年齡限制等資訊。
    >
    > 辦卡連結：使用者可以藉由此按鍵連結至發行該信用卡的銀行官網。

## 程式中用到的功能：

除了自動回覆訊息外，這個機器人還具備三種功能。

1. quick reply

    可以讓使用者用按按鈕的方式回覆我們想要使用者輸入的訊息。

    ![quick reply](/rmd_img/01.jpg)

2. Generic Template

    一般型範本可以傳送包含圖片、文字、按鈕的結構化訊息。

    ![generic template](/rmd_img/02.jpg)

3. persistent menu

    常駐功能表可以在聊天室的下方永遠顯示這些功能。

    ![persistent menu](/rmd_img/03.jpg)

4. 資料讀取與輸出

    我們原先的設計構想是希望能透過爬蟲的方式來建立資料庫。但由於我們所使用的網站來源是透過 JavaScript 的語法撰寫，爬蟲的難度會較一般寫在 HTML 中的網頁來的高，所以我們目前的因應措施是使用人工建立資料庫，再從該 csv 檔中讀取資料進行卡片推薦與後續的應用。

    資料庫在 data.csv 當中。

## 系統設計

+ **資料讀取**

為了讓程式更精簡、更好判讀，我們將為了要讀取資料創建的兩個函式和主要的程式分離。我們將資料讀取的函式存成獨立的 py 檔 *search_card.py* ，並在主程式中加入這一段程式碼：

```python
from search_card import recommend_card, card_detail
```

如此一來，在主要程式中只要呼叫這兩個函式就可以運作。

+ **設定驗證密碼**

在寫程式之前，我們需要先創建一個粉絲專頁，在創建後會自動生成一個"Access token"，也就是粉絲專頁的身分證。在發送訊息或接收訊息時，這個代碼將會被用來驗證請求。

而"verify token"則相當於一組安全密碼，密碼正確時程式和臉書才能正確地串連運作。

```python
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
```

+ **開始使用按鈕與常駐選單**

臉書的規定是，常駐選單的功能必須搭配開始按鈕一起使用才能運作。當我們按下「開始使用」時，程式便會收到一組我們設定的 payload "START"，並回傳一段文字與快速回覆按鈕。常駐選單則是以一個按鈕一個按鈕的型式組合出來，而按下按鈕的結果可以是回傳 paylaod 或是網址。

```python
page.show_starting_button('START')
page.show_persistent_menu([Template.ButtonPostBack('重新查詢', 'REFRESH'),
                           Template.ButtonWeb('前往此網頁以獲得更多資訊', 'https://money101.com.tw'),
                           Template.ButtonWeb('讓你看看我們的資料庫！', 'https://github.com/chrisyang-tw/PBC_Final/blob/master/data.csv')])
```

在這之前我們需要先定義一個函式，這個函式會判讀所有 payload 的內容，因為當使用者 **按下開始按鈕**、**按下按鈕**、**按下常駐選單**時，聊天畫面和真正回傳到程式的值是不一樣的。

另外，快速回覆的功能是只要在 *page.send* 後增加 *quick_replies* 的 list 即可，且程式會收到的是一個 message 文字。

```python
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    payload = event.postback_payload

    if payload == 'START':
        text = 'TEXT'
        page.send(sender_id, text, quick_replies=[{'title': 'TITLE', 'payload': 'PAYLOAD'},
                                                  {'title': 'TITLE', 'payload': 'PAYLOAD'}])
```

+ **訊息傳送與判斷**

當使用者傳送訊息，聊天視窗會回傳一組 JSON 格式到程式中，而在這個套件中已經簡化了我們需要對 JSON 格式的判斷，我們只要設定 *sender_id* 和 *message* 兩個變數即可回覆，並用簡單的判斷式判斷使用者傳送的訊息。

在 Messenger Platform 上也有一個傳送者動作功能，可以讓機器人的回覆更加人性化。利用這個功能，我們可以讓機器人在使用者輸入訊息後立刻回覆訊息，也能在已讀和收到預計回覆的訊息時傳送「點點點」的符號，讓用戶覺得這段時間是真的有人在回覆訊息。

```python
@page.handle_message
def message_handler(event):
    sender_id = event.sender_id
    message = event.message_text

    page.mark_seen(sender_id)
    page.typing_on(sender_id)

    if message == 'MESSAGE':
        text = 'TEXT'
        page.send(...)
```

+ **隨機回覆**

當使用者輸入不是我們要的文字時，我們利用 *random.choice* 從我們資料庫中的清單中隨機回覆。

```python
rand = ['response_1', 'response_2', 'response_3', ...]

page.send(sender_id, random.choice(rand))
```
