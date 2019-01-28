from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
from datetime import datetime
from firebase import firebase
import time
import json
import calendar
from dateutil.parser import parse
import threading

status = 0
yesterday = ""
date_now = ""

def convert_time(date):
    time_obj = parse(date)
    unixtime = (calendar.timegm(time_obj.timetuple()))
    whole_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(unixtime-25200))
    return whole_time

current_date =  datetime.utcnow().strftime('%Y-%m-%dT')
def check_date():
    global status, yesterday, date_now
    while (True):
        if(current_date != datetime.utcnow().strftime('%Y-%m-%dT')):
            print("change time")
            yesterday = convert_time(current_date)
            date_now = convert_time(datetime.utcnow().strftime('%Y-%m-%dT'))
            print(date_now)
            status = 1
        else:
            print("same time")
            print(current_date)
            status = 0

        time.sleep(1)

def query_to_firebase():
    client_influx = InfluxDBClient(host='localhost', port=8086, username='peepraeza', password='029064755')
    client_influx.switch_database('test_energy')
    global status, yesterday, date_now
    json = {}
    p1, p2, p3, p4  = [], [], [], []
    s1, s2, s3, s4  = [], [], [], []
    i1, i2, i3, i4  = [], [], [], []
    p1_wh, p2_wh, p3_wh, p4_wh = [], [], [], []
    time = []
    while (status == 1 or status == 2):
        if(status == 1):
            results = client_influx.query(("SELECT * FROM %s where time >= '%s' and time <= '%s'") % ('energy_monitor', yesterday, date_now))
            points = results.get_points()
            for item in points:
                time_obj = parse(item['time'])
                unixtime = (calendar.timegm(time_obj.timetuple()))
                time.append(unixtime)
                p1.append(item['P1'])
                p2.append(item['P2'])
                p3.append(item['P3'])
                p4.append(item['P4'])

                s1.append(item['S1'])
                s2.append(item['S2'])
                s3.append(item['S3'])
                s4.append(item['S4'])

                i1.append(item['I1'])
                i2.append(item['I2'])
                i3.append(item['I3'])
                i4.append(item['I4'])

                p1_wh.append(item['P1_wh'])
                p2_wh.append(item['P2_wh'])
                p3_wh.append(item['P3_wh'])
                p4_wh.append(item['P4_wh'])

            data = {"time":time,
                    "P1": p1, "P2": p2, "P3": p3, "P4": p4,
                    "S1": s1, "S2": s2, "S3": s3, "S4": s4,
                    "I1": i1, "I2": i2, "I3": i3, "I4": i4,
                    "P1_wh": sum(p1_wh), "P2_wh": sum(p2_wh), "P3_wh": sum(p3_wh), "P4_wh": sum(p4_wh)
            }
            json[yesterday] = data
            print("query Ja")
            print(yesterday, date_now)
            print("finished query")
            query = True

        if(query):
            try:
                print(json)
                print("uploaded to firebase")
                status = 0
                yesterday = ""
                date_now = ""
                query = False
            except:
                status = 2

        time.sleep(10)


th1 = threading.Thread(target = check_date).start()
th2 = threading.Thread(target = query_to_firebase).start()

