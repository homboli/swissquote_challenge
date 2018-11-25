from datetime import datetime
f = open("histo_prices_stamp.csv", "w")

def toUnixTimeStamp(originalDateTime):
    return int(datetime.strptime(originalDateTime, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())

for l in open("historic_prices.csv").readlines():
    t = l.split(" ")
    ts_out = toUnixTimeStamp(t[0])
    price = t[1]
    s = "%s,%s" % (ts_out, price)
    f.write(s)
