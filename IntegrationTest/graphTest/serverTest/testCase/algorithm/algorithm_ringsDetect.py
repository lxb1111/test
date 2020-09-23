#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/5/18'

"""

import sys
import os
import unittest
import importlib
from filecmp import cmp

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData

TYPE = "hongloumeng"


class TestRingsDetect(unittest.TestCase):
    """
    接口rings_detect：环路检测
    """

    @classmethod
    def setUpClass(cls):
        cls.alg = AlgInterface()
        cls.task = Task()
        cls.p = ProduceData()

        # 初始化图
        cls.clear_data = cls.p.init_data("clear")
        cls.init_data = cls.p.init_data_hongloumeng()

        # 预期结果
        cls.expect_result_depth = {"rings": [["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"],
                                              ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"],
                                              ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                              ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                              ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                              ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"]]}
        cls.expect_result_direction = {"rings": [["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"],
                                                  ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"],
                                                  ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                                  ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                                  ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                                  ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                                  ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                                  ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                                  ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                                  ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"]]}
        cls.expect_result_direction2 = {"rings": []}
        cls.expect_result_degree = {"rings": [["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"],
                                               ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"], ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                               ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                               ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                               ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                               ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                               ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                               ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                               ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"]]}
        cls.expect_result_degree2 = {"rings": [["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                                ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                                ["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"], ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"],
                                                ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                                ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                                ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                                ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                                ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                                ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"]]}
        cls.expect_result_capacity = {"rings": [["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"], ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"],
                                                 ["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                                 ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                                 ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                                 ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                                 ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                                 ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                                 ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                                 ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"]]}
        cls.expect_result_limit = {"rings": [["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"], ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"],
                                              ["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"],
                                              ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                              ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                              ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                              ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"]]}
        cls.expect_result_3 = {"rings": [["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                          ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                          ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                          ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                          ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                          ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                          ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                          ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"], ["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"],
                                          ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"]]}
        cls.expect_result_3limit = {"rings": [["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"], ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                               ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"],
                                               ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                               ["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"]]}
        cls.expect_result_label = {"rings": []}
        cls.expect_result_workers = {"rings": [["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"],
                                                ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"],
                                                ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"],
                                                ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                                ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                                ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                                ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                                ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                                ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                                ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"]]}
        cls.expect_result_3workers = {"rings": [["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"],
                                                 ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"], ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                                 ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                                 ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                                 ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                                 ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                                 ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                                 ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"],
                                                 ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"]]}
        cls.expect_result_count = {"rings": [["1:贾兰", "2:李纨", "1:贾珠", "1:贾兰"], ["1:贾琏", "2:秋桐", "1:贾赦", "1:贾琏"],
                                              ["1:贾琏", "2:平儿", "2:王熙凤", "1:贾琏"], ["1:林如海", "2:林黛玉", "2:贾敏", "1:林如海"],
                                              ["1:贾代善", "1:贾赦", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "1:贾赦", "1:贾代善"],
                                              ["1:贾代善", "1:贾赦", "2:贾母", "2:贾敏", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"],
                                              ["1:贾代善", "2:贾母", "2:贾敏", "1:贾代善"],
                                              ["1:贾宝玉", "2:王夫人", "2:薛姨妈", "2:薛宝钗", "1:贾宝玉"]]}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_rings_detect_01(self):
        """
        param = [depth]
        :return:
        """
        body = {"depth": 5}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_depth["rings"],
                          msg="%s check not pass" % result["rings"][i])
        self.assertEqual(cmp(result, self.expect_result_depth), 0, msg="result check not pass")

    def test_rings_detect_02(self):
        """
        param = [depth, source_label]
        :return:
        """
        body = {"depth": 5, "source_label": "男人"}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_depth["rings"],
                          msg="%s check not pass" % result["rings"][i])
        # self.assertEqual(cmp(result, self.expect_result_depth), 0, msg="result check not pass")

    def test_rings_detect_03(self):
        """
        param = [depth, direction]
        :return:
        """
        body = {"depth": 5, "direction": "BOTH"}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_direction["rings"],
                          msg="%s check not pass" % result["rings"][i])
        # self.assertEqual(cmp(result, self.expect_result_direction), 0, msg="result check not pass")

    def test_rings_detect_04(self):
        """
        param = [depth, direction]
        :return:
        """
        body = {"depth": 5, "direction": "IN"}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_direction2), 0, msg="result check not pass")

    def test_rings_detect_05(self):
        """
        param = [depth, direction]
        :return:
        """
        body = {"depth": 5, "direction": "OUT"}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_direction2), 0, msg="result check not pass")

    def test_rings_detect_06(self):
        """
        param = [depth, label]
        :return:
        """
        body = {"depth": 5, "label": "妻"}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_direction2), 0, msg="result check not pass")

    def test_rings_detect_07(self):
        """
        param = [depth, degree]
        :return:
        """
        body = {"depth": 5, "degree": 5}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_degree), 0, msg="result check not pass")
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_degree["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_08(self):
        """
        param = [depth, capacity]
        :return:
        """
        body = {"depth": 5, "capacity": 50}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_capacity), 0, msg="result check not pass")
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_capacity["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_09(self):
        """
        param = [depth, limit]
        :return:
        """
        body = {"depth": 5, "limit": -1}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_limit), 0, msg="result check not pass")
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_limit["rings"],
                          msg="%s check not pass" % result["rings"][i])

    # @unittest.skip("skip")
    def test_rings_detect_10(self):
        """
        param = [depth, direction, degree]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_3), 0)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_3["rings"],
                          msg="%s check not pass" % result["rings"][i])

    # @unittest.skip("skip")
    def test_rings_detect_11(self):
        """
        param = [depth, direction, degree, limit]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50, "limit": -1}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_3limit["rings"],
                          msg="%s check not pass" % result["rings"][i])

    # @unittest.skip("skip")
    def test_rings_detect_12(self):
        """
        param = [depth, direction, degree, limit, label]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50, "limit": -1, "label": "妻"}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_3limit["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_13(self):
        """
        param = [depth, direction, degree, limit, label, capacity]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50, "limit": -1, "label": "妻", "capacity": 50}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_3limit["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_14(self):
        """
        param = [depth, workers]
        :return:
        """
        body = {"depth": 5, "workers": -1}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_workers["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_15(self):
        """
        param = [depth, workers]
        :return:
        """
        body = {"depth": 5, "workers": 0}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_workers["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_16(self):
        """
        :return:
        """
        body = {"depth": 5, "workers": 100}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_workers["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_17(self):
        """
        param = [depth, direction, degree, workers]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50, "workers": 0}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_3workers["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_18(self):
        """
        param = [depth, count_only, workers]
        :return:
        """
        body = {"depth": 5, "count_only": True, "workers": 0}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(result["rings_count"], 11, msg="result check not pass")

    def test_rings_detect_19(self):
        """
        param = [depth, count_only, workers]
        :return:
        """
        body = {"depth": 5, "count_only": False, "workers": 0}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        for i in range(len(result["rings"])):
            self.assertIn(result["rings"][i], self.expect_result_count["rings"],
                          msg="%s check not pass" % result["rings"][i])

    def test_rings_detect_20(self):
        """
        param = [depth, count_only, workers]
        :return:
        """
        body = {"depth": 5, "count_only": True, "workers": 10}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(result["rings_count"], 11, msg="result check not pass")


if __name__ == '__main__':
    # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestRingsDetect("test_rings_detect_01"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
