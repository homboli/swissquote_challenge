from datetime import datetime

def toUnixTimeStamp(originalDateTime):
    return int(datetime.strptime(originalDateTime, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())



print(str(toUnixTimeStamp("2018-11-24T18:46:21.668000Z")))