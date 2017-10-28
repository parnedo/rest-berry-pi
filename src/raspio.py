import RPi.GPIO as GPIO
class raspio:
    def __init__(self, setup):

        # 5v   5v GN 14 15 18 GN 23   24 GN 25 08 07 DC GN 12 GN 16 21 21
        #-----------------------------------------------------------------#
        # 2    4  6  8  10 12 14 16   18 20 22 24 26 28 30 32 34 36 38 40 #
        # 1    3  5  7  9  11 13 15   17 19 21 23 25 27 29 31 33 35 37 39 #
        #-----------------------------------------------------------------#
        # 3.3v 02 03 04 GN 17 27 22 3.3v 10 09 11 GN DC 05 06 13 19 26 GN

        self.mPins = {}
        self.mPins['pins'] = [8,10,12,16,18,22,24,26,32,36,38,40,37,35,33,31,29,23,21,19,15,13,11,7,5,3]
        self.mPins['ground'] = [6, 14, 20, 30, 34 , 9, 25, 39]
        self.mPins['DNC'] = [27, 28]

        # GPIO.BOARD || GPIO.BCM 
        self.mBoard = GPIO.BOARD 
        self.mSetup = setup

        self.setup()

    def setup(self):
        GPIO.setmode(self.mBoard)
        for item in self.mSetup.keys():
            pin = self.mSetup[item]['pin']
            es =  self.mSetup[item]['ES']
            if 'initial' in self.mSetup[item].keys():
                initial = self.mSetup[item]['initial']
                GPIO.setup(pin, es, initial=initial)
                print "Setting pin",pin, "ES", es, "initial", initial
            else:
                GPIO.setup(pin, es)
                print "Setting pin",pin, "ES", es 

    def setPin(self, item):
        pin = self.mSetup[item]['pin']
        GPIO.output(pin,GPIO.HIGH)
        return GPIO.input(pin)

    def unsetPin(self, item):
        pin = self.mSetup[item]['pin']
        GPIO.output(pin,GPIO.LOW)
        return GPIO.input(pin)

