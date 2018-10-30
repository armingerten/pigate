# If you are not using DHTs or GPIOs, remove dht/GPIO imports and all defs/references to oberserve* functions
import time
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
from IoTHub import IoTHub


class PiGate:

    gpioStates = dict()
    onlySendUpdateOnChange = False

    def __init__(self):
        self.iothub = IoTHub("{generate GUID for gateId}", "{customerId}.myaxoom.com", False)

    def run(self):
        GPIO.setmode(GPIO.BCM)

        self.waitForActivation()
        
        while True:
            try:
                self.iothub.heartbeat()

                #self.observeDht(dht.DHT22, 6, "b38e7e44", "fe00895f")
                #self.observeDht(dht.DHT11, 5, "46bb3fa8", "9a7dbbe2")
                #self.observeGPIO(22, "412523d0") # Window 1 reed contact
                #self.observeGPIO(26, "633d8df6")  # Window 2 reed contact
                #self.observeGPIO(25, "aca899ea")  # Window 3 reed contact
                #self.observeGPIO(23, "40c1c680")  # Window 4 reed contact
                #self.observeGPIO(18, "c5ca96bd")  # Motion sensor 1
                #self.observeGPIO(24, "abb5ca5c")  # Motion sensor 2

            except Exception as ex:
                print("Exception occurred!")
                print(ex)
    
            time.sleep(2)

    def waitForActivation(self):
        tokenStatus = 'AUTH_NOT_STARTED'
        while (tokenStatus != ''):
            tokenStatus = self.iothub.requestToken()
            
            if (tokenStatus == 'authorization_pending'):
                time.sleep(6)
            else:
                self.iothub.requestAuthorization()
            
    def observeDht(self, dhtType, gpioPin, dsIdHumidity, dsIdTemperature):
        h,t = dht.read_retry(dhtType, gpioPin)
        self.iothub.observe(dsIdHumidity, h)
        self.iothub.observe(dsIdTemperature, t)

    def observeGPIO(self, gpioPin, dsIdContact):
        # Setup GPIO if necessary
        if (not gpioPin in self.gpioStates):
            print("PiGate.SetupGPIO {}".format(gpioPin))
            GPIO.setup(gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.gpioStates[gpioPin] = -1

        # Read GPIO
        m = GPIO.input(gpioPin)
        self.gpioStates[gpioPin] = m

        # Skip sending if "onlySendUpdateOnChange" is activated and state did not change
        if (not (self.onlySendUpdateOnChange and m == self.gpioStates[gpioPin])):
            self.iothub.observe(dsIdContact, m)
