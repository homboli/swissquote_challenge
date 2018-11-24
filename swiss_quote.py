import requests

HOST =  "http://lauzhack.sqpub.ch"
APIKEY = "hf3768dkLLhf"

def buy(amount):
    data = "BUY " + str(amount) + " BTC " + APIKEY
    r = requests.post(HOST, data)
    return r

def sell(amount):
    data = "SELL " + str(amount) + " BTC " + APIKEY
    r = requests.post(HOST, data)
    return r

def readHistoricalData():
    


def runPriceStream():
    r = requests.get(HOST + "/prices", stream = True)
    for line in r.iter_lines():
        if line:
            print(line)

runPriceStream()
