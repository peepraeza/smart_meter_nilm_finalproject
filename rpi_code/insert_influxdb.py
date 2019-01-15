import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime
import time
import json

client_db = InfluxDBClient(host='192.168.0.111', port=8086, username='peepraeza', password='029064755')
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
	if(pieces[0] == "START" and pieces[-1] == "END"):
		current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		json_body = [
		{
		    "measurement": "energy_monitor",
		    "time": current_time,
		    "fields": {
		        "irms1": float(pieces[1]),
		        "irms2": float(pieces[2]),
		        "irms3": float(pieces[3]),
		        "irms4": float(pieces[4]),

		        "realpower1": float(pieces[5]),
		        "realpower2": float(pieces[6]),
		        "realpower3": float(pieces[7]),
		        "realpower4": float(pieces[8]),

		        "apparentpower1": float(pieces[9]),
		        "apparentpower2": float(pieces[10]),
		        "apparentpower3": float(pieces[11]),
		        "apparentpower4": float(pieces[12])
		    }
		}]
		client_db.write_points(json_body)
		print("influxdb complete!", current_time)
	else:
		print("Miss some data")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.111", 1883, 60)
client.username_pw_set("peepraeza", "029064755")

client.loop_forever();
