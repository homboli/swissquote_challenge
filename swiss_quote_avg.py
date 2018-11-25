import requests
from datetime import datetime

HOST =  "http://lauzhack.sqpub.ch"
APIKEY = "hf3768dkLLhf"

cap = 100000


def buy(actualPrice, money, part):
   amount = (money * part) / actualPrice
   data = "BUY " + str(amount) + " BTC " + APIKEY
   r = requests.post(HOST, data)
   return r

def sell(actualPrice, money, part):
   amount = (money * part) / actualPrice
   data = "SELL " + str(amount) + " BTC " + APIKEY
   r = requests.post(HOST, data)
   return r

def readHistoricalData():
    print("")

def toUnixTimeStamp(originalDateTime):
    return int(datetime.strptime(originalDateTime, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())

def log(event):
    d = datetime.now()
    print('['+str(d)+']['+event+']')


def runPriceListening():
   r = requests.get(HOST + "/prices", stream = True)
   sliding_window = []
   cntr=0
   prev_avg = []
   for line in r.iter_lines():
       if line:
           actualTime = toUnixTimeStamp(str(line)[2:-1].split(' ')[0])
           actualPrice = float(str(line)[2:-1].split(' ')[1])
           sliding_window.append(actualPrice)
           if len(sliding_window) < 10:
               continue
           elif len(sliding_window) == 10:
               avg = sum(sliding_window) / 10.0
               log(str(avg))
               cntr+=1
               if cntr == 5:
                   prev_avg.append(avg)
                   cntr=0
               if (len(prev_avg)==4):
                   #descendent
                   if(prev_avg[0]<prev_avg[1]) and (prev_avg[1]<prev_avg[2]):
                       #sell
                       sell(actualPrice, cap, 0.03)
                       log('sell')
                   elif (prev_avg[0] > prev_avg[1]) and (prev_avg[1] > prev_avg[2]):
                       # buy
                       buy(actualPrice, cap, 0.03)
                       log('buy')
                   else:
                       #hold
                       log('hold')
                   prev_avg.remove(prev_avg[0])
               elif (len(prev_avg)==3):
                   if (prev_avg[0] < prev_avg[1]) and (prev_avg[1] < prev_avg[2]):
                       #sell
                       sell(actualPrice, cap, 0.03)
                       log('sell')

                   elif (prev_avg[0] > prev_avg[1]) and (prev_avg[1] > prev_avg[2]):
                       # buy
                       buy(actualPrice, cap, 0.03)
                       log('buy')
                   else:
                       # hold
                       log('hold')

               sliding_window.remove(sliding_window[0])


runPriceListening()