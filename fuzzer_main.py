# -*- coding: UTF-8 -*-
# @Time    : 2019/09/19
# @Author  : zxp

if __name__ == "__main__":
    import sys,os
    sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
    from data_analysis.data_processing import request_http
    request_http()

