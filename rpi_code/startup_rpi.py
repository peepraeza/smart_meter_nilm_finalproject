import time
import threading
import os

def startprgm(i):
    print "Running thread %d" % i
    if (i == 0):
        time.sleep(1)
        print('Running: insert_influxdb.py')
        os.system("sudo python /home/pi/Desktop/project_code/smart_meter_nilm_finalproject/rpi_code/insert_influxdb.py")
    elif (i == 1):
        print('Running: query__to_firebase.py')
        time.sleep(1)
<<<<<<< HEAD
        os.system("sudo python /home/pi/Desktop/project_code/smart_meter_nilm_finalproject/rpi_code/query__to_firebase.py")
=======
        os.system("sudo python /home/pi/Desktop/project_code/smart_meter_nilm_finalproject/rpi_code/query_to_firebase.py")
>>>>>>> refs/remotes/origin/master
    else:
        pass

for i in range(2):
    t = threading.Thread(target=startprgm, args=(i,))
    t.start()
