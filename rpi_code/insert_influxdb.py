from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

client_db = InfluxDBClient(host='192.168.0.105', port=8086, username='peepraeza', password='029064755')
#client_db.create_database('test_energy')
client_db.switch_database('test_energy')
#Callbacks
try:
	print("sleep 10 sec")
	time.sleep(10)
	results = client_db.query(("SELECT * FROM %s GROUP BY * ORDER BY DESC LIMIT 1") % ('energy_monitor'))
	points = results.get_points()
	for item in points:
	    whole_p1 = item['whole_p1']
	    whole_p2 = item['whole_p2']
	    whole_p3 = item['whole_p3']
	    whole_p4 = item['whole_p4']
except:
	whole_p1, whole_p2, whole_p3, whole_p4 = 0,0,0,0

def on_connect(client, userdata, flags, rc):
    print("Connected with Code :"+ str(rc))
    # Subscribe Topic
    client.subscribe("esp8266")

def on_message(client, userdata, msg):
    insertdb(str(msg.payload))

def insertdb(message):
    pieces = message.split(',')
    global whole_p1, whole_p2, whole_p3, whole_p4
    if(pieces[0] == "b'START" and "END" in pieces[13]):
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        p1_wh = float(pieces[5])/1800
        p2_wh = float(pieces[6])/1800
        p3_wh = float(pieces[7])/1800
        p4_wh = float(pieces[8])/1800
        whole_p1 += p1_wh
        whole_p2 += p2_wh
        whole_p3 += p3_wh
        whole_p4 += p4_wh

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

                "S1": float(pieces[9]),
                "S2": float(pieces[10]),
                "S3": float(pieces[11]),
                "S4": float(pieces[12]),
                
                "P1_wh" : p1_wh,
                "P2_wh" : p2_wh,
                "P3_wh" : p3_wh,
                "P4_wh" : p4_wh,

                "whole_p1" : whole_p1,
                "whole_p2" : whole_p2,
                "whole_p3" : whole_p3,
                "whole_p4" : whole_p4
            }
        }]
        print(whole_p1)
        client_db.write_points(json_body)
        print("influxdb complete!", current_time)
    else:
        print("Miss some data")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.105", 1883, 60)
client.username_pw_set("peepraeza", "029064755")

client.loop_forever();
