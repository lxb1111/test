# -*- coding:utf-8 -*-
"""
author  : lxb
note    : test CI use github action
time    : 2021/6/23 4:10 下午
"""
import unittest


class TestCase(unittest.TestCase):
    """
    test
    """
    def setUp(self):
        """
        case start
        :return:
        """
        self.a = 1
        self.b = 2

    def test_case_1(self):
        """
        case run
        :return:
        """
        c = self.a + self.b
        self.assertEqual(3, c)
    
    def test_case_2(self):
        """
        case run
        :return:
        """
        c = self.a + self.b
        self.assertEqual(3, c)
