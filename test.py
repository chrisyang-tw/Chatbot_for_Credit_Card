import csv
import urllib.request
import codecs
import random

# url = "https://raw.githubusercontent.com/chrisyang-tw/PBC_Final/master/data.csv"
# ftpstream = urllib.request.urlopen(url)
# csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
# for line in csvfile:
#     print(line)

def cal1(Type):
    webpage = urllib.request.urlopen('https://raw.githubusercontent.com/chrisyang-tw/PBC_Final/master/data.csv')
    next(webpage)
    rows = csv.reader(codecs.iterdecode(webpage, 'utf-8'))
    
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
            # print('hohoho')
    else:
        for i in range(0,len(answer1)):
            card[0].append(answer1[i][1]+answer1[i][2]+'\n')
            card[1].append(answer1[i][1]+answer1[i][2],"信用卡名:"+answer1[i][1]+answer1[i][2]+"\n"+"\n"+"國內現金回饋："+answer1[i][3]+"\n"+"\n"+"國外現金回饋："+answer1[i][4]+"\n"+"\n"+"優惠內容："+answer1[i][6]
            +"\n"+"\n"+"優惠限制："+answer1[i][7]+"\n"+"\n"+"首刷禮："+answer1[i][8]+"\n"+"\n"+"首刷活動："+answer1[i][9]+"\n"+"\n"+"手續費："+answer1[i][10]+"\n"+"\n"+"年費："+answer1[i][11]+"\n"+"\n"
            +"年收入限制："+answer1[i][12]+"\n"+"\n"+"年齡限制："+answer1[i][13]+"\n"+"\n")
            card[2].append(answer1[i][15])
            card[3].append(answer1[i][16])

    return card

print(cal1('加油停車'))