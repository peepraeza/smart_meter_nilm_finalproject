import csv

with open('/home/pi/Desktop/smart_meter_nilm_finalproject/rpi_code/whole_power.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        break