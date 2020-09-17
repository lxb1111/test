# -*- coding: UTF-8 -*-
"""
author:lxb
note  : set log_level
"""
import logging
import time


def basic_log(file_path):
    """
    set log
    :return:
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(asctime)s - %(lineno)d:%(filename)s:%(funcName)s: - %(message)s')
    ### debug级的log文件写入设置
    handler = logging.FileHandler(file_path)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    ### warn级的log打印设置
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)
    return logger


if __name__ == '__main__':
    ### test
    print(time.ctime())
    log = basic_log('/Users/lixiaobiao/Documents/lixiaobiao/codeWorkSpace/icode/baidu/'
                    'lxb-test/xbu-test-python/xbu_test_python/IntegrationTest/'
                    'log/test.log')
    try:
        open('sklearn.txt', "rb")
    except Exception:
        log.exception("Failed to open sklearn.txt from logger.exception")
