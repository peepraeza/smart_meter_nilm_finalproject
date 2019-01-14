p = {"irms1": 2, "irms2": 4, "irms3": 1, "irms4": 4}
json_influx = [
		{
		    "measurement": "energy_monitor",
		    "time": 90,
		    "fields" : p
		}]

print(json_influx)
print(p)