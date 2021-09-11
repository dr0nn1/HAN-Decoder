#!/usr/bin/python
from influxdb import InfluxDBClient

client = InfluxDBClient(host='192.168.0.51', port=8086, database='ams')

def writeToInflux (data):
   # client.write_points(data)
    try:
        client.write_points([data], time_precision='s', database='ams', retention_policy='ams_retention')
    except:
        print("what")
