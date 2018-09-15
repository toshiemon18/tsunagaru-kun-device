#!/usr/bin/env python

import time
import math
import sys
from Adafruit_ADS1x15 import ADS1015
import RPi.GPIO as GPIO

from tsunagarukun.constants import *


class Flipper:
    def __init__(self, interval):
        self.port = port
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.OUT)


    def flip(self):
        GPIO.output(self.port, (GPIO.input(self.port) + 1) % 2)

class BaseMonitor(object):
    def __init__(self, interval=1):
        self.interval = interval


    def busy_loop(self):
        pass


    def internal_loop(self):
        print(time.time() - self.start)


    def main_loop(self):
        self.start = int(time.time())
        prev = self.start
        while True:
            while time.time() - prev < self.interval:
                self.busy_loop()
            prev = int(time.time())
            self.internal_loop


class SensorMonitor(BaseMonitor):
    def __init__(self, interval):
        super().__init__(interval)
        self.flipper = Flipper(HEARTBEAT_GPIO)
        self.adc = ADS1015(address=ADS1015_I2C_BASE_ADDRESS, busnum=I2C_BUSNUM)
        selft.reset_vars()


    def reset_vars(self):
        self.sensor = 0
        self.samples = 0
        self.sample = 0
        self.sample_times = 0
        self.watt = 0


    def busy_loop(self):
        if self.sampels % CHANNEL_CHANGE_INTERVAL == 0:
            self.adc.start_adc(self.sensor,
                               gain=PGA_GAIN,
                               data_rate=SAMPLING_RATE)
            time.sleep(2.0/SAMPLING_RATE)

        current = self.adc.get_last_result() * CONVERSION_CONSTANT

        self.sample += current ** 2
        self.sample_times += 1
        if self.samples % FLIP_INTERVAL == 0:
            self.flipper.flip()
        self.samples += 1


    def internal_loop(self):
        if self.sample_times == 0:
            self.watt = 0
        else:
            self.watt = math.sqrt(self.sample / self.sample_times * VOLTAGE*TO_KILOWATT)
