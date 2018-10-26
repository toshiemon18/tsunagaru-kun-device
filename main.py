#!/usr/bin/env python

import json
import time
from tsunagarukun.api_client import APIClient
from tsunagarukun.sensor_monitor import SensorMonitor
from tsunagarukun.constants import MEASURE_INTERVAL

class Main:
    def __init__(self):
        json_fp = open("./config.json")
        self.config = dict(json.load(json_fp))
        login_data = self.config["login"]
        login_data["env"] = "production"
        self.client = APIClient(**login_data)


    def main(self):
        sensor_monitor = SensorMonitor(MEASURE_INTERVAL)
        for metrics in sensor_monitor.main_loop():
            post_data = metrics
            post_data["device_id"] = self.config["device_id"]
            self.client.post_metrics(**post_data)


if __name__ == '__main__':
    Main().main()
