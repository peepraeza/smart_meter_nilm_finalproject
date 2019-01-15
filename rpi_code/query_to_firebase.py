import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
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

#Callbacks
def on_connect(client, userdata, flags, rc):
	print("Connected with Code :"+ str(rc))
	# Subscribe Topic
	client.subscribe("esp8266")

def on_message(client, userdata, msg):
	insertdb(str(msg.payload))

def insertdb(message):
	global status_connect, time_disconnect, time_reconnect
	time_unix = int(time.time())
	pieces = message.split(',')
	if(pieces[0] == "START" and pieces[-1] == "END"):
		firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")	
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
		time_start = int(time.time())
		try:
			firebases.post('/energy',json_firebase)
			print("firebase complete!", time_unix)
			if(status_connect == 1):
				time_reconnect = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
				status_connect = 2
		except:
			if(status_connect == 0):
				time_disconnect = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
			status_connect = 1
		time_end = int(time.time())
		print(status_connect, time_end - time_start)
		time.sleep(4)
	else:
		print("Miss some data")

def backup_data():
	global status_connect, time_disconnect, time_reconnect
	while(True):
		if(status_connect == 2):
			client_influx = InfluxDBClient(host='192.168.0.111', port=8086, username='peepraeza', password='029064755')
			client_influx.switch_database('test_energy')
			firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
			print("dis", time_disconnect, "re", time_reconnect)
			results = client_influx.query(("SELECT * FROM %s where time >= '%s' and time <= '%s'") % ('energy_monitor', time_disconnect, time_reconnect))
			points = results.get_points()
			for item in points:
				time_obj = parse(item['time'])
				unixtime = (calendar.timegm(time_obj.timetuple()))
				firebases.post('/energy',{"time":unixtime, 
				    "I1":item['I1'], "I2":item['I2'], "I3":item['I3'], "I3":item['I4'],
				    "S1":item['S1'], "S2":item['S2'], "S3":item['S3'], "S4":item['S4'],
				    "P1":item['P1'], "P2":item['P2'], "P3":item['P3'], "P4":item['P4']})
				print(unixtime)
			status_connect = 0
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

client.connect("192.168.0.111", 1883, 60)
client.username_pw_set("peepraeza", "029064755")

client.loop_forever();
