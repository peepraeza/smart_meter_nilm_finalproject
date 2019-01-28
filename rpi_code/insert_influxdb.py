from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import csv
file = "/home/pi/Desktop/smart_meter_nilm_finalproject/rpi_code/whole_power.py"
client_db = InfluxDBClient(host='localhost', port=8086, username='peepraeza', password='029064755')
#client_db.create_database('test_energy')
client_db.switch_database('test_energy')
#Callbacks
with open(os.system(file)) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if(row):
        	array = row
whole_p1, whole_p2, whole_p3, whole_p4 = float(array[0]), float(array[1]), float(array[2]), float(array[3]) 

def insert_to_csv(data):
    with open(os.system(file), mode='w') as csv_file:
        csv_reader = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_reader.writerow(data)
        print("influxdb",data)

def on_connect(client, userdata, flags, rc):
    print("Connected with Code :"+ str(rc))
    # Subscribe Topic
    client.subscribe("esp8266")

def on_message(client, userdata, msg):
    insertdb(str(msg.payload))

def insertdb(message):
    pieces = message.split(',')
    data = []
    global whole_p1, whole_p2, whole_p3, whole_p4
    if(pieces[0] == "START" and "END" in pieces[13]):
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        p1_wh = float(pieces[5])/1800
        p2_wh = float(pieces[6])/1800
        p3_wh = float(pieces[7])/1800
        p4_wh = float(pieces[8])/1800
        whole_p1 += p1_wh
        whole_p2 += p2_wh
        whole_p3 += p3_wh
        whole_p4 += p4_wh
        data.append(whole_p1)
        data.append(whole_p2)
        data.append(whole_p3)
        data.append(whole_p4)
        insert_to_csv(data)
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
