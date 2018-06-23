import csv
import urllib.request
import codecs
import random

webpage = urllib.request.urlopen('https://raw.githubusercontent.com/chrisyang-tw/PBC_Final/master/data.csv')
next(webpage)
rows = csv.reader(codecs.iterdecode(webpage, 'utf-8'))

def cal2(Type):
    for row in rows:
        if Type == str(row[1]) + str(row[2]):
            ans = ("信用卡名:"+row[1]+row[2]+"\n"+"\n"+"國內現金回饋："+row[3]+"\n"+"\n"+"國外現金回饋："+row[4]+"\n"+"\n"+"優惠內容："+row[6]
            +"\n"+"\n"+"優惠限制："+row[7]+"\n"+"\n"+"首刷禮："+row[8]+"\n"+"\n"+"首刷活動："+row[9]+"\n"+"\n"+"手續費："+row[10]+"\n"+"\n"+"年費："+row[11]+"\n"+"\n"
            +"年收入限制："+row[12]+"\n"+"\n"+"年齡限制："+row[13]+"\n"+"\n")
    return ans

a = '元大銀行iCash樂享晶緻卡'

print(cal2(a))