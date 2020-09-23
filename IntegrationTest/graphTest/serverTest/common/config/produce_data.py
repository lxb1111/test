#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/5/23'

"""
import sys
import os
import importlib

import IntegrationTest.graphTest.serverTest.common.gremlin_dataset as _cfg_data
import IntegrationTest.graphTest.serverTest.common.graph_config as _cfg

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)


from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.common.hugegraph_api.auth_api import Auths


class ProduceData(object):
    """
    通过接口制造数据，每个算法执行前，先制造数据；算法执行完成后，销毁数据
    """

    def __init__(self):
        """
        初始化
        """
        self.alg = AlgInterface()
        self.data_dict = _cfg_data.GRAPH_DATA
        self.auth = Auths()

    def produce_api(self, data):
        """
        gremlin命令
        """
        body = {
            "gremlin": data,
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % _cfg.GRAPH, "g": "__g_%s" % _cfg.GRAPH}
        }
        # 测试权限使用 Auths() 有密码需要设置
        # code, ret = self.alg.post_gremlin(body)
        code, ret = self.auth.post_gremlin(body)
        return code, ret["result"]

    def init_data(self, type):
        """
        取相应的数据，生成图
        :param type:
        :return:
        """
        type_keys = self.data_dict.keys()
        if type in type_keys:
            gremlin = self.data_dict[type]
            code, ret = self.produce_api(gremlin)
            return code, ret

    def init_data_hongloumeng(self):
        """
        读取文件，生成红楼梦图
        """
        url = os.path.dirname(os.path.realpath(__file__)) + "/data_hongloumeng"
        with open(url, "r") as f:
            for line in f:
                if line is not None:
                    data = line.strip('\n')
                    break
        code, ret = self.produce_api(data)
        return code, ret

    def init_data_network1000(self):
        """
        读取文件，生成network1000图
        """
        url = os.path.dirname(os.path.realpath(__file__)) + "/network_result2.txt"
        with open(url, "r") as f:
            for line in f:
                if line is not None:
                    data = line.strip('\n')
                    print (data)
                    code, ret = self.produce_api(data)


if __name__ == '__main__':

    graph = "hugegraph"
    body = {
        "gremlin": "",
        "bindings": {},
        "language": "gremlin-groovy",
        "aliases": {"graph": "%s" % graph, "g": "__g_%s" % graph}
    }
    print (body)