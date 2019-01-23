
from datetime import datetime

import time
from pytz import timezone
tz = timezone('US/Pacific')
#date = datetime.datetime(2011, 01, 01, tzinfo=tz)
time_now = time.time()
o = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time_now-25200))
t = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
#o = datetime.fromtimestamp(time_now-25200).strftime('%Y-%m-%dT%H:%M:%SZ')
print(t,o)
#print(int(time_now) - 60, time_now)

