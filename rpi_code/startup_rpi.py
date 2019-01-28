import time
import threading
import os
# os.system("python /home/pi/Desktop/smart_meter_nilm_finalproject/rpi_code/test_time.py")
def startprgm(i):
    print("Running thread %d" % i)
    if (i == 0):
        print('Running: insert_influxdb.py')
        os.system("python /home/pi/Desktop/smart_meter_nilm_finalproject/rpi_code/insert_influxdb.py")
    elif (i == 1):
        print('Running: query_to_firebase.py')
        os.system("python /home/pi/Desktop/smart_meter_nilm_finalproject/rpi_code/query_to_firebase.py")
    else:
        pass

for i in range(2):
    t = threading.Thread(target=startprgm, args=(i,))
    t.start()
