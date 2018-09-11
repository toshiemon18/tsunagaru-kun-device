#!/usr/bin/env python

from constants import *
import math
from collections import deque
import copy
import sys
import datetime
import bz2
import Adafruit_ADS1x15

from constants import *
from interval_timer import IntervalTimer
from knocker import Knocker

class Sampler(IntervalTimer):

    """このクラスは、メインクラスです。
    AD コンバーターの管理、データ送信、ハートビートの管理をします。
    """

    def __init__(self,interval):
        super(Sampler, self).__init__(interval)
        self.knocker = Knocker(HEARTBEAT_GPIO)
        # self.recorder = Recorder(UPLOAD_URL, BASICAUTH_ID, BASICAUTH_PASS, \
        #     MINIMUM_UPLOAD_QUEUE_LENGTH)
        self.adc = Adafruit_ADS1x15.ADS1015(\
            address=ADS1015_I2C_BASE_ADDRESS,busnum=I2C_BUSNUM)
        self.reset_valiables()


    def reset_valiables(self):
        self.sensor = 0
        self.samples = 0
        self.sample_buffer = [0]*SENSORS
        self.sample_length = [0]*SENSORS
        self.watt = [0]*SENSORS


    def busyloop(self):
        if self.samples%CHANNEL_CHANGE_INTERVAL == 0 :
            self.sensor=(self.samples/CHANNEL_CHANGE_INTERVAL)%SENSORS
            # self.adc.start_adc(self.sensor, gain=PGA_GAIN, data_rate=SAMPLING_RATE)
            time.sleep(2.0/SAMPLING_RATE)

        # current=self.adc.get_last_result()*CONVERSION_CONSTANT
        current = self.adc.read_adc(1, gain=2)

        self.sample_buffer[self.sensor] += current * current
        self.sample_length[self.sensor] += 1
        if self.samples%FLIP_INTERVAL == 0:
            self.knocker.flip()
        self.samples += 1


    def longloop(self):
        for self.sensor in range(SENSORS):
            if self.sample_length[self.sensor] == 0:
                self.watt[self.sensor]=0
            else:
                self.watt[self.sensor]=\
                    math.sqrt(self.sample_buffer[self.sensor]\
                    /self.sample_length[self.sensor])*VOLTAGE*TO_KILOWATT

        # self.recorder.record(self.watt)
        self.display_metrics()
        self.reset_valiables()

    def display_metrics(self):
        print("Watt power : {}".format(self.watt))

if __name__ == '__main__':
    sampler = Sampler(MEASURE_INTERVAL)
    sampler.loop()
