#!/usr/bin/env python

import urllib
from urllib.request import Request, urlopen
import json

class APIClient:
    def __init__(self, email, password):
        self.url = self._build_baseurl()
        status, _, headers = self.login(email, password)
        if status == 200:
            self.authenticate_data = {"access-token": headers["access-token"],
                                      "uid": headers["uid"],
                                      "client": headers["client"]}


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
        headers = self._build_headers()
        s, b, h = self._post_request("/v1/auth/sign_in", params, headers)
        return s, b, h


    def post_metrics(self, params):
        """
        センサーで計測した情報をつながるくんサーバーに送信する
        Args
            - params: 送信するメトリクスのdict
        Returns
            - status:  HTTP Status
            - body:    ボディ
            - headers: ヘッダー
        """
        headers = self._build_headers(**self.authenticate_data)
        s, b, h = self._post_request("/v1/metric")


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
        request = Request("{}{}".format(self.url, endpoint), headers=headers)
        try:
            with urlopen(request) as response:
                status = response.status
                body = json.load(response)
                headers = dict(response.headers)
                return status, body, headers
        except urllib.error.HTTPError as err:
            print("Detected 4xx or 5xx HTTP Status.")
            print(err.code())
            print(err.msg)
        except urllib.error.URLError as err:
            print("Failed HTTP communication.")
            print(err.code())
            print(err.msg)


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
                                         json.dumps(data).encode(), header)
        try:
            with urlopen(request) as response:
                status = response.status
                body = json.load(response)
                headers = dict(response.headers)
                return status, body, headers
        except urllib.error.HTTPError as err:
            print("Detected 4xx or 5xx HTTP Status.")
            print(err.code())
            print(err.msg)
        except urllib.error.URLError as err:
            print("Failed HTTP communication.")
            print(err.code())
            print(err.msg)


    def _build_baseurl(self):
        """
        APIのベースURLを構築する
        """
        import platform
        url_format = "http://{}:3000"
        if platform.system() == "Darwin":
            return url_format.format("localhost")
        else:
            return url_format.format("corazonMacBook-Pro.local")


    def _build_headers(self, **kargs):
        """
        HTTPヘッダー情報を構築する
        Args
            - **kargs: キーワード引数. よしなに投げろ
        Returns
            - headers: HTTPヘッダー情報をdictで返す
        """
        headers = {"Content-Type": "application/json"}
        if len(kargs) != 0:
            for key, val in kargs.items():
                headers[str(key)] = val
        return headers
