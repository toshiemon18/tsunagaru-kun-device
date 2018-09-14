#!/usr/bin/env python

import urllib
from urllib.request import Request, urlopen
import json

class APIClient:
    def __init__(self, url="http://localhost", port="3000"):
        self.url = self.build_baseurl(url, port)

    def login(self, email, password):
        """
        つながるくんサーバーにログインする
        Args
            - email: 登録したemail
            - password: パスワード
        Returns
            - status:  HTTP Status
            - body:    ボディ
            - headers  ヘッダー
        """
        params = {"email": email,
                  "password": password}
        headers = {"Content-Type": "application/json"}
        s, b, h = self._post_request("/v1/auth/sign_in", params, headers)
        return s, b, h


    def post_metrics(self, params, headers):
        """
        センサーで計測した情報をつながるくんサーバーに送信する
        Args
        Returns
            - status:  HTTP Status
            - body:    ボディ
            - headers: ヘッダー
        """
        pass


    # ===== Private functions
    def _get_request(self, endpoint, params, headers):
        """
        endpointに向けてGETリクエストを送信する
        Args
            - endpoint: リクエストの送信先エンドポイント
            - params:   リクエスト時に送信するパラメータ
            - headers:  リクエスト時に送信するヘッダー情報
        Returns
            - status:  HTTP Status
            - body:    HTTPレスポンスのボディ
            - headers: HTTPレスポンスのヘッダー
        """
        request = Request("{}{}".format(self.url, endpoint))
        with urlopen(request) as response:
            body = json.load(response)
            headers = dict(response.headers)
            return body, headers


    def _post_request(self, endpoint, data, header):
        """
        endpointに向けてPOSTリクエストを送信する
        Args
            - endpoint: リクエストの送信先エンドポイント
            - params:   リクエスト時に送信するパラメータ
            - headers:  リクエスト時に送信するヘッダー情報
        Returns
            - status:  HTTP Status
            - body: HTTPレスポンスのボディ
            - headers: HTTPレスポンスのヘッダー
        """
        request = Request("{}{}".format(self.url, endpoint),
                                         json(data).encode(), header)
        with urlopen(request) as response:
            body = json.load(response)
            headers = dict(response.headers)
            return body, headers


    def _build_baseurl(self, url, port):
        """
        APIのベースURLを構築する
        """
        url = "{}:{}".format(url, port)
        return url
