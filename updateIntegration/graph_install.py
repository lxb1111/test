# -*- coding:utf-8 -*-
"""
author     : lxb
note       : travis CI --- graph 组件部署
create_time: 2020/4/22 5:17 下午
"""
import sys
import graph_part_install
from utils import loadPath
from utils import setLog

project_path = loadPath.ProjectPath()
logger = setLog.basic_log(project_path.log_file())

if __name__ == "__main__":
    param_1 = sys.argv[1]
    server = graph_part_install.DeployServer()
    hubble = graph_part_install.DeployHubble()

    if param_1 == 'master' or 'integration-LSHT' in param_1:
        ### start server
        # server.git_tar()
        # server.start_server()
        # ### start loader
        graph_part_install.DeployLoader().git_tar()
        # ### start hubble
        hubble.git_tar()
        hubble.start_hubble()
        # ### start tools
        graph_part_install.DeployTools().git_tar()
    elif 'individual-loader' in param_1:
        ### start server
        server.git_tar()
        server.start_server()
        ### start loader
        graph_part_install.DeployLoader().git_tar()
    elif 'individual-server' in param_1:
        server.git_tar()
        server.start_server()
    elif 'individual-hubble' in param_1:
        ### start server
        server.git_tar()
        server.start_server()
        ### start hubble
        hubble.git_tar()
        hubble.start_hubble()
    elif 'individual-tools' in param_1:
        ### start server
        server.git_tar()
        server.start_server()
        ### start tools
        graph_part_install.DeployTools().git_tar()
    else:
        logger.error('---> 输入分支参数错误')
