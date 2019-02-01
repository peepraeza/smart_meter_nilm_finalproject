from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

client_db = InfluxDBClient(host='localhost', port=8086, username='peepraeza', password='029064755')
#client_db.create_database('test_energy')
client_db.switch_database('test_energy')
#Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with Code :"+ str(rc))
    # Subscribe Topic
    client.subscribe("esp8266")

def on_message(client, userdata, msg):
    insertdb(str(msg.payload))

def insertdb(message):
    pieces = message.split(',')
    if(pieces[0] == "START" and "END" in pieces[13]):
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        p1_wh = float(pieces[5])/1800
        p2_wh = float(pieces[6])/1800
        p3_wh = float(pieces[7])/1800
        p4_wh = float(pieces[8])/1800

        json_body = [
        {
            "measurement": "energy_monitor",
            "time": current_time,
            "fields": {
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
                "P4_wh" : p4_wh,
            }
        }]
        client_db.write_points(json_body)
        print("influxdb complete!", current_time)
    else:
        print("Miss some data")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.username_pw_set("peepraeza", "029064755")

client.loop_forever();
