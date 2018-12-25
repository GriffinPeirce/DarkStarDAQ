from abc import ABC

class LJMInput(ABC):
    
    def __init__(self, name, address):
        self.sensorName = name
        self.addressName = address
        super(ABC, self).__init__()

    @abstractmethod
    def get_sensor_name(self):
        pass