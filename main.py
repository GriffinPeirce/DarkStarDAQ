import ConfigParser
from labjack import ljm

config = ConfigParser.ConfigParser()
config.read('test_stand.ini')
config.sections()
address = config.get('LABJACK','Address')


# Open first found LabJack
handle = ljm.openS("T7", "TCP", address)

# Call eReadName to read the serial number from the LabJack.
name = "SERIAL_NUMBER"
result = ljm.eReadName(handle, name)

print("\neReadName result: ")
print("    %s = %f" % (name, result))