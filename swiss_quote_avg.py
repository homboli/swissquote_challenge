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
   amount = ((100000 - money) * part) / actualPrice
   data = "SELL " + str(amount) + " BTC " + APIKEY
   r = requests.post(HOST, data)
   return r

def readHistoricalData():
    print("")

def toUnixTimeStamp(originalDateTime):
    return int(datetime.strptime(originalDateTime, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())

def log(event,value):
    d = datetime.now()
    print('['+str(d)+']['+event+']['+str(value)+']')


def runPriceListening():
   r = requests.get(HOST + "/prices", stream = True)
   sliding_window = []
   cntr=0
   prev_avg = []
   for line in r.iter_lines():
       if line:
           #actualTime = toUnixTimeStamp(str(line)[2:-1].split(' ')[0])
           actualPrice = float(str(line)[2:-1].split(' ')[1])
           sliding_window.append(actualPrice)
           if len(sliding_window) < 10:
               continue
           elif len(sliding_window) == 10:
               avg = sum(sliding_window) / 10.0
               log('avg',str(avg))
               cntr+=1
               if cntr == 5:
                   prev_avg.append(avg)
                   cntr=0
               if (len(prev_avg)==4):
                   #descendent
                   slope = abs(prev_avg[2] - prev_avg[0])/10
                   print(slope)
                   if(prev_avg[0]<prev_avg[1]) and (prev_avg[1]<prev_avg[2]):
                       #sell
                       if (slope > 0.1):
                            sell(actualPrice, cap, slope)
                            log('sell',((cap * slope) / actualPrice))
                   elif (prev_avg[0] > prev_avg[1]) and (prev_avg[1] > prev_avg[2]):
                       # buy
                       if (slope > 0.1):
                            buy(actualPrice, cap, slope)
                            log('buy',((cap * slope) / actualPrice))
                   else:
                       #hold
                       log('hold',((cap * slope) / actualPrice))
                   prev_avg.remove(prev_avg[0])
               elif (len(prev_avg)==3):
                   slope = abs(prev_avg[2] - prev_avg[0])/10
                   print(slope)
                   if (prev_avg[0] < prev_avg[1]) and (prev_avg[1] < prev_avg[2]):
                       #sell
                       if(slope>0.1):
                            sell(actualPrice, cap, slope)
                            log('sell',((cap * slope) / actualPrice))

                   elif (prev_avg[0] > prev_avg[1]) and (prev_avg[1] > prev_avg[2]):
                       # buy
                       if (slope > 0.1):
                            buy(actualPrice, cap, slope)
                            log('buy',((cap * slope) / actualPrice))
                   else:
                       # hold
                       log('hold',((cap * slope) / actualPrice))

               sliding_window.remove(sliding_window[0])


runPriceListening()