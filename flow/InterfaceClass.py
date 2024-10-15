#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author   : chuanwen.peng
# @Time     : 2022/9/9 14:30
# @File     : InterfaceClass.py
# @Project  : XR_face_Tools
"""
import pprint

import requests
import json
import urllib3

from requests_toolbelt.multipart.encoder import MultipartEncoder

urllib3.disable_warnings()


class XJSDFace:
    def __init__(self):
        self.base_url = "https://xr-face-fat.xjsdtech.com/"

    def detail_face_set(self, face_set_id):
        url = self.base_url + "/faceset/detail"

        payload = json.dumps({
            "faceSetId": face_set_id
        })
        headers = {
            'Connection': 'close',
            'faceSetDetailRequest': 'true',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        pprint.pprint(response.json())
        assert response.json().get("data").get("name"), response.json().get("data").get("faceTokenList")
        return response.json().get("data").get("faceTokenList")

    def add_face_set(self, name, description=""):
        url = self.base_url + "/faceset/add"

        payload = json.dumps({
            "description": description,
            "name": name
        })
        headers = {
            'Connection': 'close',
            'faceSetAddRequest': 'true',
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        response = session.post(url, headers=headers, data=payload, timeout=30)
        # session.request("POST", url, headers=headers, data=payload, timeout=3, verify=False)
        # try:
        #     response = requests.request("POST", url, headers=headers, data=payload, timeout=3, verify=False)
        # except:
        #     print(111)
        # print(response.text)
        face_id = int(response.json().get("data").get("id"))
        return face_id

    def add_face(self, face_set_id, face_tokens):
        url = self.base_url + "/face/add"

        payload = json.dumps({
            "description": "",
            "faceSetId": int(face_set_id),
            "faceTokens": face_tokens
        })
        headers = {
            'Connection': 'close',
            'faceAddRequest': 'true',
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        response = session.post(url, headers=headers, data=payload, timeout=30)

        return response.json()

    def detect_face(self, file_name=r'D:\\workspace\pythonStudy\\face\\image\\1.jpeg'):
        url = self.base_url + "/face/detect"

        # file_name = r'D:\\workspace\pythonStudy\\face\\image\\1.jpeg' if not file_name else file_name
        payload = {}
        files = [
            ('file', (file_name.split("\\")[-1], open(file_name, 'rb'), 'image/jpeg'))
        ]
        headers = {
            'Connection': 'close',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        response = session.post(url, headers=headers, data=payload, timeout=30, files=files)

        # print(response.text)
        # if response.json().get("data") is not None:
        #     face_token = response.json().get("data").get("faceToken")
        # else:
        #     face_token = False
        # return face_token
        if response.status_code == 200:
            return response.json()

    def search_face(self, face_set_id, file_name):
        url = self.base_url + "/face/search"

        # file_name = r'D:\\workspace\pythonStudy\\face\\image\\1.jpeg'
        payload = {'faceSetId': int(face_set_id)}
        files = [
            ('file', (file_name.split("\\")[-1], open(file_name, 'rb'), 'image/jpeg'))
        ]
        headers = {
            'Connection': 'close',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        session.keep_alive = False
        response = session.post(url, headers=headers, data=payload, timeout=50, files=files)
        # response = requests.post(url, headers=headers, data=payload, timeout=5, files=files, verify=False)

        if response.json().get("code") == 101014:
            result, token = 0, 0
        else:
            result = response.json().get("data").get("result")
            token = response.json().get("data").get("faceToken")

        return result, token

    def delete_face(self, face_set_id, face_tokens):
        url = self.base_url + "/face/delete"

        payload = json.dumps({
            "faceSetId": face_set_id,
            "faceTokens": face_tokens
        })
        headers = {
            'Connection': 'close',
            'faceDeleteRequest': 'true',
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        response = session.post(url, headers=headers, data=payload, timeout=30)

        assert response.json().get("msg") == "success"


class KShiFace:
    def __init__(self):
        self.base_url = "https://api-cn.faceplusplus.com/facepp/v3/"

    def detail_face_set(self, face_set_token):
        url = self.base_url + "faceset/getdetail"

        payload = MultipartEncoder(
            {
                "api_key": "kfAxKV3FYvXw8NZdBvpdYrK3PCSstjPi",
                "api_secret": "65_ssP7ljA9Da1siFE8xlMluGC-olQTh",
                "faceset_token": face_set_token,
                "start": '1900'
            }
        )
        headers = {
            'Connection': 'close',
            'faceSetAddRequest': 'true',
            'Content-Type': payload.content_type,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            face_tokens = response.json().get("face_tokens")
        else:
            face_tokens = []
        return face_tokens

    def add_face_set(self, face_set_id):
        url = self.base_url + "faceset/create"

        payload = MultipartEncoder(
            {
                "api_key": "kfAxKV3FYvXw8NZdBvpdYrK3PCSstjPi",
                "api_secret": "65_ssP7ljA9Da1siFE8xlMluGC-olQTh",
                "outer_id": face_set_id,
            }
        )
        headers = {
            'Connection': 'close',
            'faceSetAddRequest': 'true',
            'Content-Type': payload.content_type,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        response = session.post(url, headers=headers, data=payload, timeout=30)
        if response.status_code == 200:
            face_set_token = response.json().get("faceset_token")
        else:
            face_set_token = ''
        return face_set_token

    def add_face(self, faceset_token, face_tokens):
        url = self.base_url + "faceset/addface"

        payload = MultipartEncoder(
            {
                "api_key": "kfAxKV3FYvXw8NZdBvpdYrK3PCSstjPi",
                "api_secret": "65_ssP7ljA9Da1siFE8xlMluGC-olQTh",
                "faceset_token": faceset_token,
                "face_tokens": face_tokens
            }
        )
        headers = {
            'Connection': 'close',
            'faceSetAddRequest': 'true',
            'Content-Type': payload.content_type,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        response = session.post(url, headers=headers, data=payload, timeout=30)

        if response.status_code == 200:
            if response.json().get("face_added") != 0:
                face_add_count = response.json().get("faceset_token")
            else:
                face_add_count = 0
        else:
            face_add_count = 0
        return response.json()

    def detect_face(self, file_name=r"D:\workspace\pythonStudy\face\data\img_search_pn_400\pn_0_001682.jpg"):
        url = self.base_url + "detect"

        files = [
            ('file', (file_name.split("\\")[-1], open(file_name, 'rb'), 'image/jpg'))
        ]
        payload = MultipartEncoder(
            # {
            #     "api_key": "kfAxKV3FYvXw8NZdBvpdYrK3PCSstjPi",
            #     "api_secret": "65_ssP7ljA9Da1siFE8xlMluGC-olQTh",
            #     "image_file": file_name
            # }
            fields={
                "api_key": "kfAxKV3FYvXw8NZdBvpdYrK3PCSstjPi",
                "api_secret": "65_ssP7ljA9Da1siFE8xlMluGC-olQTh",
                "image_file": ("pn_0_001682.jpg", open(file_name, 'rb'), "image/jpg")
            }
        )
        headers = {
            'Connection': 'close',
            'faceSetAddRequest': 'true',
            'Content-Type': payload.content_type,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        response = session.post(url, headers=headers, data=payload, timeout=30)

        # if response.status_code == 200:
        #     face_token_li = response.json().get("faces")
        #     if face_token_li:
        #         face_token = face_token_li[0].get("face_token")
        #     else:
        #         face_token = ''
        # else:
        #     face_token = ''
        # return face_token
        if response.status_code == 200:
            return response.json()

    def search_face(self, face_set_token, file_name):
        url = self.base_url + "search"

        payload = MultipartEncoder(
            # {
            #     "api_key": "kfAxKV3FYvXw8NZdBvpdYrK3PCSstjPi",
            #     "api_secret": "65_ssP7ljA9Da1siFE8xlMluGC-olQTh",
            #     "image_file": file_name
            # }
            fields={
                "api_key": "kfAxKV3FYvXw8NZdBvpdYrK3PCSstjPi",
                "api_secret": "65_ssP7ljA9Da1siFE8xlMluGC-olQTh",
                "faceset_token": face_set_token,
                "image_file": ("pn_0_001682.jpg", open(file_name, 'rb'), "image/jpg")
            }
        )
        headers = {
            'Connection': 'close',
            'faceSetAddRequest': 'true',
            'Content-Type': payload.content_type,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        session = requests.session()
        session.keep_alive = False
        response = session.post(url, headers=headers, data=payload, timeout=30)

        if response.status_code == 200:
            if response.json().get("results"):
                face_confidence = response.json().get("results")[0].get("confidence")
                face_token = response.json().get("results")[0].get("face_token")
            else:
                face_confidence = 0
                face_token = ''
        else:
            face_confidence = 0
            face_token = ''
        return face_confidence, face_token
