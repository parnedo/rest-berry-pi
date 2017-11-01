from model import models


class Raspberry:
    def __init__(self):
        self._model = None
        self._setup = None
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
           self._model.setupPin(int(pin['pin']), pin['es'], pin['initial'])
        
    def getSetup(self):
        if self._setup:
          return self._setup
        else :
          return "Setup for the card is not configured"

    def status(self, data):
        for pin in data['pins']:
            pin_id    = int(pin['pin'])
            pin_value = pin['value']
            self._model.setPinValue(pin_id, pin_value)

    def getStatus(self):
        if not self._model:
          return "Model for the card is not configured"
        if not self._setup:
          return "Setup for the card is not configured"
        output = {}
        output ['pins'] = []
        for pin in self._setup ['pins']:
            single_pin = {}
            single_pin['pin'] = pin['pin']
            single_pin['value'] = self._model.getPinValue(int(pin['pin']))
            output['pins'].append(single_pin)
        return output 

