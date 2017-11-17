from model import models
from ds18b20 import DS18B20
import Adafruit_DHT

class Raspberry:
    def __init__(self):
        self._model = None
        self._setup = None
        self._type_AM2302=[]
        self._type_DS18B20=[]
        import os.path
        if os.path.isfile('/sys/firmware/devicetree/base/model'):
           self._model = models[open('/sys/firmware/devicetree/base/model','r').read().replace('\x00','')]

    def getModelInfo(self):
        if self._model:
          return self._model.getInfo()
        else :
          return "Model for the card is not configured"
          
    def setup(self, config):
        self._setup = config
        self._model.setupBoardMode(config['board_mode'])
        for pin in config['pins']:
           if "type" not in pin.keys():
             print "Setting pin[",pin['pin'],"] es [",pin['es'],"] with initial [",pin['initial'],"]"
             self._model.setupPin(pin['pin'], pin['es'], pin['initial'])
           else:
             print "Setting pin[",pin['pin'],"] as [",pin['type'],"]"
             if pin["type"] == "AM2302":
                 self._type_AM2302.append(pin["pin"])
             if pin["type"] == "DS18B20":
                 self._type_DS18B20.append(pin["pin"])
        
    def getSetup(self):
        if self._setup:
          return self._setup
        else :
          return "Setup for the card is not configured"

    def status(self, iData, iPin = None):
        if iPin is not None:
            self._model.setPinValue(iPin, iData['value'])
        else:
            for pin in iData['pins']:
                pin_id    = pin['pin']
                pin_value = pin['value']
                self._model.setPinValue(pin_id, pin_value)

    def getStatusByPin(self, iPin):
        single_pin = {}
        single_pin['pin'] = iPin
        print iPin, self._type_AM2302,self._type_DS18B20
        if iPin in self._type_AM2302:
            single_pin['type'] = "AM2302"
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, iPin)
            single_pin['humidity'] = humidity
            single_pin['temperature'] = temperature
        elif iPin in self._type_DS18B20:
            for value in DS18B20().read():
                single_pin[value['name']] = value['temperature']
        else:
            single_pin['value'] = self._model.getPinValue(iPin)
        return single_pin 

    def getStatus(self):
        if not self._model:
          return "Model for the card is not configured"
        if not self._setup:
          return "Setup for the card is not configured"
        output = {}
        output ['pins'] = []
        for pin in self._setup ['pins']:
            output['pins'].append(self.getStatusByPin(pin['pin']))
        return output 

