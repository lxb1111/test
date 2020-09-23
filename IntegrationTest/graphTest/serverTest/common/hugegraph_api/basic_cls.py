#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '19/10/09'

"""
from io import StringIO
import gzip
import requests.packages.urllib3.util.ssl_
import requests
import copy
import json
import logging as logger
import urllib
import sys
import os
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.config import graph_config as _cfg

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


class BasicClassMethod(object):
    """
    common classMethod
    """

    def __init__(self):
        self.host = _cfg.HOST
        self.port = _cfg.PORT
        self.graph = _cfg.GRAPH
        self.timeout = 120
        self.debug = False
        self.admin = _cfg.admin_password

    def to_url_params(self, params):
        """
        get请求 处理请求参数
        :param params: {a:1,b:2}
        :return: string -> a=1&b=2
        """
        if not params:
            return ""
        else:
            new_params = {}
            str_params = ''
            for k, v in params.items():
                if isinstance(v, list):
                    for v_item in v:
                        if isinstance(v_item):
                            str_params += '&%s[]=%s' % (k, v_item.encode('utf-8'))
                        elif isinstance(v_item, str):
                            str_params += '&%s[]=%s' % (k, v_item)
                        elif isinstance(v_item, int):
                            str_params += '&%s[]=%s' % (k, str(v_item))
                        elif v_item is None:
                            str_params += '&%s[]=%s' % (k, None)
                        else:
                            logger.log("Got an invalid params:(k: %s, v: %s)" % k, v_item)
                else:
                    if isinstance(v):
                        new_params[k] = v.encode('utf-8')
                    elif isinstance(v, str):
                        new_params[k] = v
                    elif isinstance(v, int):
                        new_params[k] = str(v)
                    elif v is None:
                        new_params[k] = None
                    else:
                        logger.log("Got an invalid params:(k: %s, v: %s)" % k, v)
            return urllib.urlencode(new_params) + str_params

    def request(self, method, path, params={}, body={}, user_id=None, headers={}, cookies={}):
        """
        :param method: request的请求方法
        :param path:  part_url
        :param params: 请求参数
        :param body:   请求body
        :param user_id:
        :param headers:
        :param cookies:
        :return:
        """
        # set header
        h = copy.deepcopy(headers)
        h['Content-Type'] = 'application/json'
        if user_id is not None:
            h['X-User-Id'] = user_id
        else:
            pass
        # set url
        url = "http://%s:%d" % (self.host, self.port) + path
        if params is not None:
            url += '?' + self.to_url_params(params)
        else:
            pass

        resp = requests.request(method, url, data=body,
                                headers=h, verify=False, timeout=self.timeout, cookies=cookies)
        # print ("--status_code: " + str(resp.status_code) + " -- content:" + resp.content)
        # deal result
        if resp.status_code == 201 or resp.status_code == 200:
            ret = json.loads(resp.content)
            return resp.status_code, ret
        else:
            try:
                ret = json.loads(resp.content)
                return resp.status_code, ret
            except:
                return resp.status_code, resp.content

    def gzip_decompress(self, data):
        """
        处理zip文件
        :param data:
        :return:
        """
        f = StringIO(data)
        gz = gzip.GzipFile(fileobj=f, mode='rb')
        return gz.read()


if __name__ == "__main__":
    cls_test = BasicClassMethod()
    print (cls_test.graph)
