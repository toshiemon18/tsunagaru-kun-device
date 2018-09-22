#!/usr/bin/env python

import time
import math
import sys
from Adafruit_ADS1x15 import ADS1015
import RPi.GPIO as GPIO

from tsunagarukun.constants import *

class BaseMonitor(object):
    def __init__(self, interval=1):
        self.interval = interval


    def busy_loop(self):
        pass


    def internal_loop(self):
        print(time.time() - self.start)


class SensorMonitor(BaseMonitor):
    def __init__(self, interval):
        super().__init__(interval)
        self.adc = ADS1015(address=ADS1015_I2C_BASE_ADDRESS, busnum=I2C_BUSNUM)
        self.reset_vars()


    def reset_vars(self):
        self.sensor = 0
        self.samples = 0
        self.sample = 0
        self.sampling_times = 0
        self.watt_rms = 0
        self.current_rms = 0


    def busy_loop(self):
        current = self.convert_adcval_to_current(adc.read_adc(0, gain=PGA_GAIN))

        self.sample += current ** 2
        self.sampling_times += 1
        if self.samples % FLIP_INTERVAL == 0:
            self.flipper.flip()
        self.samples += 1


    def internal_loop(self):
        if self.sampling_times == 0:
            self.watt_rms = 0
        else:
            self.watt_rms = math.sqrt(self.sample / float(self.sampling_times)) * VOLTAGE
            self.current_rms = math.sqrt(self.sample / float(self.sampling_times))


    def main_loop(self):
        self.start = int(time.time())
        prev = self.start
        while True:
            while time.time() - prev < self.interval:
                self.busy_loop()
            prev = int(time.time())
            self.internal_loop
            yield {"electric_current": self.current_rms, "watt": self.watt_rms}


    def convert_adcval_to_current(self, adcval):
        Vmax = 2.048   # 測定可能な最大電圧 (ADS1015のGain2を選択)
        ValMax = 2048  # 引数の最大値
        return (adcval / ValMax * Vmax) / CONVERSION_CONSTANT
