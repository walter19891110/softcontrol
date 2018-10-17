"""
安装时软件版本控制
"""
from watchdog.observers import Observer
from watchdog.events import *
import hashlib
import json
import re
import sys
import time
from svc.SoftVersionControl import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


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
client = Client(None)  # 连接服务器的客户端


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


def conn_server(ip, port):
    while True:
        try:
            transport = TSocket.TSocket(ip, port)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = Client(protocol)
            transport.open()
            return client
        except Thrift.TException as e:
            # print(e)
            continue


def init():
    global client
    ip = "localhost"
    port = 9234
    client = conn_server(ip, port)


def analysis_created_file(file):
    # 获取被创建的文件名
    filename = file.split("/")[-1]
    match_str = r"\.(jar|exe)$"
    if re.search(match_str, filename) is not None:
        # print(filename[:-4] + "程序正在安装！")
        # 开始校验可执行文件
        res = verify_md5(file)
        if res["ret_code"] != 0:
            print(filename[:-4], "程序校验失败，禁止安装，删除可执行文件！")
            os.remove(file)


def verify_md5(filename):
    global client
    soft_name = filename.split("/")[-1][:-4]  # 获取无后缀的软件名
    soft_id = soft_name + "_" + os_name
    with open(filename, 'rb') as file:
        data = file.read()
        md5 = hashlib.md5()
        md5.update(data)
        soft_md5 = md5.hexdigest()

    r = client.verify_soft_code(soft_id, 0, soft_md5)
    return json.loads(r)


def install_soft_control():
    init()
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
