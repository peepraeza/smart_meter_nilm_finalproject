from firebase import firebase
import time
import threading
from datetime import datetime
time_now = 0
time_now = int(time.time())
firebases = firebase.FirebaseApplication("https://data-log-fb39d.firebaseio.com/")
while(True):
	time_now = int(time.time())
	json_body = {"time" : time_now}
	firebases.post('/time',json_body)
	print(time_now)
	time.sleep(2)
