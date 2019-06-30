import unittest

class LJSensor(unittest.TestCase):
    def __init__(self):

        self.__positive_channel = None
        self.__negative_channel = None
        self.__name = None
        self.__resolution = None
        self.__analog_EF = None
        self.__calibration_slope = None
        self.__calibration_intercept = None

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

    def setResolution(self, res):
        assert isinstance(res, int), 'Resolution must be integer!'
        if (res > 12 or res < 0):
            self.__resolution = 1
        else:
            self.__resolution = res

    def getResolution(self):
        return self.__resolution

    def setName(self, name):
        assert isinstance(name, str), 'Name must be a string!'
        self.name = name

    def getName(self):
        return self.name

    def setPositiveChannel(self, ch):
        assert isinstance(ch, int), 'Positive channel must be an integer!'
        self.positive_channel = ch

    def setNegativeChannel(self, ch):
        assert isinstance(ch, int), 'Negative channel must be an integer!'
        self.negative_channel = ch

    def getPositiveChannel(self):
        return self.positive_channel

    def getNegativeChannel(self):
        return self.negative_channel
