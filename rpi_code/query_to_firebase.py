from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
from datetime import datetime
from firebase import firebase
import time
import json
import calendar
from dateutil.parser import parse
import threading

status_connect = 0 
time_disconnect = ""
time_reconnect = ""
time_delay = 0

#Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with Code :"+ str(rc))
    # Subscribe Topic
    client.subscribe("esp8266")

def on_message(client, userdata, msg):
    insertdb(str(msg.payload))

def insertdb(message):
    global status_connect, time_disconnect, time_reconnect, time_delay
    time_unix = int(time.time())
    time_now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    # time_obj = parse(time_now)
    # unixtime = (calendar.timegm(time_obj.timetuple()))
    pieces = message.split(',')
    if(pieces[0] == "START" and "END" in pieces[13]):
        firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
        p1_wh = float(pieces[5])/1800
        p2_wh = float(pieces[6])/1800
        p3_wh = float(pieces[7])/1800
        p4_wh = float(pieces[8])/1800
        json_body = {
            "time": time_unix,
            "I1": float(pieces[1]),
            "I2": float(pieces[2]),
            "I3": float(pieces[3]),
            "I4": float(pieces[4]),

            "P1": float(pieces[5]),
            "P2": float(pieces[6]),
            "P3": float(pieces[7]),
            "P4": float(pieces[8]),

            "Q1": float(pieces[9]),
            "Q2": float(pieces[10]),
            "Q3": float(pieces[11]),
            "Q4": float(pieces[12]),
            
            "P1_wh" : p1_wh,
            "P2_wh" : p2_wh,
            "P3_wh" : p3_wh,
            "P4_wh" : p4_wh
            }
        time_start = int(time.time())
        try:
            firebases.post('/energy',json_body)
            print("firebase complete!", time_now)
            i = 0
            if(status_connect == 1):
                time_reconnect = int(time.time())
                status_connect = 2
        except:
            if(status_connect == 0):
                time_disconnect = int(time.time())
            status_connect = 1
        time_end = int(time.time())
        if(status_connect == 1 and time_delay == 0):
            time_delay = time_end - time_start
            print(time_delay)
        print(status_connect, time_end - time_start)
    else:
        print("Miss some data")

def backup_data():
    global status_connect, time_disconnect, time_reconnect, time_delay
    while(True):
        if(status_connect == 2):
            client_influx = InfluxDBClient(host='localhost', port=8086, username='peepraeza', password='029064755')
            client_influx.switch_database('test_energy')
            firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
            time_dis = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time_disconnect-25200-time_delay))
            time_re = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time_reconnect-25200))
            print("dis", time_dis, "re", time_re)
            time_start = int(time.time())
            results = client_influx.query(("SELECT * FROM %s where time >= '%s' and time <= '%s'") % ('energy_monitor', time_dis, time_re))
            time_end = int(time.time())
            print("query : ", time_end - time_start)
            points = results.get_points()
            time_start = int(time.time())
            for item in points:
                time_obj = parse(item['time'])
                unixtime = (calendar.timegm(time_obj.timetuple()))
                firebases.post('/energy',{"time":unixtime, 
                    "I1":item['I1'], "I2":item['I2'], "I3":item['I3'], "I4":item['I4'],
                    "Q1":item['Q1'], "Q2":item['Q2'], "S3":item['Q3'], "Q4":item['Q4'],
                    "P1":item['P1'], "P2":item['P2'], "P3":item['P3'], "P4":item['P4'], "Power":item['Power']})
                print(item['time'])
            time_end = int(time.time())
            print("push : ", time_end - time_start)
            status_connect = 0
            time_delay = 0
            time_disconnect = ""
            time_reconnect = ""
        elif(status_connect == 1):
            print("Disconnecting")
        else:
            print("Connection Well")
        time.sleep(10)

th1 = threading.Thread(target = backup_data).start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.username_pw_set("peepraeza", "029064755")

client.loop_forever();
