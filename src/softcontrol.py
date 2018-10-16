"""
软件版本控制客户端
"""

import time
from multiprocessing import Process
from run_svc import *
from install_svc import *
import requests
from requests_toolbelt import SSLAdapter


def connect_server():
    # 设置HTTPS
    adapter = SSLAdapter('TLSv1.2')  # 设置证书验证方式为TLSv1.2
    r = requests.Session()
    r.mount('https://', adapter)  # 设置HTTPS的SSL适配器
    ca_file = '../certs/chain-ca.pem'  # 设置根证书
    connect_server_api = "https://127.0.0.1:5000/"
    while True:
        try:
            req = requests.get(connect_server_api, verify=ca_file)
            if req.status_code == 200:
                break
        except Exception as e:
            print(e)
        time.sleep(10)
    print("server connected!")


def running_soft_control():
    running_svc = run_svc.RunSvc()
    running_svc.init()
    while True:
        running_svc.soft_run_control()
        time.sleep(60)


def install_soft_control():
    installing_svc = install_svc.InstallSvc()

    installing_svc.install_soft_control()
    print("install_soft_control")


if __name__ == "__main__":

    print("soft control!")
    connect_server()
    ps = list()
    p1 = Process(target=running_soft_control)
    p2 = Process(target=install_soft_control)
    ps.append(p1)
    ps.append(p2)
    for p in ps:
        p.start()
    for p in ps:
        p.join()
    # install_soft_control()
    print("主进程结束")
