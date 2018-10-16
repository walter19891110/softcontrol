from svc.SoftVersionControl import *
from my_db import DBSession
from my_db import SoftList
from my_db import SoftInfo
import json
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# 创建Session:
session = DBSession()


class SoftVersionControlHandler:
    """
    真正的服务代码。
    类名为hrift中定义的服务名+Handler
    函数名、参数等要与thrift中服务名下定义的接口一致
    """
    def verify_soft_code(self, soft_id, verify_type, verify_code):
        """
        验证软件校验码，verify_type为0，校验安装包，verify_type为1 校验主程序文件

        :param soft_id:
            软件ID
        :param verify_type:
            校验码类型，0为安装包校验码，1为主程序文件校验码
        :param verify_code:
            软件描述
        :return:
            {"ret_code": ret_code, "msg": msg}
        """
        ret_code = 0
        msg = "OK"

        if soft_id is None or verify_type is None or verify_code is None:
            ret_code = 1
            msg = "missing arguments!"
            result = {"ret_code": ret_code, "msg": msg}
            return json.dumps(result)

        soft_info = session.query(SoftInfo).filter_by(softID=soft_id).first()
        if soft_info is None:
            ret_code = 1
            msg = "soft not exist!"
            result = {"ret_code": ret_code, "msg": msg}
            return json.dumps(result)

        if verify_type not in (0, 1):
            ret_code = 2
            msg = "type value err!"
            result = {"ret_code": ret_code, "msg": msg}
            return json.dumps(result)
        if soft_info.softmode == 0:  # 如果是正常模式，进行校验，否则是调试模式，不用校验，直接返回校验通过
            codelist = soft_info.setupcodelist
            if verify_type == 1:
                codelist = soft_info.maincodelist
            # print(code, codelist)
            if (codelist is None) or (verify_code not in codelist.split(',')):
                ret_code = 3
                msg = "verify failed!"

        result = {"ret_code": ret_code, "msg": msg}
        return json.dumps(result)

    def get_soft_info(self, soft_id):
        """
        查看软件信息

        :param soft_id:
            软件ID
        :return:
            {"ret_code": ret_code, "msg": msg}
        """
        ret_code = 0
        msg = "OK"

        if soft_id is None:
            ret_code = 1
            msg = "missing arguments!"
            result = {"ret_code": ret_code, "msg": msg}
            return json.dumps(result)

        soft_info = session.query(SoftInfo).filter_by(softID=soft_id).first()
        if soft_info is None:
            ret_code = 1
            msg = "soft not exist!"
            result = {"ret_code": ret_code, "msg": msg}
            return json.dumps(result)

        soft_json = {"softID": soft_info.softID,
                     "softname": soft_info.softname,
                     "osname": soft_info.osname,
                     "softmode": soft_info.softmode,
                     "setupname": soft_info.setupname,
                     "setupcodelist": soft_info.setupcodelist,
                     "mainfile": soft_info.mainfile,
                     "maincodelist": soft_info.maincodelist,
                     "desc": soft_info.desc}

        result = {"ret_code": ret_code, "msg": msg, "softinfo": soft_json}
        return json.dumps(result)

    def get_soft_list(self):
        """
        查看软件信息

        :return:
            {"ret_code": ret_code, "msg": msg}
        """
        ret_code = 0
        msg = "OK"

        soft_dict = dict()
        for soft in session.query(SoftList).all():
            soft_dict[soft.softname] = soft.softname
        result = {"ret_code": ret_code, "msg": msg, "softlist": soft_dict}
        return json.dumps(result)


def run():
    """服务运行代码"""
    # 创建服务端
    handler = SoftVersionControlHandler()
    processor = Processor(handler)

    # 监听端口
    transport = TSocket.TServerSocket('localhost', 9234)

    # 选择传输层
    tfactory = TTransport.TBufferedTransportFactory()

    # 选择传输协议
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # 创建服务端
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    server.setNumThreads(5)

    print('start thrift serve in python')
    server.serve()
    print('done!')


if __name__ == '__main__':
    run()
