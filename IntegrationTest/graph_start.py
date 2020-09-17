# -*- coding:utf-8 -*-
"""
author     : lxb
note       : travis CI --- graph 组件启动
create_time: 2020/4/22 5:17 下午
"""
import sys


if __name__ == "__main__":
    param_1 = sys.argv[1]
    if param_1 == 'server':
        pass
    elif param_1 == 'hubble':
        pass
    else:
        print('---> 输入分支参数错误')