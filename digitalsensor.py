class DigitalLJSensor():
    def __init__(self):
        self.__address = None
        self.__name = None

    def __init__(self, name, address):
        self.__name = name
        self.__address = address

    def setName(self, name):
        assert isinstance(name, str), 'Name must be a string!'
        self.__name = name

    def getName(self):
        return self.__name

    def setAddress(self, address):
        assert isinstance(address, int), 'Register address must be an integer!'
        self.__address = address

    def getAddress(self):
        return self.__address
