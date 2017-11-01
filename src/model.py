from abc import abstractmethod
from abc import ABCMeta
import RPi.GPIO as GPIO

class Model:
    __metaclass__ = ABCMeta
    def __init__(self, io, gnd, vcc5_0v, vcc3_3v, dnc, name):
        self._io      = io
        self._gnd     = gnd
        self._vcc5_0v = vcc5_0v
        self._vcc3_3v = vcc3_3v
        self._dnc     = dnc
        self._name    = name

    #@abstractmethod
    #def getInfo():
    #    pass

    def setupBoardMode(self, mode):
        if mode == 'board':
          self._mode = GPIO.BOARD
        elif mode == 'bcm':
          self._mode = GPIO.BCM
        GPIO.setmode(self._mode)

    def setupPin(self, pin, es, initial):
        print "Setting pin",[pin], "ES", [es], "initial", [initial]
        value_es = (GPIO.IN,GPIO.OUT)[es == 'out']
        value_initial = (GPIO.LOW,GPIO.HIGH)[initial == 'high']
        GPIO.setup(pin, value_es, initial=value_initial)

    def getPinValue(self, pin):
        return GPIO.input(pin)

    def tooglePinValue(self, pin):
        value = not GPIO.input(pin)
        print "Setting pin",[pin], "value", [value]
        GPIO.output(pin, value) 
        return GPIO.input(pin)

    def setPinValue(self, pin, value):
        value = (GPIO.LOW,GPIO.HIGH)[value == 'high']
        print "Setting pin",[pin], "value", [value]
        GPIO.output(pin, value)
        return GPIO.input(pin)

    def getInfo(self):
        return { 'card': {
                          'io'      : self._io     ,
                          'gnd'     : self._gnd    , 
                          'vcc5_0v' : self._vcc5_0v,
                          'vcc3_3v' : self._vcc3_3v,
                          'dnc'     : self._dnc    ,
                          'name'    : self._name   
                          }
                }

# 5v   5v GN 14 15 18 GN 23   24 GN 25 08 07 DC GN 12 GN 16 20 21
#-----------------------------------------------------------------#
# 2    4  6  8  10 12 14 16   18 20 22 24 26 28 30 32 34 36 38 40 #
# 1    3  5  7  9  11 13 15   17 19 21 23 25 27 29 31 33 35 37 39 #
#-----------------------------------------------------------------#
# 3.3v 02 03 04 GN 17 27 22 3.3v 10 09 11 GN DC 05 06 13 19 26 GN
class Zero_w(Model):
    def __init__(self):
        Model.__init__(self,
		       io      = [8,3,5,7,10,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37,38,40],
                       gnd     = [6, 14, 20, 30, 34 , 9, 25, 39],
                       dnc     = [27, 28],
                       vcc5_0v = [2,4],
                       vcc3_3v = [1, 17],
                       name    = "Raspberry Pi Zero W Rev 1.1")

models = { 'Raspberry Pi Zero W Rev 1.1' : Zero_w()}
