#!/usr/bin/evn python
# -*- coding: UTF-8 -*-
# @Time    : 2019/09/18
# @Author  : zxp
import os, sys,json

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from config.baseconfig import *
workpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '\\'
datafile=workpath+"config"

def create_data(execute, url, method, parame, headers, case, fuzzresult,sheet):
    for i, j, k in os.walk(datafile):
        for i in k:
            if '.py' not in i:
                with open(workpath + "config\\" + i + "", 'r', encoding='UTF-8') as f:
                    content = f.readlines()
                    for k, v in parame.items():
                        content = [x.strip('\n').strip(',') for x in content if
                                   x and not x.startswith('[') and not x.startswith(']')]
                        for i in content:
                            execute(url, method, dictfiltration(parame, k, i), headers, case, fuzzresult, sheet,k + i)



def dictdelkey(dict, key):
    '''
    键
    '''
    tmp = dict.copy()
    del tmp[key]
    return tmp


def dictmodify(dict, key, value):
    '''
    值
    '''
    tmp = dict.copy()
    tmp[key] = value
    return tmp


def dictfiltration(dict, key, value):
    tmp = dict.copy()
    tmp[key] = value.strip().replace("\"", "").replace("\\\\","\\")
    return tmp


def dicttostr(dict, sp='&', op='='):
    str1 = ''
    for k, v in dict.items():
        str1 = str1 + k + op + str(v) + sp
    return str1[0:-1]


def strtodict(str, sp='&', op='='):
    dict = {}
    try:
        list = str.split(sp)
    except ValueError:
        return dict
    for i in list:
        try:
            k, v = i.split(op)
            dict[k] = v
        except ValueError:
            break
    return dict


def delinstruct(path):
    if switch == True:
        del_har = 'del /F /S /Q  ' + path + ''
        os.system(del_har)
    else:
        return



def accesstype(data):
    typedata = {}
    for k, v in data.items():
        typedata[k] = type(v)
    return typedata


def verification():
    '''验证结果'''
    return


def har_data(path):
    try:
        if not os.path.exists(path):
            print("api record file not exist, exit test!")
            exit()
        else:
            os.system('har2case ' + path + '')

    except Exception as e:
        print(e)
        print("api record file open error, exit!")
        exit()

def extractiondata():
    workpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '\\'
    harfile = workpath + "api\\test.har"
    json_file = workpath + "api\\test.json"
    exists = os.path.exists(json_file)
    if exists:
        pass
    else:
        har_data(harfile)
    with open(json_file, encoding='utf-8') as t:
        data = json.loads(t.read())
        # 判断请求次数 并执行
        for i in range(1, len(data)):
            if 'test' in data[i]:
                default_data['url'] = data[i]['test']['request']['url']
                default_data['method'] = data[i]['test']['request']['method']
                default_data['headers'] = data[i]['test']['request']['headers']
                default_data['json'] = data[i]['test']['request']['json']
    delinstruct(harfile)



