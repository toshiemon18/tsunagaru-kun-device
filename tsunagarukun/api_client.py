#!/usr/bin/env python

import urllib
import urllib.request
import json

class APIClient:
    def __init__(self, url="http://localhost", port="3000"):
        self.url = self.build_baseurl(url, port)

    def get_request(self, endpoint, data, header):
        pass

    def post request(self, endpoint, data, header):
        request = urllib.request.Request(url, json(data).encode(), header)
        with urllib.request.urlopen(request) as response:
            body = response.read()

    def _build_baseurl(self, url, port):
        """
        APIのベースURLを構築する
        """
        url = "{}:{}".format(url, port)
        return url
