#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @author: zxp
# @date: 2019/09/19


import time, os, xlwt, xlrd
from xlutils.copy import copy

workpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '\\'


def now_time():
    '''
    获取当前时间
    '''
    return time.strftime("%m_%d_%H_%M_%S", time.localtime())


def report_file(data):
    log_file = workpath + "result\\" + now_time() + ".log"
    try:
        with open(log_file, 'a')as f:
            f.write(str(data).encode('utf-8'))
    except Exception:
        with open(log_file, 'ab')as f:
            f.write(str(data).encode('utf-8'))

def createexcel():
    filename = xlwt.Workbook()
    sheet = filename.add_sheet("测试数据")
    first_col = sheet.col(0)
    first_col.width = 600 * 20
    first_col = sheet.col(3)
    first_col.width = 1200 * 20
    first_col = sheet.col(2)
    first_col.width = 800 * 20
    sheet.write(0, 0, '用例名称')
    sheet.write(0, 1, '测试结果')
    sheet.write(0, 2, '请求参数')
    sheet.write(0, 3, 'body返回值')
    sheet.write(0, 4, 'header返回值')
    return filename ,sheet