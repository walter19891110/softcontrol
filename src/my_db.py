
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class SoftInfo(Base):
    """软件基本信息表"""
    # 定义表名
    __tablename__ = 'software_version_control'
    # 定义列对象
    softID = Column(String(256), primary_key=True)  # 主键
    softname = Column(String(256))  # 软件名称
    osname = Column(String(256))  # 运行的操作系统
    softmode = Column(Integer)  # 软件模式，0表示正常模式 1表示调试模式
    setupname = Column(String(256))  # 安装包名称
    setupcodelist = Column(String(256))  # 安装包校验码列表
    mainfile = Column(String(256))  # 主程序文件名
    maincodelist = Column(String(256))  # 主程序文件校验码列表
    desc = Column(String(256))  # 软件描述

    def add_setupcode(self, setupcode):
        """
        将某个安装包校验码添加到该软件的安装包校验码列表中

        :param setupcode: 安装包校验码
        :return: 添加后的安装包校验码列表
        """
        if self.setupcodelist is not None:
            code_list = self.setupcodelist.split(',')
            if setupcode not in code_list:
                code_list.append(setupcode)
                self.setupcodelist = ','.join(code_list)  # 将校验码用逗号连接
        else:
            self.setupcodelist = setupcode

    def del_setupcode(self, setupcode):
        """
        将某个安装包校验码从该软件的安装包校验码列表中删除

        :param setupcode: 安装包校验码
        :return: 更新后的安装包校验码列表
        """
        if self.setupcodelist is not None:
            code_list = self.setupcodelist.split(',')
            for code in code_list:
                if code == setupcode:
                    code_list.remove(setupcode)
            if len(code_list) != 0:
                self.setupcodelist = ','.join(code_list)  # 将校验码用逗号连接

    def add_maincode(self, maincode):
        """
        将某个主程序文件校验码添加到该软件的主程序文件校验码列表中

        :param maincode: 主程序文件校验码
        :return: 添加后的主程序文件校验码列表
        """
        if self.maincodelist is not None:
            code_list = self.maincodelist.split(',')
            if maincode not in code_list:
                code_list.append(maincode)
                self.maincodelist = ','.join(code_list)  # 将校验码用逗号连接
        else:
            self.maincodelist = maincode

    def del_maincode(self, maincode):
        """
        将某个主程序文件校验码从该软件的主程序文件校验码列表中删除

        :param maincode: 主程序文件校验码
        :return: 更新后的主程序文件校验码列表
        """
        if self.maincodelist is not None:
            code_list = self.maincodelist.split(',')
            for code in code_list:
                if code == maincode:
                    code_list.remove(maincode)
            if len(code_list) != 0:
                self.maincodelist = ','.join(code_list)  # 将校验码用逗号连接


class SoftList(Base):
    """可以免于版本控制的软件列表，大部分为基础开发环境软件(java、python)或开源软件(ES、Spark)等"""
    # 定义表名
    __tablename__ = 'soft_list'
    # 定义列对象
    ID = Column(Integer, autoincrement=True, primary_key=True)  # 主键, 自增长
    softname = Column(String(256))  # 软件名称


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:walter135790@localhost:3306/flask_auth?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


if __name__ == "__main__":
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    user = session.query(SoftList).all()
    for i in user:
        print('name:', i.softname)
    # 关闭Session:
    session.close()