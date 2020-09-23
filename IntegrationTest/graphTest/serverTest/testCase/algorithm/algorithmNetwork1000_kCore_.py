#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/6/7'

"""
import sys
import os
import unittest
from filecmp import cmp
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData


class TestKCore(unittest.TestCase):
    """
    接口kcore：K-Core社区发现
    """

    @classmethod
    def setUpClass(cls):
        cls.alg = AlgInterface()
        cls.task = Task()
        cls.p = ProduceData()

        # 初始化数据
        cls.clear_data = cls.p.init_data("clear")
        cls.init_data = cls.p.init_data_network1000()

        # 预期结果
        cls.expect_result_no = {"kcores": []}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_kcore_01(self):
        """
        校验基本参数 + alpha=0.6, merged=true,label=knows
        :return:
        """
        body = {"direction": "BOTH", "k": 4, "degree": 3, "alpha":0.9, "merage": True, "label": "link"}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestKCore("test_kcore_001"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
