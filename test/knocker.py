#!/usr/bin/env python

import RPi.GPIO as GPIO

class Knocker:
    """このクラスは、GPIO の出力電圧を変化させます。
    flip() メソッドが呼ばれる毎に、指定の GPIO ピンの出力をフリップします。
    """

    def __init__(self, port):
        self.port = port
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port,GPIO.OUT)


    def flip(self):
        GPIO.output(self.port,(GPIO.input(self.port)+1)%2)
