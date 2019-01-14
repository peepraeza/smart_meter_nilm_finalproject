import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime
from firebase import firebase
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
	message = str(msg.payload)
	time_unix = int(time.time())
	current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	pieces = message.split(',')
	firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
	if(pieces[0] == "START" and pieces[-1] == "END"):
		json_firebase = {
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
		
		json_influx = [
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
		print("firebase_time", time_unix)
		client_db.write_points(json_influx)
		firebases.post('/energy',json_firebase)
		time.sleep(1)
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
