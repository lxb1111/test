#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/5/14'

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


TYPE = "centrality"


class TestEigenvectorCentrality(unittest.TestCase):
    """
    接口eigenvector_centrality：特征中心性
    case1/2/3/5/20 结果需要调试
    """
    @classmethod
    def setUpClass(cls):
        cls.alg = AlgInterface()
        cls.task = Task()
        cls.p = ProduceData()

        # 初始化数据
        # cls.clrcode, cls.clrret = cls.p.init_data("clear")
        # cls.initcode, cls.initret = cls.p.init_data(TYPE)
        cls.clear_data = cls.p.init_data("clear")
        cls.init_data = cls.p.init_data(TYPE)

        # 预期结果
        cls.expect_result_01 = {"2:ripple": 4, "1:marko": 4, "1:peter": 4, "1:vadas": 3, "2:lop": 2, "1:josh": 1}
        cls.expect_result_02 = {"2:ripple": 4, "1:marko": 3, "2:lop": 3, "1:peter": 2, "1:josh": 1,
                                           "1:vadas": 1}
        cls.expect_result_03 = {"2:ripple": 1, "1:marko": 1, "1:josh": 1, "1:vadas": 1, "1:peter": 1}
        cls.expect_result_04 = {"2:ripple": 10, "1:marko": 10, "1:josh": 10, "1:vadas": 10, "1:peter": 10,
                                     "2:lop": 10}
        cls.expect_result_05 = {"1:vadas": 10, "1:marko": 7, "1:peter": 7, "1:josh": 6, "2:ripple": 4, "2:lop": 2}
        cls.expect_result_06 = {"2:ripple": 3, "1:marko": 3, "1:peter": 3, "1:josh": 1, "1:vadas": 1,
                                          "2:lop": 1}
        cls.expect_result_07 = {"1:marko": 4, "1:josh": 4, "1:vadas": 4, "1:peter": 4, "2:ripple": 1,
                                           "2:lop": 1}
        cls.expect_result_08 = {"2:ripple": 10, "1:marko": 10, "1:josh": 10, "1:vadas": 10, "1:peter": 10,
                                            "2:lop": 10}
        cls.expect_result_09 = {"2:ripple": 5, "1:josh": 3, "1:vadas": 2, "1:peter": 2, "1:marko": 1,
                                           "2:lop": 1}
        cls.expect_result_10 = {"1:marko": 6, "1:peter": 3, "2:lop": 2, "2:ripple": 1, "1:josh": 1,
                                          "1:vadas": 1}
        cls.expect_result_11 = {"2:ripple": 10, "1:marko": 10, "1:josh": 10, "1:vadas": 10, "1:peter": 10,
                                        "2:lop": 10}
        cls.expect_result_12 = {"2:ripple": 10, "1:marko": 10, "1:josh": 10, "1:vadas": 10, "1:peter": 10}
        cls.expect_result_13 = {"2:ripple": 10, "1:marko": 10, "1:josh": 10, "1:vadas": 10, "1:peter": 10, "2:lop": 10}
        cls.expect_result_14 = {"2:ripple": 3, "1:marko": 3, "1:peter": 3, "1:josh": 1, "1:vadas": 1, "2:lop": 1}
        cls.expect_result_15 = {"2:ripple": 10, "1:marko": 10, "1:josh": 10, "1:vadas": 10, "1:peter": 10,
                                    "2:lop": 10}
        cls.expect_result_16 = {"1:marko": 6, "1:peter": 3, "2:lop": 2, "2:ripple": 1, "1:josh": 1, "1:vadas": 1}
        cls.expect_result_17 = {"2:ripple": 5, "1:josh": 3, "1:vadas": 2, "1:peter": 2, "1:marko": 1, "2:lop": 1}
        cls.expect_result_18 = {"2:ripple": 3, "1:marko": 3, "1:peter": 3, "1:josh": 1, "1:vadas": 1,
                                         "2:lop": 1}
        cls.expect_result_19 = {"2:ripple": 3, "1:marko": 3, "1:peter": 3, "1:josh": 1, "1:vadas": 1, "2:lop": 1}
        cls.expect_result_20 = {"1:marko": 1, "1:josh": 1}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_eigenvector_centrality_01(self):  # 结果会变
        """
        param = [depth]
        :return:
        """
        body = {"depth": 5}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_01), 0, "result check not pass")

    def test_eigenvector_centrality_02(self):  # 结果会变
        """
        param = [depth, source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": -1}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_02), 0, "result check not pass")

    def test_eigenvector_centrality_03(self):  # 结果会变
        """
        param = [depth, source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": 2}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_03), 0, "result check not pass")

    def test_eigenvector_centrality_04(self):
        """
        param = [depth, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_04), 0, "result check not pass")

    def test_eigenvector_centrality_05(self):  # 结果会变
        """
        param = [depth, sample]
        :return:
        """
        body = {"depth": 5, "sample": 2}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_05), 0, "result check not pass")

    def test_eigenvector_centrality_06(self):
        """
        param = [depth, sample, label]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "created"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_06), 0, "result check not pass")

    def test_eigenvector_centrality_07(self):
        """
        param = [depth, sample, label]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "knows"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_07), 0, "result check not pass")

    def test_eigenvector_centrality_08(self):
        """
        param = [depth, sample, direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "BOTH"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_08), 0, "result check not pass")

    def test_eigenvector_centrality_09(self):
        """
        param = [depth, sample, direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "OUT"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_09), 0, "result check not pass")

    def test_eigenvector_centrality_10(self):
        """
        param = [depth, sample, direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "IN"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_10), 0, "result check not pass")

    def test_eigenvector_centrality_11(self):
        """
        param = [depth, sample, degree]
        :return:
        """
        body = {"depth": 5, "sample": -1, "degree": 5}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_11), 0, "result check not pass")

    def test_eigenvector_centrality_12(self):
        """
        param = [depth, sample, top]
        :return:
        """
        body = {"depth": 5, "sample": -1, "top": 5}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_12), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_eigenvector_centrality_13(self):
        """
        param = [depth, sample, top, degree, source_sample]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_13), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_eigenvector_centrality_14(self):
        """
        param = [depth, sample, top, degree, source_sample, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "label":"created"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_14), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_eigenvector_centrality_15(self):
        """
        param = [depth, sample, top, degree, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction":"BOTH"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_15), 0, "result check not pass")

    def test_eigenvector_centrality_16(self):
        """
        param = [depth, sample, top, degree, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction":"IN"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_16), 0, "result check not pass")

    def test_eigenvector_centrality_17(self):
        """
        param = [depth, sample, top, degree, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction": "OUT"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_17), 0, "result check not pass")

    def test_eigenvector_centrality_18(self):
        """
        param = [depth, sample, top, degree, source_sample, direction, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction": "BOTH", "label": "created"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_18), 0, "result check not pass")
        body.pop("direction")
        body.pop("label")

    # @unittest.skip("skip")
    def test_eigenvector_centrality_19(self):
        """
        param = [depth, sample, top, degree, source_sample, direction, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": 10,
                "direction": "BOTH", "label": "created"}
        code, ret = self.alg.post_eigenvector_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_19), 0, "result check not pass")
        body.pop("direction")
        body.pop("label")
        body["source_sample"] = -1

    def test_eigenvector_centrality_20(self):
        """
        :return:source_clabel验证
        """
        pass
        # body_lpa = {"direction": "BOTH"}
        # code, ret = self.alg.post_lpa(body_lpa)
        # id = ret["task_id"]
        # result = self.task.get_task(id)
        # getcode, getret = self.p.init_data("id_clabel")
        # clabel = getret["data"][0]
        # body_new = {"depth": 5, "sample": -1,
        #             "source_clabel": clabel
        #             }
        # code, ret = self.alg.post_eigenvector_centrality(body_new)
        # self.assertEqual(code, 201)
        # id = ret["task_id"]
        # result = self.task.get_task(id)
        # # self.assertEqual(cmp(result, self.expect_result_20), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    unittest.main(verbosity=2)

    # run one case
    # suite = unittest.TestSuite()
    # suite.addTest(TestEigenvectorCentrality("test_eigenvector_centrality_011"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
