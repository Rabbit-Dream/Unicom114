#-*- coding: utf-8 -*-

import requests
import time
import hashlib
import base64
#####################
import socket
import os
import sys
import wave
import numpy as np 
from datetime import datetime
from pyaudio import PyAudio,paInt16



class KdxfAPI(object):

    def __init__(self,filePath):

        self.URL = "http://openapi.xfyun.cn/v2/aiui"
        self.APPID = "5b17aa2c"
        self.API_KEY = "150ae1dfdb5649d0af9747b5d7d1a58c"
        self.AUE = "raw"
        self.AUTH_ID = "d4893d28232db580e52a21b391e4f993"
        self.DATA_TYPE = "audio"
        self.SAMPLE_RATE = "16000"
        self.SCENE = "main"
        self.RESULT_LEVEL = "plain"
        self.LAT = "39.938838"
        self.LNG = "116.368624"
        #个性化参数，需转义
        self.PERS_PARAM = "{\\\"auth_id\\\":\\\"d4893d28232db580e52a21b391e4f993\\\"}"
        self.FILE_PATH = filePath

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(('localhost', 10005))


    def buildHeader(self):
        curTime = str(int(time.time()))
        param = "{\"result_level\":\""+self.RESULT_LEVEL+"\",\"auth_id\":\""+self.AUTH_ID+"\",\"data_type\":\""+self.DATA_TYPE+"\",\"sample_rate\":\""+self.SAMPLE_RATE+"\",\"scene\":\""+self.SCENE+"\",\"lat\":\""+self.LAT+"\",\"lng\":\""+self.LNG+"\"}"
        #使用个性化参数时参数格式如下：
        #param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\",\"pers_param\":\""+PERS_PARAM+"\"}"
        paramBase64 = base64.b64encode(param.encode())
        w = self.API_KEY + curTime + paramBase64.decode()
        checkSum = hashlib.md5(w.encode('utf-8')).hexdigest()

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.APPID,
            'X-CheckSum': checkSum,
        }
        return header

    def readFile(self):
        binfile = open(self.FILE_PATH, 'rb')
        data = binfile.read()
        return data


    def fun(self):
        r = requests.post(self.URL, headers=self.buildHeader(), data=self.readFile())
        re = r.content.decode("utf-8")
        print(re)
        print(type(re))
        # 字符串转化为字典
        re = eval(re)
        ls = re['data']
        # print(type(ls))
        # print(len(ls))
        s = ""
        for l in ls:
            s = s + l['text']

        print(s, s.encode())
        print(len(s))   
        self.conn.send(s.encode())
        # with open('01.txt','w') as f:
        #     f.write(s)

xf = KdxfAPI("F:\\114文件\\录音分割结果\\新录音\\002wav\\8.wav")
xf.fun()