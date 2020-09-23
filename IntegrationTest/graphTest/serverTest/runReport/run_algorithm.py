#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/4/27'
"""
import unittest
import time
import os
import sys
import HTMLTestRunner
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)


def suites(case_url, match_content):
    """
    all cases of algorithm
    :param case_url: case的路径
    :param match_content: case匹配
    :return:
    """
    test_unit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_url, pattern=match_content, top_level_dir=None)
    for each_suite in discover:
        for test_case in each_suite:
            test_unit.addTests(test_case)
    return test_unit


if __name__ == '__main__':
    case_list = [
        # {"case": "algorithm_*.py", "report": "all001.html"},
        # {"case": "algorithm_countVertex.py", "report": "countVertex.html"},
        # {"case": "algorithm_countEdge.py", "report": "countEdge.html"},
        # {"case": "algorithm_degreeCentrality.py", "report": "degreeCentrality.html"},
        # {"case": "algorithm_eigenvectorCentrality.py", "report": "eigenvectorCentrality.html"},
        {"case": "algorithm_betweenessCentrality.py", "report": "betweenessCentrality.html"},
        # {"case": "algorithm_closenessCentrality.py", "report": "closenessCentrality.html"},
        # {"case": "algorithm_triangleCount.py", "report": "triangleCount.html"},
        # {"case": "algorithm_clusterCoeffcient.py", "report": "clusterCoeffcient.html"},
        # {"case": "algorithm_lpa.py", "report": "lpa.html"},
        # {"case": "algorithm_louvain.py", "report": "louvain.html"},
        # {"case": "algorithm_kCore.py", "report": "kCore.html"},
        # {"case": "algorithm_fusiformSimilarity.py", "report": "fusiformSimilarity.html"},
        # {"case": "algorithm_ringsDetect.py", "report": "ringsDetect.html"},
    ]
    for data in case_list:
        case_path = os.getcwd() + '/../testCase/algorithm/'
        all_test_name = suites(case_path, data["case"])
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        report_name = os.getcwd() + "/report/report_" + data["report"]

        fp = open(report_name, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="test_report_lxb", description='test_algorithm')
        runner.run(all_test_name)
        fp.close()
