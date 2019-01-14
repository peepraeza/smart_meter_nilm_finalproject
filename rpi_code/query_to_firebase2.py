import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime
from firebase import firebase
import time
import json

#Callbacks
def on_connect(client, userdata, flags, rc):
	print("Connected with Code :"+ str(rc))
	# Subscribe Topic
	client.subscribe("esp8266")

def on_message(client, userdata, msg):
	message = str(msg.payload)
	time_unix = int(time.time())
	pieces = message.split(',')
	firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
	if(pieces[0] == "START" and pieces[-1] == "END"):
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

	        "S1": float(pieces[9]),
	        "S2": float(pieces[10]),
	        "S3": float(pieces[11]),
	        "S4": float(pieces[12])  
			}
		print("firebase_time", time_unix)
		firebases.post('/energy',json_body)
		time.sleep(5)
	else:
		print("Miss some data")

# def insertdb(message):
# 	time_unix = int(time.time())
# 	pieces = message.split(',')
# 	if(pieces[0] == "START" and pieces[-1] == "END"):
# 		firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
# 		json_body = {
# 			"time": time_unix,
# 	        "I1": float(pieces[1]),
# 	        "I2": float(pieces[2]),
# 	        "I3": float(pieces[3]),
# 	        "I4": float(pieces[4]),

# 	        "P1": float(pieces[5]),
# 	        "P2": float(pieces[6]),
# 	        "P3": float(pieces[7]),
# 	        "P4": float(pieces[8]),

# 	        "S1": float(pieces[9]),
# 	        "S2": float(pieces[10]),
# 	        "S3": float(pieces[11]),
# 	        "S4": float(pieces[12])  
# 			}
# 		print("firebase_time", time_unix)
# 		firebases.post('/energy',json_body)
# 		time.sleep(3)
# 	else:
# 		print("Miss some data")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.111", 1883, 60)
client.username_pw_set("peepraeza", "029064755")

client.loop_forever();
