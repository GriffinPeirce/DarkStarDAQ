class AnalogLJSensor():
    def __init__(self):
        self.__positive_channel = None
        self.__negative_channel = None
        self.__name = None
        self.__resolution = None
        self.__analog_EF = None
        self.__calibration_slope = None
        self.__calibration_intercept = None

    def __init__(self, name, pChannel, nChannel, res, slope, intercept, ef):
        self.__positive_channel = pChannel
        self.__negative_channel = nChannel
        self.__name = name
        self.__resolution = res
        self.__analog_EF = ef
        self.__calibration_slope = slope
        self.__calibration_intercept = intercept

    def setExtendedFeatures(self, ef):
        pass

    def getExtendedFeatures(self):
        return self.__analog_EF

    def setCalibrationSlope(self, slope):
        assert isinstance(slope, float), 'Slope must be a float!'
        self.__calibration_slope = slope

    def getCalibrationSlope(self):
        return self.__calibration_slope

    def setCalibrationIntercept(self, intercept):
        assert isinstance(intercept, float), 'Intercept must be a float!'
        self.__calibration_intercept = intercept

    def getCalibrationIntercept(self):
        return self.__calibration_intercept

    def setRange(self, rng):
        self.__range = rng

    def getRange(self):
        return self.__range

    def setName(self, name):
        assert isinstance(name, str), 'Name must be a string!'
        self.__name = name

    def getName(self):
        return self.__name

    def setPositiveChannel(self, ch):
        assert isinstance(ch, int), 'Positive channel must be an integer!'
        self.__positive_channel = ch

    def setNegativeChannel(self, ch):
        assert isinstance(ch, int), 'Negative channel must be an integer!'
        self.__negative_channel = ch

    def getPositiveChannel(self):
        return self.__positive_channel

    def getNegativeChannel(self):
        return self.__negative_channel
