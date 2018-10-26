#!/usr/bin/env python

import time
import math
import sys
from Adafruit_ADS1x15 import ADS1015
import RPi.GPIO as GPIO
import numpy as np

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
        self.sample_list = []
        self.sampling_times = 0
        self.watt_rms = 0
        self.current_rms = 0


    def busy_loop(self):
        current = self.convert_adcval_to_current(self.adc.read_adc(0, gain=PGA_GAIN))
        self.sample_list.append(current)
        self.sampling_times += 1


    def internal_loop(self):
        if self.sampling_times == 0:
            self.reset_vars()
        else:
            self.current_rms = self.rms(self.sample_list)
            self.watt_rms = self.current_rms * VOLTAGE


    def main_loop(self):
        self.start = int(time.time())
        prev = self.start
        while True:
            self.reset_vars()
            while time.time() - prev < self.interval:
                if len(self.sample_list) <= SAMPLE_TIMES:
                    self.busy_loop()
            prev = int(time.time())
            self.internal_loop()
            yield {"electric_current": self.current_rms, "watt": self.watt_rms}


    def convert_adcval_to_current(self, adcval):
        Vmax = 2.048   # 測定可能な最大電圧 (ADS1015のGain2を選択)
        ValMax = 2048  # 引数の最大値
        return ((adcval / ValMax) * Vmax) / CONVERSION_CONSTANT

    def rms(self, num_list):
        powered_nums = np.power(num_list, 2)
        rms = np.sqrt(np.sum(powered_nums) / len(num_list))
        return rms
