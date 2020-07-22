# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 环境部（两种方式：wget url、git clone)
create_time: 2020/4/21 7:15 下午
"""
import subprocess
import sys
import os
from utils import setLog
from utils import loadPath
from config import graph_conf

project_path = loadPath.ProjectPath()
logger = setLog.basic_log(project_path.log_file())


class DeployServer:
    """
    server 部署
    """
    def __init__(self):
        self.wget_url = graph_conf.server['wget']
        self.git_url = graph_conf.server['git']
        self.git_branch = graph_conf.server['branch']

        self.server_host = graph_conf.server['graph']['server_host']
        self.server_port = graph_conf.server['graph']['server_port']
        self.gremlin_port = graph_conf.server['graph']['gremlin_port']

        self.deploy_path = project_path.deploy_graph()
        self.git_path = project_path.git_graph()

    def server_remove(self):
        """
        关闭server、删除server
        :return:
        """
        cmd = 'rm -rf %s/%s' % (self.deploy_path, GetFile('server', self.deploy_path))
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def server_stop(self):
        """
        关闭server
        :return:
        """
        cmd = '%s/%s/bin/stop-hugegraph.sh' % (self.deploy_path, GetFile('server', self.deploy_path))
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def wget_tar(self):
        """
        wget 部署包并解压到部署目录
        :return:
        """
        ### 获取包
        wget_file = os.path.basename(self.wget_url)
        cmd = 'wget -P %s %s && ' \
              'tar xzvf %s/%s -C %s' % (self.deploy_path, self.wget_url,
                                        self.deploy_path, wget_file, self.deploy_path)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def git_tar(self):
        """
        github上拉取代码，编译，解压到部署目录
        :return:
        """
        cmd = 'cd %s && ' \
              'git clone -b %s %s && ' \
              'cd hugegraph/ && ' \
              'mvn clean package -DskipTests ' % (self.git_path, self.git_branch, self.git_url)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

        server_path = self.git_path + '/hugegraph'
        graph_dir = GetFile('server', server_path)
        cmd1 = 'mv %s/%s %s' % (server_path, graph_dir, self.deploy_path)
        logger.info(cmd1)
        subprocess.call(cmd1, shell=True)

    def start_server(self):
        """
        修改配置、初始化server、启动server
        :return:
        """
        graph_dir = GetFile('server', self.deploy_path)
        rest_file = self.deploy_path + '/' + graph_dir + '/conf/rest-server.properties'
        ### 修改配置
        cmd = "sed -i 's/127.0.0.1:8080/%s/g' %s && " \
              "sed -i 's/#gremlinserver/gremlinserver/g' %s && " \
              "sed -i 's/127.0.0.1:8182/%s/g' %s " \
              % (self.server_host + ':' + str(self.server_port), rest_file, rest_file,
                 self.server_host + ':' + str(self.gremlin_port), rest_file)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

        gremlin_file = self.deploy_path + '/' + graph_dir + '/conf/gremlin-server.yaml'
        cmd1 = "sed -i 's/#host: 127.0.0.1/host: %s/g' %s && " \
               "sed -i 's/#port: 8182/port: %d' %s" \
               % (self.server_host, gremlin_file,
                  self.gremlin_port, gremlin_file)
        logger.info(cmd1)
        subprocess.call(cmd1, shell=True)

        ### init
        cmd2 = "%s/%s/bin/init-store.sh" % (self.deploy_path, graph_dir)
        logger.info(cmd2)
        subprocess.call(cmd2, shell=True)
        ### start
        cmd3 = "%s/%s/bin/start-hugegraph.sh" % (self.deploy_path, graph_dir)
        logger.info(cmd3)
        subprocess.call(cmd3, shell=True)


class DeployLoader:
    """
    loader 部署
    """

    def __init__(self):
        self.wget_url = graph_conf.loader["wget"]
        self.git_url = graph_conf.loader["git"]
        self.git_branch = graph_conf.loader["branch"]

        self.deploy_path = project_path.deploy_graph()
        self.git_path = project_path.git_graph()

    def loader_remove(self):
        """
        删除loader
        :return:
        """
        cmd = 'rm -rf %s/%s' % (self.deploy_path, GetFile('loader', self.deploy_path))
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def wget_tar(self):
        """
        wget 部署包并解压到部署目录
        :return:
        """
        wget_file = os.path.basename(self.wget_url)
        cmd = 'wget -P %s %s && ' \
              'tar xzvf %s/%s -C %s' % (self.deploy_path, self.wget_url,
                                        self.deploy_path, wget_file, self.deploy_path)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def git_tar(self):
        """
        github上拉取代码，编译，解压到部署目录
        :return:
        """
        cmd = 'cd %s && ' \
              'git clone -b %s %s && ' \
              'cd hugegraph-loader/ && ' \
              'mvn install:install-file ' \
              '-Dfile=%s/hugegraph-loader/assembly/static/lib/ojdbc8-12.2.0.1.jar ' \
              '-DgroupId=com.oracle ' \
              '-DartifactId=ojdbc8 ' \
              '-Dversion=12.2.0.1 ' \
              '-Dpackaging=jar && ' \
              'mvn clean package -DskipTests' % (self.git_path, self.git_branch, self.git_url, self.git_path)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

        load_path = self.git_path + '/hugegraph-loader'
        graph_dir = GetFile('loader', load_path)
        cmd1 = 'mv %s/%s %s' % (load_path, graph_dir, self.deploy_path)
        logger.info(cmd1)
        subprocess.call(cmd1, shell=True)


class DeployTools:
    """
    tools 部署
    """

    def __init__(self):
        self.wget_url = graph_conf.tools["wget"]
        self.git_url = graph_conf.tools["git"]
        self.git_branch = graph_conf.tools["branch"]

        self.deploy_path = project_path.deploy_graph()
        self.git_path = project_path.git_graph()

    def tools_remove(self):
        """
        删除tools
        :return:
        """
        cmd = 'rm -rf %s/%s' % (self.deploy_path, GetFile('loader', self.deploy_path))
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def wget_tar(self):
        """
        wget 部署包并解压到部署目录
        :return:
        """
        wget_file = os.path.basename(self.wget_url)
        cmd = 'wget -P %s %s && ' \
              'tar xzvf %s/%s -C %s' % (self.deploy_path, self.wget_url,
                                        self.deploy_path, wget_file, self.deploy_path)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def git_tar(self):
        """
        github上拉取代码，编译，解压到部署目录
        :return:
        """
        cmd = 'cd %s && ' \
              'git clone -b %s %s && ' \
              'cd hugegraph-tools/ && ' \
              'mvn clean package -DskipTests' % (self.git_path, self.git_branch, self.git_url)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

        tools_path = self.git_path + '/hugegraph-tools'
        graph_dir = GetFile('tools', tools_path)
        cmd1 = 'mv %s/%s %s' % (tools_path, graph_dir, self.deploy_path)
        logger.info(cmd1)
        subprocess.call(cmd1, shell=True)


class DeployHubble:
    """
    hubble 部署
    """

    def __init__(self):
        self.wget_url = graph_conf.hubble["wget"]
        self.git_url = graph_conf.hubble["git"]
        self.git_branch = graph_conf.hubble["branch"]

        self.host = graph_conf.hubble['host']
        self.port = graph_conf.hubble['port']

        self.deploy_path = project_path.deploy_graph()
        self.git_path = project_path.git_graph()

    def hubble_remove(self):
        """
        删除 hubble
        :return:
        """
        cmd = 'rm -rf %s/%s' % (self.deploy_path, GetFile('loader', self.deploy_path))
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def hubble_stop(self):
        """
        停止 hubble
        :return:
        """
        cmd = '%s/%s/bin/stop-hubble.sh' % (self.deploy_path, GetFile('loader', self.deploy_path))
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def wget_tar(self):
        """
        wget 部署包并解压到部署目录
        :return:
        """
        wget_file = os.path.basename(self.wget_url)
        cmd = 'wget -P %s %s && ' \
              'tar xzvf %s/%s -C %s' % (self.deploy_path, self.wget_url,
                                        self.deploy_path, wget_file, self.deploy_path)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

    def git_tar(self):
        """
        github上拉取代码，编译，解压到部署目录
        :return:
        """
        cmd = 'cd %s && ' \
              'git clone -b %s %s && ' \
              'cd hugegraph-hubble/ && ' \
              'mvn clean package -DskipTests' % (self.git_path, self.git_branch, self.git_url)
        logger.info(cmd)
        subprocess.call(cmd, shell=True)

        hubble_path = self.git_path + '/hugegraph-hubble'
        graph_dir = GetFile('hubble', hubble_path)
        cmd1 = 'mv %s/%s %s' % (hubble_path, graph_dir, self.deploy_path)
        logger.info(cmd1)
        subprocess.call(cmd1, shell=True)

    def start_hubble(self):
        """
        start hubble
        :return:
        """
        properties_file = self.deploy_path + '/' + GetFile('loader', self.deploy_path) + 'hugegraph-hubble.properties'
        cmd = "sed -i 's/server.host=localhost/server.host=%s/g' %s && " \
              "sed -i 's/server.port=8088/server.port=%d/g' %s && " \
              "%s/%s/bin/start-hubble.sh" % (self.host, properties_file,
                                             self.port, properties_file,
                                             self.deploy_path, GetFile('loader', self.deploy_path))
        logger.info(cmd)
        subprocess.call(cmd, shell=True)


def GetFile(file_type, file_path):
    """
    获取包名
    :param file_type: server, loader, hubble, tools
    :param file_path: 文件路径
    :return: file_name
    """
    graph_dir = ""
    re_pattern = {'server': 'hugegraph-0.', 'hubble': 'hugegraph-hubble-1.',
                  'loader': 'hugegraph-loader-0.', 'tools': 'hugegraph-tools-1.'}
    list_dir = os.listdir(file_path)
    for each in list_dir:
        pattern = re_pattern[file_type]
        if pattern in each and '.tar.gz' not in each:
            graph_dir = each
            break
        else:
            pass
    return graph_dir


if __name__ == "__main__":
    # ### loader、server、tools、hubble
    # param_1 = sys.argv[1]
    # ### remove、start、stop
    # param_2 = sys.argv[2]
    #
    # if 'server' == param_1:
    #     if 'remove' == param_2:
    #         DeployServer().server_remove()
    #     elif 'stop' == param_2:
    #         DeployServer().server_stop()
    #     elif 'start' == param_2:
    #         DeployServer().start_server()
    #     elif 'get' == param_2:
    #         if 'wget' == graph_conf.server["mode"]:
    #             DeployServer().wget_tar()
    #         else:  # git 方式
    #             DeployServer().git_tar()
    #     else:
    #         logger.error(' the secondary param if error --- [stop, remove, start, get]')
    #
    # elif 'loader' == param_1:
    #     if 'remove' == param_2:
    #         DeployLoader().loader_remove()
    #     elif 'get' == param_2:
    #         if 'wget' == graph_conf.loader["mode"]:
    #             DeployLoader().wget_tar()
    #         else:  # git方式
    #             DeployLoader().git_tar()
    #     else:
    #         logger.error(' the secondary param if error --- [remove, package]')
    #
    # elif 'tools' == param_1:
    #     if 'remove' == param_2:
    #         DeployTools().tools_remove()
    #     elif 'get' == param_2:
    #         if 'wget' == graph_conf.tools['mode']:
    #             DeployTools().wget_tar()
    #         else:  # git方式
    #             DeployTools().git_tar()
    #     else:
    #         logger.error(' the secondary param if error --- [remove, package]')
    #
    # elif 'hubble' == param_1:
    #     if 'remove' == param_2:
    #         DeployHubble().hubble_remove()
    #     elif 'stop' == param_2:
    #         DeployHubble().hubble_stop()
    #     elif 'get' == param_2:
    #         if 'wget' == graph_conf.hubble['mode']:
    #             DeployHubble().wget_tar()
    #         else:  # git 方式
    #             DeployHubble().git_tar()
    #     elif 'start' == param_2:
    #         DeployHubble().start_hubble()
    #     else:
    #         logger.error(' the secondary param is error --- [remove, start, stop, package]')
    #
    # else:
    #     logger.error(' the first param is error --- [server, loader, tools, hubble]')

    print(GetFile('server', project_path.git_graph()+'/hugegraph'))