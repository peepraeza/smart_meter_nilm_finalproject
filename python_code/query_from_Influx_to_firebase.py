import time
from influxdb import InfluxDBClient
from firebase import firebase
from datetime import datetime
import threading

status_connect = 0
time_disconnect = ""
time_reconnect = ""
client = InfluxDBClient(host='192.168.0.106', port=8086, username='peepraeza', password='029064755')
client.switch_database('test_energy')
		
def insertdb():
        time.sleep(60)
        t = 1
        print("Waited 1mins")
	global status_connect, time_disconnect, time_reconnect
	while(True):
            if(t == 1):
		results = client.query(("SELECT * FROM %s where time > now() - 5s") % ('energy_monitor'))
		points = results.get_points()
		for item in points:
			try:
				firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
				firebases.post('/bbb',{"time":item['time'], 
				"Irms1":item['irms1'], "Irms2":item['irms2'], "Irms3":item['irms3'], "Irms4":item['irms4'],
				"S1":item['apparentpower1'], "S2":item['apparentpower1'], "S3":item['apparentpower3'], "S4":item['apparentpower4'],
				"P1":item['realpower1'], "P2":item['realpower2'], "P3":item['realpower3'], "P4":item['realpower4']})
				if(status_connect == 1):
					time_reconnect = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
					status_connect = 2
			except:
				if (status_connect == 0):
					time_disconnect = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
				status_connect = 1
		print("ADD 1")
		print("disconnect:"+time_disconnect)
		print("reconnect:"+time_reconnect)
		time.sleep(1.5)
	    else:
                print("No Connect InfluxDB")

def insertdb2():
	global status_connect, time_disconnect, time_reconnect
	connect_db_status = 0
	while (True):
	    if(status_connect == 2):
		firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
                results = client.query(("SELECT * FROM %s where time >= '%s' and time <= '%s'") % ('energy_monitor', time_disconnect, time_reconnect))
		points = results.get_points()
		for item in points:
		    firebases.post('/bbb',{"time":item['time'], 
			    "Irms1":item['irms1'], "Irms2":item['irms2'], "Irms3":item['irms3'], "Irms4":item['irms4'],
			    "S1":item['apparentpower1'], "S2":item['apparentpower1'], "S3":item['apparentpower3'], "S4":item['apparentpower4'],
			    "P1":item['realpower1'], "P2":item['realpower2'], "P3":item['realpower3'], "P4":item['realpower4']})
		print("ADDED 2 already")
		status_connect = 0
		time.sleep(1)
	    else:
		print("Waiting for disconnect network")
		time.sleep(5)

th1 = threading.Thread(target = insertdb).start()
th2 = threading.Thread(target = insertdb2).start()