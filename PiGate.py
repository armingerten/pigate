# Before running:
# git clone https://github.com/adafruit/Adafruit_Python_DHT.git
# git clone git://github.com/kennethreitz/requests.git
# sudo python setup.py install

import time
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
from IoTHub import IoTHub

class PiGate:
    def __init__(self):
        self.iothub = IoTHub("2ada2125-4067-4385-9a5a-f7c4427757e1", "https://connectivity.myaxoom.com", False)

    def run(self):
        self.iothub.activate("0123456789")

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.lastStateReadContact = -1
        self.lastStatePir = -1

        while True:
            self.iothub.heartbeat()

            self.observeDht(dht.DHT22, 6, "b38e7e44", "fe00895f")
            self.observeDht(dht.DHT11, 5, "46bb3fa8", "9a7dbbe2")
            self.observeReadContact(23, "9f5f3563")
            self.observePir(18, "ed9eb94c")
    
            time.sleep(2)

    def observeDht(self, dhtType, gpioPin, dsIdHumidity, dsIdTemperature):
        h,t = dht.read_retry(dhtType, gpioPin)
        self.iothub.observe(dsIdHumidity, h)
        self.iothub.observe(dsIdTemperature, t)

    def observeReadContact(self, gpioPin, dsIdContact):
        m = GPIO.input(gpioPin)
        if (m != self.lastStateReadContact):
            self.iothub.observe(dsIdContact, 'Open' if m else 'Closed')
            self.lastStateReadContact = m

    def observePir(self, gpioPin, dsIdPir):
        p = GPIO.input(gpioPin)
        if (p != self.lastStatePir):
            self.iothub.observe(dsIdPir, 'Motion' if p else 'No motion')
            self.lastStatePir = p
