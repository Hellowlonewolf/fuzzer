#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @author: zxp
# @date: 2019/09/18

import os,sys,time

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from work.case_report import report_file,createexcel
from work.fuzz_work import *
from fuzzer_method.fuzzer_method import extractiondata
from config.baseconfig import *

workpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '\\'
def request_http():
    fuzzresult = {}
    filename,sheet=createexcel()
    extractiondata()
    testcases = ['case1raw', 'case2noheader', 'case3nocookies', 'case4errorcookies', 'case5noparams',
                 'case6lackparams', 'case7moreparams', 'case8blankvalue'
        , 'case9valueintmultin', 'case10valueintdivn', 'case11valuestr', 'case12valuestrextend',
                 'case13valuestrillega','case16format','case15valuebase64']


    for case in testcases:
        eval(case)(default_data['url'], default_data['method'], default_data['json'],
                   default_data['headers'], case, fuzzresult,sheet)
    report_file(fuzzresult)
    filename.save(workpath + 'result\\report' + time.strftime("%m_%d_%H_%M_%S", time.localtime()) + '.xls')

