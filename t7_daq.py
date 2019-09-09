#!/usr/bin/env python
from datetime import datetime
import sys
import numpy as np
import json
from labjack import ljm

import collections
from collections import OrderedDict
from analogsensor import AnalogLJSensor
from digitalsensor import DigitalLJSensor

analog_sensors = collections.OrderedDict()
digital_sensors = collections.OrderedDict()

with open('darkstar_t7.json', 'r') as f:
  config_data = f.read()
  config_dict = json.loads(config_data.decode('utf-8'), object_pairs_hook=OrderedDict)

for sensor in config_dict['Analog Sensors']:
	analog_sensors[sensor['Name']]=AnalogLJSensor(sensor['Name'], sensor['PChannel'], sensor['NChannel'], sensor['range'], sensor['slope'], sensor['intercept'],sensor['ef_index'])    
for sensor in config_dict['Digital Sensors']:
	digital_sensors[sensor['Name']]=DigitalLJSensor(sensor['Name'], sensor['Address'])

# Open first found LabJack
handle = ljm.openS("T7", "ANY", "ANY")  # Any device, Any connection, Any identifier
# handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier
# handle = ljm.openS("T4", "ANY", "ANY")  # T4 device, Any connection, Any identifier
# handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")  # Any device, Any connection, Any identifier

info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
	  "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
	  (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

# deviceType = info[0]
aScanList = []
channelNames = []

# Stream Configuration
for sensorName, sensor in analog_sensors.items():
    if sensor is not None:
       aScanList.append(int(sensor.getPositiveChannel()))
       channelNames.append(str(sensor.getName()))
       print(int(sensor.getPositiveChannel()))
       print(str(sensor.getName()))

print "Scan list" , aScanList

aWriteNames = []
aWriteValues = []
aScanListNames = []
# print(type(analog_sensors))
# Stream Configuration
for sensor in analog_sensors:
	pChannel = str(analog_sensors[sensor].getPositiveChannel())
	nChannel = int(analog_sensors[sensor].getNegativeChannel())
	aScanListNames.append("AIN"+pChannel)
	if(nChannel > 0):
		print("configuring negative channel")
		aWriteNames.append("AIN"+pChannel+"_NEGATIVE_CH")
		aWriteValues.append(nChannel)
	if(int(analog_sensors[sensor].getExtendedFeatures())>0):
		aWriteNames.append("AIN"+pChannel+"_EF_INDEX")
		aWriteValues.append(int(analog_sensors[sensor].getExtendedFeatures()))



print "Scan list names" , aScanListNames
print "Names written" , aWriteNames
print "Values written" , aWriteValues


ljm.eWriteNames(handle, len(aWriteNames), aWriteNames, aWriteValues)

results = ljm.eReadNames(handle, len(aWriteNames), aWriteNames)


print("\neReadNames results: ")
for i in range(len(aWriteNames)):
    print("    Name - %s, value : %d" % (aWriteNames[i], results[i]))


aReadListNames = []
channelNames = []

# Read Configuration
for sensorName, sensor in analog_sensors.items():
    if sensor is not None:
    	channelNames.append(str(sensor.getName()))
    	if(int(sensor.getExtendedFeatures()) > 0):
    		aReadListNames.append("AIN"+str(sensor.getPositiveChannel())+"_EF_READ_A")
    	else:
    		aReadListNames.append("AIN"+str(sensor.getPositiveChannel()))

results = ljm.eReadNames(handle, len(aReadListNames), aReadListNames)

for i in range(len(aReadListNames)):
    print("    Name - %s, value : %f" % (channelNames[i], results[i]))

'''
aScanListNames = ["AIN14", "AIN98", "AIN99"]  # Scan list names to stream
numAddresses = len(aScanListNames)
aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
scanRate = 100
scansPerRead = int(scanRate / 2)
typeK = thermocouples['K']

def device_temp(ic_voltage):
	return ic_voltage*-92.6+467.6
try:
	# When streaming, negative channels and ranges can be configured for
	# individual analog inputs, but the stream has only one settling time and
	# resolution.

	# LabJack T7 and other devices configuration

	# Ensure triggered stream is disabled.
	ljm.eWriteName(handle, "STREAM_TRIGGER_INDEX", 0)

	# Enabling internally-clocked stream.
	ljm.eWriteName(handle, "STREAM_CLOCK_SOURCE", 0)

	# All negative channels are single-ended, AIN0 and AIN1 ranges are
	# +/-10 V, stream settling is 0 (default) and stream resolution index
	# is 0 (default).
	aNames = ["AIN98_NEGATIVE_CH","AIN99_NEGATIVE_CH", "AIN98_RANGE", "AIN99_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"]
	aValues = [106, 107, 1, 1, 0, 0]
	# Write the analog inputs' negative channels (when applicable), ranges,
	# stream settling time and stream resolution configuration.
	numFrames = len(aNames)
	ljm.eWriteNames(handle, numFrames, aNames, aValues)

	# Configure and start stream
	scanRate = ljm.eStreamStart(handle, scansPerRead, numAddresses, aScanList, scanRate)
	print("\nStream started with a scan rate of %0.0f Hz." % scanRate)

	print("\nPerforming %i stream reads." % MAX_REQUESTS)
	start = datetime.now()
	totScans = 0
	totSkip = 0  # Total skipped samples

	i = 1
	while i <= MAX_REQUESTS:
		ret = ljm.eStreamRead(handle)

		aData = ret[0]
		# print(type(aData))
		# print(aData)
		a = np.asarray(aData)
		# print(a.shape)
		scans = len(aData) / numAddresses
		totScans += scans
		b = np.reshape(a,(int(scans), numAddresses))
		# print(b)
		c = np.average(b[:, 1:],axis=0)
		# print(c)
		Tref = device_temp(aData[0])
		print(type(Tref))
		print("Device temp: ", Tref)
		for tc_v in c:
			# print("Temperature: ", tc.thermocouple('K',tc_v,'V','K'))
			print("Scaled Temp: ", typeK.inverse_KmV(tc_v*1000, Tref))

		# Count the skipped samples which are indicated by -9999 values. Missed
		# samples occur after a device's stream buffer overflows and are
		# reported after auto-recover mode ends.
		curSkip = aData.count(-9999.0)
		totSkip += curSkip

		print("\neStreamRead %i" % i)
		ainStr = ""
		for j in range(0, numAddresses):
			ainStr += "%s = %0.5f, " % (aScanListNames[j], aData[j])
		# print("  1st scan out of %i: %s" % (scans, ainStr))
		# print("Device Temp: ", device_temp(aData[0]))
		#print("  Scans Skipped = %0.0f, Scan Backlogs: Device = %i, LJM = "
		 #     "%i" % (curSkip/numAddresses, ret[1], ret[2]))
		i += 1

	end = datetime.now()

	print("\nTotal scans = %i" % (totScans))
	tt = (end - start).seconds + float((end - start).microseconds) / 1000000
	print("Time taken = %f seconds" % (tt))
	print("LJM Scan Rate = %f scans/second" % (scanRate))
	print("Timed Scan Rate = %f scans/second" % (totScans / tt))
	print("Timed Sample Rate = %f samples/second" % (totScans * numAddresses / tt))
	print("Skipped scans = %0.0f" % (totSkip / numAddresses))
except ljm.LJMError:
	ljme = sys.exc_info()[1]
	print(ljme)
except Exception:
	e = sys.exc_info()[1]
	print(e)

try:
	print("\nStop Stream")
	ljm.eStreamStop(handle)
except ljm.LJMError:
	ljme = sys.exc_info()[1]
	print(ljme)
except Exception:
	e = sys.exc_info()[1]
	print(e)

'''
# Close handle
ljm.close(handle)