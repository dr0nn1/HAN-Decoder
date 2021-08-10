'''
https://www.kode24.no/guider/smart-meter-part-1-getting-the-meter-data/71287300
Used for understanding the obis number.
'''

import json
import datetime
import time

METERID = 11005255
METERTYPE = 119611255
ACTIVEPOWERINN = 11170255
ACTIVEPOWEROUT = 11270255
REACTIVEPOWERINN = 11370255
REACTIVEPOWEROUT = 11470255
L1CURRENT = 113170255
L2CURRENT = 115170255
L3CURRENT = 117170255
L1VOLTAGE = 113270255
L2VOLTAGE = 115270255
L3VOLTAGE = 117270255
CLOCKANDDATE = 1100255
HOURLYACTIVEPOWERINN = 11180255 
HOURLYACTIVEPOWEROUT = 11280255
HOURLYREACTIVEPOWERINN = 11380255
HOURLYREACTIVEPOWEROUT = 11480255

days = ["Sunday","Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def  hanDecoding(message):
    data = {}
    data["measurement"] = "Power reading"
    data["tags"] = {}
    data["time"] = int(time.time())
    data["fields"] = {}
    data["tags"]["host"] = "server01"
    data["tags"]["region"] = "eu-north"
    codedMessage = message.split(' ')
    for number in range(0,len(codedMessage)-1):
        if codedMessage[number] == "09":
            size = getSize(codedMessage[number+1])
            obisNumber = getObisNumber(codedMessage[number+2:number+size+2])
            dataSize = getDataSize(codedMessage[number+2+size])
            value = getData(codedMessage[number+3+size:number+3+size+dataSize])

            if obisNumber == ACTIVEPOWERINN:
                data["fields"]["Active Power Inn"] = value

            elif obisNumber == ACTIVEPOWEROUT:
                data["fields"]["Active Power Out"] = value

            elif obisNumber == REACTIVEPOWERINN:
                data["fields"]["Reactive Power Inn"] = value

            elif obisNumber == REACTIVEPOWEROUT:
                data["fields"]["Reactive Power Out"] = value

            elif obisNumber == L1CURRENT:
                data["fields"]["L1 Current"] = value/100

            elif obisNumber == L2CURRENT:
                data["fields"]["L2 Current"] = value/100

            elif obisNumber == L3CURRENT:
                data["fields"]["L3 Current"] = value/100

            elif obisNumber == L1VOLTAGE:
                data["fields"]["L1 Voltage"] = value

            elif obisNumber == L2VOLTAGE:
                data["fields"]["L2 Voltage"] = value

            elif obisNumber == L3VOLTAGE:
                data["fields"]["L3 Voltage"] = value

            elif obisNumber == CLOCKANDDATE:
                data["fields"]["Clock And Date"] = value

            elif obisNumber == HOURLYACTIVEPOWERINN:
                data["fields"]["Hourly Active Inn"] = value/100

            elif obisNumber == HOURLYACTIVEPOWEROUT:
                data["fields"]["Hourly Active Out"] = value/100
            
            elif obisNumber == HOURLYREACTIVEPOWERINN:
                data["fields"]["Hourly Reactive Inn"] = value/100

            elif obisNumber == HOURLYREACTIVEPOWEROUT:
                data["fields"]["Hourly Reactive Out"] = value/100      
    return "["+json.dumps(data)+"]"
         
def getSize(number):
    if number == "00":
        return 1
    return int(number,16)

def getDataSize(number):
    if number == "06":
        return 4
    elif number == "12":
        return 2
    elif number == "09":
        return 13
    else:
        return 1
            
def getData(lst):
    data = ""
    if len(lst) == 13:
        year = str(int((lst[1] + lst[2]),16))
        month = lst[3]
        dayMonth = int(lst[4],16)
        dayMonth = str('%02.0f' % dayMonth)
        dayWeek = lst[5]

        hour = int(lst[6],16)
        hour = str('%02.0f' % hour)
        minutes =int(lst[7],16)
        minutes = str('%02.0f' % minutes)
        seconds = int(lst[8],16)
        seconds = str('%02.0f' % seconds)

        #data = "Year: " + year + " Month: " + month + " Day of month:  " + dayMonth + " Day of week: " + dayWeek + " Hour: " + hour + " Minutes: " + minutes + " Seconds: " + seconds
        data = "Clock: " + hour +":"+minutes+":"+seconds + " Date: " + days[int(dayWeek)] + " " + dayMonth + "." + month +"."+year
        return data

    else:
        for item in lst:
            data += item
        return int(data,16)

def getObisNumber(lst):
    value = ""
    for number in lst:
        value += str(int(number,16))
    return int(value)

if __name__ == "__main__":
    tenSecMessage = "7E A0 E2 2B 21 13 23 9A E6 E7 00 0F 00 00 00 00 0C 07 E3 06 12 02 14 2F 32 FF 80 00 80 02 19 0A 0E 4B 61 6D 73 74 72 75 70 5F 56 30 30 30 31 09 06 01 01 00 00 05 FF 0A 10 32 32 30 30 35 36 37 32 32 33 31 39 37 37 31 34 09 06 01 01 60 01 01 FF 0A 12 36 38 34 31 31 33 31 42 4E 32 34 33 31 30 31 30 34 30 09 06 01 01 01 07 00 FF 06 00 00 06 A7 09 06 01 01 02 07 00 FF 06 00 00 00 00 09 06 01 01 03 07 00 FF 06 00 00 00 00 09 06 01 01 04 07 00 FF 06 00 00 01 E0 09 06 01 01 1F 07 00 FF 06 00 00 00 88 09 06 01 01 33 07 00 FF 06 00 00 02 36 09 06 01 01 47 07 00 FF 06 00 00 00 6D 09 06 01 01 20 07 00 FF 12 00 EB 09 06 01 01 34 07 00 FF 12 00 EB 09 06 01 01 48 07 00 FF 12 00 EB 83 77 7E"
    test = "7E A0 E2 2B 21 13 23 9A E6 E7 00 0F 00 00 00 00 0C 07 E4 0B 08 07 15 2C 0A FF 80 00 00 02 19 0A 0E 4B 61 6D 73 74 72 75 70 5F 56 30 30 30 31 09 06 01 01 00 00 05 FF 0A 10 35 37 30 36 35 36 37 32 37 39 36 37 35 31 34 35 09 06 01 01 60 01 01 FF 0A 12 36 38 34 31 31 32 31 42 4E 32 34 33 31 30 31 30 34 30 09 06 01 01 01 07 00 FF 06 00 00 0F 31 09 06 01 01 02 07 00 FF 06 00 00 00 00 09 06 01 01 03 07 00 FF 06 00 00 00 00 09 06 01 01 04 07 00 FF 06 00 00 01 FA 09 06 01 01 1F 07 00 FF 06 00 00 05 EA 09 06 01 01 33 07 00 FF 06 00 00 01 11 09 06 01 01 47 07 00 FF 06 00 00 05 7D 09 06 01 01 20 07 00 FF 12 00 EC 09 06 01 01 34 07 00 FF 12 00 EA 09 06 01 01 48 07 00 FF 12 00 EB 45 91 7E"
    hourlyMessage = "7E A1 2C 2B 21 13 FC 04 E6 E7 00 0F 00 00 00 00 0C 07 E3 07 09 02 14 00 05 FF 80 00 80 02 23 0A 0E 4B 61 6D 73 74 72 75 70 5F 56 30 30 30 31 09 06 01 01 00 00 05 FF 0A 10 32 32 30 30 35 36 37 32 32 33 31 39 37 37 31 34 09 06 01 01 60 01 01 FF 0A 12 36 38 34 31 31 33 31 42 4E 32 34 33 31 30 31 30 34 30 09 06 01 01 01 07 00 FF 06 00 00 01 6C 09 06 01 01 02 07 00 FF 06 00 00 00 00 09 06 01 01 03 07 00 FF 06 00 00 00 00 09 06 01 01 04 07 00 FF 06 00 00 01 42 09 06 01 01 1F 07 00 FF 06 00 00 00 85 09 06 01 01 33 07 00 FF 06 00 00 00 5C 09 06 01 01 47 07 00 FF 06 00 00 00 3F 09 06 01 01 20 07 00 FF 12 00 EB 09 06 01 01 34 07 00 FF 12 00 EB 09 06 01 01 48 07 00 FF 12 00 EB 09 06 00 01 01 00 00 FF 09 0C 07 E3 07 09 02 14 00 05 FF 80 00 80 09 06 01 01 01 08 00 FF 06 00 38 DE 2A 09 06 01 01 02 08 00 FF 06 00 00 00 00 09 06 01 01 03 08 00 FF 06 00 00 00 1F 09 06 01 01 04 08 00 FF 06 00 09 00 85 83 77 7E"
    realMessage = "7E A0 E2 2B 21 13 23 9A E6 E7 00 0F 00 00 00 00 0C 07 E4 0B 07 06 00 0D 0A FF 80 00 00 02 19 0A 0E 4B 61 6D 73 74 72 75 70 5F 56 30 30 30 31 09 06 01 01 00 00 05 FF 0A 10 35 37 30 36 35 36 37 32 37 39 36 37 35 31 34 35 09 06 01 01 60 01 01 FF 0A 12 36 38 34 31 31 32 31 42 4E 32 34 33 31 30 31 30 34 30 09 06 01 01 01 07 00 FF 06 00 00 04 59 09 06 01 01 02 07 00 FF 06 00 00 00 00 09 06 01 01 03 07 00 FF 06 00 00 00 00 09 06 01 01 04 07 00 FF 06 00 00 01 D3 09 06 01 01 1F 07 00 FF 06 00 00 01 44 09 06 01 01 33 07 00 FF 06 00 00 01 4E 09 06 01 01 47 07 00 FF 06 00 00 01 0E 09 06 01 01 20 07 00 FF 12 00 EB"
    
    jsonMessage = hanDecoding(test)
    print(jsonMessage + "\n")
    jsonMessage = hanDecoding(realMessage)
    print(jsonMessage + "\n")
    jsonMessage = hanDecoding(tenSecMessage)
    print(jsonMessage + "\n")
    jsonMessage = hanDecoding(hourlyMessage)
    print(jsonMessage)
    