#!/usr/bin/evn python
# -*- coding: UTF-8 -*-
# @Time    : 2019/09/18
# @Author  : zxp
import requests, random, os, sys, xlwt, json

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from config.baseconfig import default_data, report, n, assertdata
from fuzzer_method.fuzzer_method import dictdelkey, dictmodify, create_data, accesstype


def send(url, method, parame, headers, **args):
    if headers == {}:
        if method == 'POST':
            r = requests.post(url, json=parame, headers=headers, **args)
        if method == 'GET':
            r = requests.get(url, data=parame, headers=headers, **args)
        return [r.status_code, r.text, r.headers]
    else:
        if method == 'POST':
            if headers["Content-Type"] == "application/json":
                r = requests.post(url, json=parame, headers=headers, **args)
                return [r.status_code, r.text, r.headers]
            else:
                r = requests.post(url, data=parame, headers=headers, **args)
        if method == 'GET':
            r = requests.get(url, data=parame, headers=headers, **args)
        return [r.status_code, r.text, r.headers]


def sendformat(url, method, parame, headers):
    if headers["Content-Type"] == "application/json":
        if method == 'POST':
            r = requests.post(url, data=parame, headers=headers)
        if method == 'GET':
            r = requests.get(url, data=parame, headers=headers)
    else:
        if method == 'POST':
            r = requests.post(url, json=parame, headers=headers)
        if method == 'GET':
            r = requests.get(url, json=parame, headers=headers)
    return [r.status_code, r.text, r.headers]


def fuzztrigger(url, method, parame, headers, case, fuzzresult, sheet, *args):
    '''
    这边添加返回结果
    '''
    global n
    n += 1
    report = {}
    if args == ('case16format',):
        try:
            (code, body, header) = sendformat(url, method, parame, headers)
            report['case'] = case
            report['response body'] = body
            report['response header'] = header
        except Exception as e:
            print(e)
            if accesstype(default_data['json']) == accesstype(parame):
                report['except'] = str(e)
                report['result'] = 'FAIL'
    else:
        try:
            (code, body, header) = send(url, method, parame, headers)
            report['case'] = case
            report['response body'] = body
            report['response header'] = header
        except Exception as e:
            print(e)
            if accesstype(default_data['json']) == accesstype(parame):
                report['except'] = str(e)
                report['result'] = 'FAIL'
    # if 'code' in report['response body']:
    #     try:
    #         if accesstype(default_data['json']) == accesstype(parame):
    #             if assertdata['code'] == report['response body']['code']:
    #                 sheet.write(n, 1, 'succeed')
    #             else:
    #                 sheet.write(n, 1, 'failed')
    #         elif accesstype(default_data['json']) != accesstype(parame):
    #             if assertdata['code'] == report['response body']['code']:
    #                 sheet.write(n, 1, 'failed')
    #             else:
    #                 sheet.write(n, 1, 'succeed')
    #         else:
    #             sheet.write(n, 1, 'failed')
    #     except Exception as e:
    #         report['except'] = str(e)
    #         report['result'] = 'FAIL'
    #         sheet.write(n, 1, 'succeed')
    # elif 'code' in report['response header']:
    #     try:
    #         if accesstype(default_data['json']) == accesstype(parame):
    #             if assertdata['code'] == report['response header']['code']:
    #                 sheet.write(n, 1, 'succeed')
    #             else:
    #                 sheet.write(n, 1, 'failed')
    #         elif accesstype(default_data['json']) != accesstype(parame):
    #             if assertdata['code'] == report['response header']['code']:
    #                 sheet.write(n, 1, 'failed')
    #             else:
    #                 sheet.write(n, 1, 'succeed')
    #         else:
    #             sheet.write(n, 1, 'failed')
    #     except Exception as e:
    #         report['except'] = str(e)
    #         report['result'] = 'FAIL'
    #         sheet.write(n, 1, 'succeed')
    # else:
    #     try:
    #         if accesstype(default_data['json']) == accesstype(parame):
    #             if assertdata['code'] == report['response header']['code']:
    #                 sheet.write(n, 1, 'succeed')
    #             else:
    #                 sheet.write(n, 1, 'failed')
    #         elif accesstype(default_data['json']) != accesstype(parame):
    #             if assertdata['code'] == report['response header']['code']:
    #                 sheet.write(n, 1, 'failed')
    #             else:
    #                 sheet.write(n, 1, 'succeed')
    #         else:
    #             sheet.write(n, 1, 'failed')
    #     except Exception as e:
    #         report['except'] = str(e)
    #         report['result'] = 'FAIL'
    #         sheet.write(n, 1, 'succeed')
    sheet.write(n, 0, case + str(args) + ':' + url)
    sheet.write(n, 2, str(parame))
    try:
        sheet.write(n, 3, str(report['response body']))
    except Exception:
        sheet.write(n, 3, '返回值为空')
    try:
        sheet.write(n, 4, str(report['response header']))
    except Exception as e:
        sheet.write(n, 4, '返回值为空')
    fuzzresult[case + str(args) + ':' + url] = report


def case1raw(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    正常请求
    '''
    fuzztrigger(url, method, parame, headers, case, fuzzresult, sheet)


def case2noheader(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    null header
    '''
    if headers != {}:
        fuzztrigger(url, method, parame, {}, case, fuzzresult, sheet)
    else:
        return


def case3nocookies(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    null cookies
    '''
    for i in headers:
        if 'Cookie' in i:
            headers['Cookie'] = ''
            fuzztrigger(url, method, parame, headers, case, fuzzresult, sheet)
    else:
        return


def case4errorcookies(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    error cookies
    '''
    for i in headers:
        if 'Cookie' in i:
            headers['Cookie'] = '__error='
            fuzztrigger(url, method, parame, headers, case, fuzzresult, sheet)
    else:
        return


def case5noparams(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    NUll body
    '''
    if method == 'POST':
        fuzztrigger(url, method, {}, headers, case, fuzzresult, sheet)
    else:
        return


def case6lackparams(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    参数键遍历删除上传
    '''
    for k, v in parame.items():
        fuzztrigger(url, method, dictdelkey(parame, k), headers, case, fuzzresult, sheet, k)


def case7moreparams(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    添加无效参数
    '''
    parame['test'] = 'error'
    fuzztrigger(url, method, parame, headers, case, fuzzresult, sheet)
    del parame['test']


def case8blankvalue(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    空的参数值
    '''
    for k, v in parame.items():
        fuzztrigger(url, method, dictmodify(parame, k, None), headers, case, fuzzresult, sheet, k)


def case9valueintmultin(url, method, parame, headers, case, fuzzresult, sheet):
    '''
    修改value的int值
    '''
    for k, v in parame.items():
        n = random.randint(2, 101)
        if isinstance(v, int):
            fuzztrigger(url, method, dictmodify(parame, k, v * n), headers, case,
                        fuzzresult, sheet, k)
        else:
            continue


def case10valueintdivn(url, method, parame, headers, case, fuzzresult, sheet):
    '''int 转换成float'''
    for k, v in parame.items():
        n = random.random()
        if isinstance(v, int):
            fuzztrigger(url, method, dictmodify(parame, k, v * n), headers, case, fuzzresult, sheet, k)
        else:
            continue


def case11valuestr(url, method, parame, headers, case, fuzzresult, sheet):
    '''int转换成str'''
    for k, v in parame.items():
        if isinstance(v, int):
            fuzztrigger(url, method, dictmodify(parame, k, str(v)), headers, case, fuzzresult, sheet, k)
        else:
            continue


def case12valuestrextend(url, method, parame, headers, case, fuzzresult, sheet):
    '''修改str值'''
    for k, v in parame.items():
        v1 = ''
        if isinstance(v, str):
            for i in range(0, random.randint(2, 9)): v1 += v
            fuzztrigger(url, method, dictmodify(parame, k, v1), headers, case, fuzzresult, sheet, k)
        else:
            continue


def case13valuestrillega(url, method, parame, headers, case, fuzzresult, sheet):
    '''str 添加特殊符号 '''
    for k, v in parame.items():
        v1 = ',*&#%()=][@$&~`?.+-'
        if isinstance(v, str):
            v1 = v + v1[random.randint(1, 8) - 1] + v + v1[random.randint(1, 8) - 1] + v
            fuzztrigger(url, method, dictmodify(parame, k, v1), headers, case, fuzzresult, sheet, k)
        else:
            continue


def case15valuebase64(url, method, parame, headers, case, fuzzresult, sheet):
    '''blns.base64'''
    create_data(fuzztrigger, url, method, parame, headers, case, fuzzresult, sheet)


def case16format(url, method, parame, headers, case, fuzzresult, sheet):
    '''json&Text'''
    k = "case16format"
    fuzztrigger(url, method, parame, headers, case, fuzzresult, sheet, k)
