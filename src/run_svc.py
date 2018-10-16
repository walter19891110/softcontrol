"""
运行时软件版本检测
:module:
"""
import hashlib
import platform
import psutil
import re
import requests
from requests_toolbelt import SSLAdapter
import time


class RunSvc(object):

    def __init__(self):
        self.os_name = platform.system()  # 获取系统平台名，Linux、Windows
        self.ca_file = "../certs/chain-ca.pem"  # 设置根证书
        adapter = SSLAdapter('TLSv1.2')  # 设置证书验证方式为TLSv1.2
        r = requests.Session()
        r.mount('https://', adapter)  # 设置HTTPS的SSL适配器
        self.soft_list = list()
        self.user_list = list()

    def init(self):
        """从服务端读取免于版本控制的软件列表"""
        get_soft_list_api = "https://127.0.0.1:5000/api/soft/get_soft_list"
        try:
            r = requests.get(get_soft_list_api, verify=self.ca_file)
        except Exception as e:
            print(e)
            return 1
        self.soft_list = r.json()["softlist"].keys()
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

        verify_soft_code_api = "https://127.0.0.1:5000/api/soft/verify_soft_code"
        data = {"softID": soft_id, "type": 1, "code": soft_md5}
        r = requests.post(verify_soft_code_api, json=data, verify=self.ca_file)
        # print(r.status_code)
        if r.status_code != 200:
            return {"ret_code": r.status_code, "msg": "error"}
        return r.json()


def running_soft_control():
    running_svc = RunSvc()
    running_svc.init()
    while True:
        running_svc.soft_run_control()
        time.sleep(60)


if __name__ == "__main__":
    print("running soft control!")
    running_soft_control()
