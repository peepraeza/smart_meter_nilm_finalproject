#!/usr/bin/python
import csv
import os

os.chdir('/home/pi/Desktop/smart_meter_nilm_finalproject/rpi_code/')
with open('whole_power.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        break
