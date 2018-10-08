#!/usr/bin/env python

import urllib
from urllib.request import Request, urlopen
import json

class APIClient:
    def __init__(self, email, password, env="development"):
        self.url = self._build_baseurl(env)
        login_times = 0
        while True:
            status, _, headers = self.login(email, password)
            login_times += 1
            if status == 200:
                self.authenticate_data = {"token-type": headers["token-type"],
                                          "access-token": headers["access-token"],
                                          "uid": headers["uid"],
                                          "client": headers["client"]}
                break
            else:
                if login_times >= 100:
                    raise Exception("Cannot find {}".format(self.url))
                print("Failed sign up to {}".format(self.url))
                from time import sleep
                sleep(3)


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


    def post_device(self, name, category, image=""):
        """
        自身をつながるくんサーバーに登録する
        API Parameters
            - name: デバイス名
            - category: 接続する機器のカテゴリ
            - iamge: サムネイル (Not implement)
        Args
            - name: デバイス名. ex) 1F洗濯機
            - category: 接続する機器のカテゴリ
            - image: デバイスのサムネイル (Not implement)
        Returns
            - status: HTTP Status
            - body:   レスポンスbody
            - headers: レスポンスheader
        """
        headers = self._build_headers(**self.authenticate_data)
        params = {"name": name,
                  "category": category,
                  "image": image}
        s, b, h = self._post_request("/v1/devices", params, headers)
        return s, b, h


    def post_metrics(self, electric_current, watt, device_id):
        """
        センサーで計測した情報をつながるくんサーバーに送信する
        API Parameters
            - electric_current: 電流値
            - watt: 電力
            - device_id: 本デバイスのID
        Args
            - params: 送信するメトリクス(上記API Parameters)のdict
        Returns
            - status:  HTTP Status
            - body:    ボディ
            - headers: ヘッダー
        """
        headers = self._build_headers(**self.authenticate_data)
        s, b, h = self._post_request("/v1/metrics", params, headers)
        return s, b, h


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
            print(err)
        except urllib.error.URLError as err:
            print("Failed HTTP communication.")
            print(err)


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
            print(err)
        except urllib.error.URLError as err:
            print("Failed HTTP communication.")
            print(err)


    def _build_baseurl(self, env):
        """
        APIのベースURLを構築する
        Args
            - env: 環境 (development, production)
        Returns
            プラットフォームに依存して変化
            - Darwin(macOS): http://localhost:3000
            - Others:
                - development: http://st-pro.local
                - production:  http://corazonMacBook-Pro.local
        """
        import platform
        url_format = "http://{}:3000"
        if platform.system() == "Darwin":
            return url_format.format("localhost")
        else:
            if env == "development":
                return url_format.format("st-pro.local")
            elif env == "production":
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
