import time
from influxdb import InfluxDBClient
from firebase import firebase
from datetime import datetime
import threading
import calendar
from dateutil.parser import parse

status_connect = 0		# check status connection with Internet
time_disconnect = ""
time_reconnect = ""
# Main function for upload data from InfluxDB to Firebase all time
def insertdb():
	global status_connect, time_disconnect, time_reconnect
	time.sleep(20)
	client = InfluxDBClient(host='192.168.0.111', port=8086, username='peepraeza', password='029064755')
	client.switch_database('test_energy')
	while(True):
<<<<<<< HEAD
                try:
		    results = client.query(("SELECT * from %s ORDER by time DESC LIMIT 1") % ('energy_monitor'))
                    points = results.get_points()
                    for item in points:
                            time_obj = parse(item['time'])
                            unixtime = (calendar.timegm(time_obj.timetuple()))
			    real1 = item['realpower1']
			    real2 = item['realpower2']
			    real3 = item['realpower3']
			    real4 = item['realpower4']
                            try:
                                    firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
                                    firebases.post('/test_again',{"pee_time":unixtime,"test":"Peeja", 
                                    #"Irms1":item['irms1'], "Irms2":item['irms2'], "Irms3":item['irms3'], "Irms4":item['irms4'],
                                    #"S1":item['apparentpower1'], "S2":item['apparentpower1'], "S3":item['apparentpower3'], "S4":item['apparentpower4'],
                                    "real1":real1, "real2":real2, "real3":real3, "real4":real4, "test2":"PEEEJA"})
                                    print(unixtime, real1, real2, real3, real4)
                                    if(status_connect == 1): # if Internet connection reconnect
                                            time_reconnect = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')	# keep last time that internet reconnect
                                            status_connect = 2	# status change from 1 to 2 
                            except:
                                    if (status_connect == 0): # if Internet connection disconnected 
                                            time_disconnect = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')	# keep first time that internet disconnected
                                    status_connect = 1	# status change from 0 to 1 
                                    print("Data Can't add")
=======
		results = client.query(("SELECT * from %s ORDER by time DESC LIMIT 1") % ('energy_monitor'))
		points = results.get_points()
		for item in points:
			time_obj = parse(item['time'])
			unixtime = (calendar.timegm(time_obj.timetuple())*1000)
			try:
				firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
				firebases.post('/test_again',{"time":unixtime, "Irms1":item['irms1'], "Irms2":item['irms2'], "Irms3":item['irms3'], "Irms4":item['irms4'],
				"S1":item['apparentpower1'], "S2":item['apparentpower2'], "S3":item['apparentpower3'], "S4":item['apparentpower4'],
				"P1":item['realpower1'], "P2":item['realpower2'], "P3":item['realpower3'], "P4":item['realpower4']})
				print("I1:"+item['irms1']+" I2:"+item['irms2'])
				print("S1:"+item['apparentpower1']+" S2:"+item['apparentpower2'])
				print(unixtime)
				if(status_connect == 1): # if Internet connection reconnect
					time_reconnect = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')	# keep last time that internet reconnect
					status_connect = 2	# status change from 1 to 2 
			except:
				if (status_connect == 0): # if Internet connection disconnected 
					time_disconnect = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')	# keep first time that internet disconnected
				status_connect = 1	# status change from 0 to 1 
				print('Data not added')
>>>>>>> 4e4f7eaf03eb740672d55f16e31cca47a60bd48a

                    print("disconnect:"+time_disconnect)
                    print("reconnect:"+time_reconnect)
                except:
                    print("Can't Query")
                time.sleep(2)

# Secondary function for Backup data when the Internet disconnected
def insertdb2():
	global status_connect, time_disconnect, time_reconnect
	time.sleep(20)
	client = InfluxDBClient(host='192.168.0.111', port=8086, username='peepraeza', password='029064755')
	client.switch_database('test_energy')
	connect_db_status = 0
	while (True):
		if(status_connect == 2): # if status connection is 2
			firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
			# Query data from time since the Internet disconnected to the Internet reconnected
			results = client.query(("SELECT * FROM %s where time >= '%s' and time <= '%s'") % ('energy_monitor', time_disconnect, time_reconnect))
			points = results.get_points()
			for item in points:
				time_obj = parse(item['time'])
				unixtime = (calendar.timegm(time_obj.timetuple()))
				firebases.post('/test_again',{"time":unixtime, 
				    "Irms1":item['irms1'], "Irms2":item['irms2'], "Irms3":item['irms3'], "Irms4":item['irms4'],
				    "S1":item['apparentpower1'], "S2":item['apparentpower1'], "S3":item['apparentpower3'], "S4":item['apparentpower4'],
				    "P1":item['realpower1'], "P2":item['realpower2'], "P3":item['realpower3'], "P4":item['realpower4']})
				print("ADDED 2 already")
				status_connect = 0 	# after finish uploaded whole data to firebase, status connection return to 0 
				time.sleep(1)
			else:
				print("Waiting for disconnect network")
				time.sleep(5)

th1 = threading.Thread(target = insertdb).start()
th2 = threading.Thread(target = insertdb2).start()
