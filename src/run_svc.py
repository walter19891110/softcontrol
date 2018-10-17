"""
运行时软件版本检测
:module:
"""
import hashlib
import os
import platform
import psutil
import re
import time
import json
from svc.SoftVersionControl import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class RunSvc(object):

    def __init__(self):
        self.os_name = "linux"  # 获取系统平台名，Linux、Windows
        self.client = Client(None)  # 初始化客户端
        self.soft_list = list()  # 免于版本控制的软件列表
        self.user_list = list()  # 监控的用户列表

    def init(self):
        """从服务端读取免于版本控制的软件列表"""
        if os.name == "nt":
            self.os_name = "windows"
        elif sys.platform.startswith("darwin"):  # OSX
            self.os_name = "Darwin"
        else:
            self.os_name = "linux"

        conn_flag = True
        while conn_flag:
            try:
                transport = TSocket.TSocket('localhost', 9234)
                transport = TTransport.TBufferedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                self.client = Client(protocol)
                transport.open()
                conn_flag = False
            except Thrift.TException as e:
                # print(e)
                continue

        try:
            r = self.client.get_soft_list()
        except Exception as e:
            print(e)
            return 1
        self.soft_list = json.loads(r)["softlist"].keys()
        self.user_list.append("walter")
        return 0

    def soft_run_control(self):
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)  # 获取指定进程的进程信息
            if p.username() in self.user_list:
                self.soft_run_info(p)

    def soft_run_info(self, p):
        # print(p.name())
        if p.name() == "java":  # Java程序
            cmd_str = p.cmdline()[2]  # 获取jar文件路径
            match_str = r"\.jar$"
            if re.search(match_str, cmd_str) is not None:
                soft_name = cmd_str.split("/")[-1][:-4]  # 获取软件名
                if cmd_str[0] != "/":  # 路径第一个字符不是'/'，说明不是使用的绝对路径
                    cmd_str = p.cwd() + "/" + cmd_str  # 和工作目录一起，拼接出绝对路径
                res = self.verify_md5(cmd_str, soft_name)
                if res["ret_code"] != 0:
                    print(soft_name, res["msg"])
            else:
                # 不是使用jar文件启动的，如ES、spark、hadoop等，逐个排查系统中部署的此类软件
                cmd_str = " ".join(p.cmdline())
                illegal_run = True
                for match_str in self.soft_list:
                    if re.search(match_str, cmd_str) is not None:
                        illegal_run = False
                        print(match_str + "不需进行版本控制!")
                        break
                if illegal_run:
                    # 不在列表中，说明是非法运行的程序，需进行告警
                    print("非法程序, 启动命令为", cmd_str)
        elif "python" in p.name() or "Python" in p.name():
            cmd_str = p.cmdline()[1]
            soft_name = cmd_str.split("/")[-1][:-3]  # 获取软件名
            if cmd_str[0] != "/":  # 路径第一个字符不是'/'，说明不是使用的绝对路径
                cmd_str = p.cwd() + "/" + cmd_str  # 和工作目录一起，拼接出绝对路径

            res = self.verify_md5(cmd_str, soft_name)
            if res["ret_code"] != 0:
                print(soft_name, res["msg"])
        else:
            # c语言程序直接使用p.exe()，即可找到主程序文件
            # self.verify_md5(p.exe(), p.name())
            pass

    def verify_md5(self, filename, soft_name):
        os_name = platform.system()
        soft_id = soft_name + "_" + os_name
        with open(filename, 'rb') as file:
            data = file.read()
            md5 = hashlib.md5()
            md5.update(data)
            soft_md5 = md5.hexdigest()

        r = self.client.verify_soft_code(soft_id, 1, soft_md5)
        return json.loads(r)


def running_soft_control():
    running_svc = RunSvc()
    running_svc.init()
    while True:
        running_svc.soft_run_control()
        time.sleep(60)


if __name__ == "__main__":
    print("running soft control!")
    running_soft_control()
