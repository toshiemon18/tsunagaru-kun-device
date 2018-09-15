#!/usr/bin/env python

import time
import math
import sys
from Adafruit_ADS1x15 import ADS1015
import RPi.GPIO as GPIO

class Flipper:
    def __init__(self, port):
        self.port = port
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.OUT)


    def flip(self):
        """
        GPIOの出力電位を変化させる
        呼ばれるたびにコンストラクタで指定したGPIO Portの出力をフリップする
        """
        GPIO.output(self.port, (GPIO.input(self.port)+1)%2))


class BaseMonitor(object):
    def __init__(self, interval=1):
        self.interval = interval


    def busy_loop(self):
        pass


    def internal_loop(self):
        print(time.time() - self.start)


    def main_loop(self):
        self.start = int(time.time())

