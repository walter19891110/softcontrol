"""
安装时软件版本控制
"""
from watchdog.observers import Observer
from watchdog.events import *
import hashlib
import re
import sys
import time
import requests
from requests_toolbelt import SSLAdapter

# 设置HTTPS
adapter = SSLAdapter('TLSv1.2')  # 设置证书验证方式为TLSv1.2
r = requests.Session()
r.mount('https://', adapter)  # 设置HTTPS的SSL适配器
ca_file = '../certs/chain-ca.pem'  # 设置根证书

WINDOWS = os.name == "nt"
LINUX = sys.platform.startswith("linux")
OSX = sys.platform.startswith("darwin")
os_name = "linux"
if WINDOWS:
    os_name = "windows"
elif OSX:
    os_name = "Darwin"
else:
    os_name = "linux"


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            pass
        else:
            pass

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            print("file created:{0}".format(event.src_path))
            analysis_created_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            pass

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            pass


def analysis_created_file(file):
    # 获取被创建的文件名
    filename = file.split("/")[-1]
    match_str = r"\.(jar|exe)$"
    if re.search(match_str, filename) is not None:
        print(filename[:-4] + "程序正在安装！")
        # 开始校验可执行文件
        res = verify_md5(file)
        if res["ret_code"] != 0:
            print(filename[:-4], "程序校验失败，禁止安装，删除可执行文件！")
            os.remove(file)


def verify_md5(filename):
    global ca_file, os_name
    soft_name = filename.split("/")[-1][:-4]  # 获取无后缀的软件名
    soft_id = soft_name + "_" + os_name
    with open(filename, 'rb') as file:
        data = file.read()
        md5 = hashlib.md5()
        md5.update(data)
        soft_md5 = md5.hexdigest()

    verify_soft_code_api = "https://127.0.0.1:5000/api/soft/verify_soft_code"
    data = {"softID": soft_id, "type": 0, "code": soft_md5}
    r = requests.post(verify_soft_code_api, json=data, verify=ca_file)
    if r.status_code != 200:
        return {"ret_code": r.status_code, "msg": "error"}
    print(r.json())
    return r.json()


def install_soft_control():
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, "/Users/walter/Downloads", True)
    observer.start()
    print("observer.start()")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("observer.stop()")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    print("install soft control!")
    install_soft_control()
