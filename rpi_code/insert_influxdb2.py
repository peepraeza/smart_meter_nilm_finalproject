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
	firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
	json_body = {"time" : int(time.time()),
				 "data" : str(msg.payload)}
	firebases.post('/testdata',json_body)
	time.sleep(5)

# def insertdb(message):
# 	global time_unix
# 	pieces = message.split(',')
# 	if(pieces[0] == "START" and pieces[-1] == "END"):
# 		firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
# 		current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
# 		# if(time_unix != int(time.time())):
# 		# 	time_unix = int(time.time())

# 		json_body = [
# 		{
# 		    "measurement": "energy_monitor",
# 		    "time": current_time,
# 		    "fields": {
# 		        "irms1": float(pieces[1]),
# 		        "irms2": float(pieces[2]),
# 		        "irms3": float(pieces[3]),
# 		        "irms4": float(pieces[4]),

# 		        "realpower1": float(pieces[5]),
# 		        "realpower2": float(pieces[6]),
# 		        "realpower3": float(pieces[7]),
# 		        "realpower4": float(pieces[8]),

# 		        "apparentpower1": float(pieces[9]),
# 		        "apparentpower2": float(pieces[10]),
# 		        "apparentpower3": float(pieces[11]),
# 		        "apparentpower4": float(pieces[12])
# 		    }
# 		}]
# 		print("influxdb_time", time_unix)
# 		client_db.write_points(json_body)
# 		firebases.post('/energy',json_body)
# 		time.sleep(1)
# 	else:
# 		print("Miss some data")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.111", 1883, 60)
client.username_pw_set("peepraeza", "029064755")

client.loop_forever();
