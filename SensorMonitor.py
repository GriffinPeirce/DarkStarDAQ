import csv
from datetime import datetime
import sys
import numpy as np
import time

from labjack import ljm

def generateCSV():
    fileName = "DarkStarDAQ_" + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
    csvFile = open(fileName, 'wb')
    return [csv.writer(csvFile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL), csvFile]

def datetime_to_float(d):
    epoch = datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

def main():
    try:
        openTime = datetime.utcnow()
        daqHandle = ljm.openS("T7", "TCP", "ANY")

        daqInfo = ljm.getHandleInfo(daqHandle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
              "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
              (daqInfo[0], daqInfo[1], daqInfo[2], ljm.numberToIP(daqInfo[3]), daqInfo[4], daqInfo[5]))

        csvWriter, csvFile = generateCSV()
        timeHeader = ["TIME"]
        timeHeader.extend(aScanListNames)
        csvWriter.writerow(timeHeader)
        if (daqInfo[0] == ljm.constants.dtT7):

            # Disable triggered streaming
            ljm.eWriteName(daqHandle, "STREAM_TRIGGER_INDEX", 0)

            # Enabling internally-clocked stream.
            ljm.eWriteName(daqHandle, "STREAM_CLOCK_SOURCE", 0)

            # All negative channels are single-ended, AIN0 and AIN1 ranges are
            # +/-10 V, stream settling is 0 (default) and stream resolution index
            # is 0 (default).
            aNames = ["AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"]
            aValues = [ljm.constants.GND, 10.0, 0, 0]

            ljm.eWriteNames(daqHandle, len(aNames), aNames, aValues)

            # Configure and start stream
            scanStartTime = datetime_to_float(datetime.utcnow())
            lastScanStartTime = scanStartTime
            scanRate = ljm.eStreamStart(daqHandle, scansPerRead, numAddresses, aScanList, scanRate)
            print("\nStream started with a scan rate of %0.0f Hz." % scanRate)

            totScans = 0
            totSkip = 0  # Total skipped samples

            aScanClockNames = ["SYSTEM_TIMER_20HZ", "CORE_TIMER"]
            startClocks = ljm.eReadNames(daqHandle, len(aScanClockNames), aScanClockNames)
            start20HzClock = startClocks[0]
            start40MHzClock = startClocks[1]
            count40MHzRollover = 0

            # Stream Configuration
            aScanListNames = ["AIN0", "AIN1", "AIN2", "AIN3"]  # Scan list names to stream
            aScanList = ljm.namesToAddresses(len(numAddresses), aScanListNames)[0]
            scanRate = 10
            scansPerRead = int(scanRate / 2)

            # while True:
            try:
                ret = ljm.eStreamRead(daqHandle)
                scanStopTime = datetime_to_float(datetime.utcnow())

                aData = ret[0]
                scans = len(aData) / numAddresses
                totScans += scans

                # Count the skipped samples which are indicated by -9999 values. Missed
                # samples occur after a device's stream buffer overflows and are
                # reported after auto-recover mode ends.
                curSkip = aData.count(-9999.0)
                totSkip += curSkip
                ainStr = ""
                for j in range(0, numAddresses):
                    ainStr += "%s = %0.5f, " % (aScanListNames[j], aData[j])
                print("  1st scan out of %i: %s" % (scans, ainStr))
                print("  Scans Skipped = %0.0f, Scan Backlogs: Device = %i, LJM = "
                      "%i" % (curSkip/numAddresses, ret[1], ret[2]))
                timeData = np.linspace(scanStartTime, scanStopTime, num=scansPerRead)
                print timeData
                print aData
                scanData = np.array(aData)
                print scanData
                print ("Rows/Cols: ", scanData.shape)
                print ("Num address: ", numAddresses)
                splitScanData =  np.split(scanData, scansPerRead)
                print splitScanData
                print ("Rows/Cols: ", splitScanData[0].shape)
                csvWriter.writerows(splitScanData)
                verticalStackedSplitScanData = np.vstack(splitScanData)
                print verticalStackedSplitScanData
                print "Test"
                # csvWriter.writerows(verticalStackedSplitScanData)   #use write rows once separated with numpy array
            except Exception as e:
                raise e
                # break
            except KeyboardInterrupt: # Extend to save button interrupt
                pass
                # break
            # Close T7 Connection
            try:
                print("\nStop Stream")
                ljm.eStreamStop(daqHandle)
            except ljm.LJMError:
                ljme = sys.exc_info()[1]
                print(ljme)
            except Exception:
                e = sys.exc_info()[1]
                print(e)

    except ljm.LJMError:
        ljme = sys.exc_info()[1]
        print(ljme)
    except Exception:
        e = sys.exc_info()[1]
        print(e)

    csvFile.close()
    ljm.close(daqHandle)

if __name__ == '__main__':
    main()