from labjack import ljm

def main():
    try:
        daqHandle = ljm.openS("T7", "TCP", "ANY")
    except Exception as e:
        raise e

    daqInfo = ljm.getHandleInfo(daqHandle)
    print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
          "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
          (daqInfo[0], daqInfo[1], daqInfo[2], ljm.numberToIP(daqInfo[3]), daqInfo[4], daqInfo[5]))

    if (daqInfo[0] == ljm.constants.dtT7):
        intervalHandle = 1
        ljm.startInterval(intervalHandle, 10*1000) # Interval in us

        while True:
            try:

                aNames = ["AIN14"]
                numFrames = len(aNames)
                aValues = ljm.eReadNames(daqHandle, numFrames, aNames)
                print("inputs  : " +
                      "".join(["%s = %f, " % (aNames[j], aValues[j]) for j in range(numFrames)]))

                # Repeat every 1 second
                skippedIntervals = ljm.waitForNextInterval(intervalHandle)
                if skippedIntervals > 0:
                    print("\nSkippedIntervals: %s" % skippedIntervals)
            except Exception as e:
                raise e
                break
            except KeyboardInterrupt: # Extend to save button interrupt
                break

    # Close T7 Connection
    ljm.cleanInterval(intervalHandle)
    ljm.close(daqHandle)

if __name__ == '__main__':
    main()