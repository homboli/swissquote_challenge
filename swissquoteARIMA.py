import requests
from datetime import datetime
import pandas
import numpy
import pylab
import matplotlib.pyplot as pyplot
import csv
from decimal import Decimal

from statsmodels.tsa.arima_model import ARIMA


from sklearn.metrics import mean_squared_error

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

def toUnixTimeStamp(originalDateTime):
    return int(datetime.strptime(originalDateTime, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())

def runPriceListening(dataset):
    r = requests.get(HOST + "/prices", stream = True)
    previousTime = 0
    for line in r.iter_lines():
        if line:
            actualTime = toUnixTimeStamp(str(line)[2:-1].split(' ')[0])
            if actualTime - previousTime > 1:
                print(line)
                actualPrice = Decimal(str(line)[2:-1].split(' ')[1])
                previousTime = actualTime
                dataset.append([actualTime, actualPrice])
                if actualTime - previousTime > 10:
                    model = ARIMA(dataset['Price'].values, order=(6, 1, 4))
                    model_fit = model.fit(disp=False)
                    predictions = model_fit.predict(len(dataset['Date'].values), len(dataset['Date'].values) + 10, typ='levels')
                    if predictions[-1] - actualPrice > actualprice * 0.0001:
                        buy(actualPrice, cap, 0.04)
                    if predictions[-1] - actualPrice < actualprice * 0.0001:
                        sell(actualPrice, cap, 0.04)
                    print(line)

dataset = pandas.read_csv('histo_prices_stamp.csv', names=['Date','Price'])
#runPriceListening(dataset)
model = ARIMA(dataset['Price'].values[0:350], order=(6, 1, 4))
model_fit = model.fit(disp=False)
p = model_fit.predict(len(dataset['Date'].values[:350]), len(dataset['Date'].values[:350])+49, typ='levels',dynamic=False )
x = dataset['Date'].values[350:400]
y = dataset['Price'].values[350:400]
pyplot.plot(x,y, label='True Data')
z = dataset['Date'].values[350:400]
pyplot.plot(z,p, label = "pred")
pyplot.legend()
pyplot.show()