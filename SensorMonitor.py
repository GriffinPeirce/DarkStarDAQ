import csv
from datetime import datetime
import sys

from labjack import ljm

def generateCSV():
    fileName = "DarkStarDAQ_" + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
    csvFile = open(fileName, 'wb')
    return [csv.writer(csvFile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL), csvFile]
def main():
    try:
        daqHandle = ljm.openS("T7", "TCP", "ANY")

        daqInfo = ljm.getHandleInfo(daqHandle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
              "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
              (daqInfo[0], daqInfo[1], daqInfo[2], ljm.numberToIP(daqInfo[3]), daqInfo[4], daqInfo[5]))

        # Stream Configuration
        aScanListNames = ["AIN0", "AIN1", "AIN14"]  # Scan list names to stream
        numAddresses = len(aScanListNames)
        aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
        scanRate = 10
        scansPerRead = int(scanRate / 2)

        csvWriter, csvFile = generateCSV()

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
            scanRate = ljm.eStreamStart(daqHandle, scansPerRead, numAddresses, aScanList, scanRate)
            print("\nStream started with a scan rate of %0.0f Hz." % scanRate)

            start = datetime.now()
            totScans = 0
            totSkip = 0  # Total skipped samples

            while True:
                try:
                    ret = ljm.eStreamRead(daqHandle)

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
                    print aData
                    csvWriter.writerow(aData)   #use write rows once separated with numpy array
                    print ("Test")
                except Exception as e:
                    raise e
                    break
                except KeyboardInterrupt: # Extend to save button interrupt
                    break
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