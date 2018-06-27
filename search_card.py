import csv
import random
import urllib.request
import codecs

## cal1 function 可隨機推薦四張卡並回傳卡片名稱、圖片與銀行網址
def recommend_card(Type):
    webpage = urllib.request.urlopen('https://raw.githubusercontent.com/chrisyang-tw/PBC_Final/master/data.csv')
    next(webpage)
    rows = csv.reader(codecs.iterdecode(webpage, 'utf-8'))

    answer = []
    for row in rows:
        if Type in row[5]:
            answer += [row]

    number = []
    answer1 = []
    answer2 = []
    for i in range(0,len(answer)):
        number.append(i)
    random.shuffle(number)
    for i in range(0,len(answer)):
        answer1.append(answer[number[i]])

    ## 按照現金回饋排序
    # answer1 = sorted(answer1, key=lambda y: y[14], reverse=True)

    for i in range(4):
        answer2.append(answer1[i])

    card = [[], [], []]
    for i in range(4):
        ## 四張卡的名稱
        card[0].append(answer2[i][1] + answer2[i][2])
        ## 四張卡的圖片
        card[1].append(answer1[i][15])
        ## 四張卡的銀行網站
        card[2].append(answer1[i][16])

    return card

# ans = recommend_card('購物')
# print(ans[0])

## cal2 function 可搜尋該卡片的詳細資訊
def card_detail(Card):
    webpage = urllib.request.urlopen('https://raw.githubusercontent.com/chrisyang-tw/PBC_Final/master/data.csv')
    next(webpage)
    rows = csv.reader(codecs.iterdecode(webpage, 'utf-8'))
    for row in rows:
        if Card == str(row[1]) + str(row[2]):
            detail = ('信用卡名：' + row[1] + row[2] + '\n' + '\n'
                    + '國內現金回饋：' + row[3] + '\n' + '\n' 
                    + '國外現金回饋：' + row[4] + '\n' + '\n' 
                    + '優惠內容：' + row[6] + '\n' + '\n' 
                    + '優惠限制：' + row[7] + '\n' + '\n' 
                    + '首刷禮：' + row[8] + '\n' + '\n' 
                    + '首刷活動：' + row[9] + '\n' + '\n' 
                    + '手續費：' + row[10] + '\n' + '\n' 
                    + '年費：' + row[11] + '\n' + '\n'
                    + '年收入限制：' + row[12] + '\n' + '\n' 
                    + '年齡限制：' + row[13] + '\n'+ '\n')
            return detail

# ans2 = card_detail('台北富邦法鼓山自在卡')
# print(ans2)