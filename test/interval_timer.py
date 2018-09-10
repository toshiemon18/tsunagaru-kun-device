#!/usr/bin/env python

import time

class IntervalTimer(object):
    """このクラスは、全速力で busyloop() メソッドを実行します。
    また、コンストラクタで指定した秒毎に longloop() メソッドを実行します
    """

    def __init__(self, interval = 1):
        self.interval = interval

    def busyloop(self):
        pass

    def longloop(self):
        print time.time()-self.start

    def loop(self):
        self.start=int(time.time())
        prev=self.start
        while True:
            while time.time()-prev < self.interval:
                self.busyloop()
            prev = int(time.time())
            self.longloop()

