import os
import json
import pymysql
from requests import request
import requests
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler

import config

class FilePath(object):

    @classmethod
    def current_file_path(cls):
        '''
        当前的方法，返回的是文件的位置
        :return:
        '''
        return os.path.realpath(__file__)

    @classmethod
    def current_file_dir(cls):
        '''
        返回的当前文件所在的目录

        :return:
        '''
        dir_path = os.path.dirname(cls.current_file_path())
        return dir_path

    @classmethod
    def file_path(cls,*args):
        '''
        当前方法用来拼接文件路径
        :param args: 需要拼接的文件
        :return: 拼接的完整的路径字符串
        '''
        path = os.path.join(*args)
        return path

class HandlerJson(object):

    @classmethod
    def write_json(cls,json_path,data):
        '''
        当前的方法实现的是新建一个json文件
        :param json_path: 文件路径
        :param data: 写入json文件的数据
        :return:
        '''
        f2 = open(json_path, 'w', encoding='utf-8')
        # 将python数据类型转换为json
        json.dump(data, f2, ensure_ascii=False)  # ensure_ascii=False代表中文不转义


    @classmethod
    def read_json(cls,json_path):
        '''
        当前的方法用来读取json文件，将读取的数据以python类型返回
        :param json_path: json文件的路径
        :return: data 数据
        '''
        file = open(json_path, 'r', encoding='utf-8')
        # 将数据转换成python数据类型
        data = json.load(file)
        return data

class HandlerMysql(object):

    @classmethod
    def create_con_cur(cls,db_host,user,pwd,db_name):
        '''
        当前的方法用来创建操作句柄和连接对象
        :param db_host: 数据库的地址
        :param user: 用户名
        :param pwd: 密码
        :param db_name: 数据库的名字
        :return: 返回连接对象和操作句柄
        '''
        con = pymysql.connect(host=db_host,user=user,password=pwd,database=db_name,charset='utf8')
        cur = con.cursor()
        return con,cur

    @classmethod
    def create(cls,con,cur,sql,*args):
        '''
         执行数据库的增加数据功能
        :param con: python与mysql数据库的连接对象
        :param cur: 操作句柄
        :param sql: 插入语句
        :param args: 插入语句需要的数据
        :return: 插入的结果
        '''
        res = cur.execute(sql,args)
        con.commit()
        if res == 0:
            return 'fail'
        else:
            return 'success'

    @classmethod
    def retrieve(cls,cur,sql,count=-1):
        '''
        当前的方法用于返回数据
        :param cur: 操作句柄
        :param sql: 查询语句
        :param count: 需要返回的数量，-1为默认值，默认将查询结果全部返回，必须是int类型
        :return:根据count的数值返回对应的数据
        '''
        cur.execute(sql)

        if isinstance(count,int):
            if count == -1:
                return cur.fetchall()

            elif count == 1:
                return cur.fetchone()

            else:
                return cur.fetchmany(count)
        else:
            raise TypeError("count的数据类型是整数")

    @classmethod
    def update(cls,con,cur,sql,*args):
        '''
         执行数据库的修改数据功能
        :param con: python与mysql数据库的连接对象
        :param cur: 操作句柄
        :param sql: 修改语句
        :param args: 修改语句需要的数据
        :return:
        '''
        res = cur.execute(sql,args)
        con.commit()
        if res == 0:
            return 'fail'
        else:
            return 'success'

    @classmethod
    def delete(cls,con,cur,sql,*args):
        '''
         删除数据
        :param con: python与mysql数据库的连接对象
        :param cur: 操作句柄
        :param sql: 删除语句
        :param args: 删除语句需要的数据
        :return:
        '''
        res = cur.execute(sql,args)
        con.commit()
        if res == 0:
            return 'fail'
        else:
            return 'success'


class RequestProxy(object):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    @classmethod
    def get(cls,url, params=None,headers=None,**kwargs):
        r"""Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        kwargs.update({"headers":cls.headers})
        return request('get', url, params=params ,**kwargs)

    @classmethod
    def options(cls,url, **kwargs):
        r"""Sends an OPTIONS request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)
        kwargs.update({"headers": cls.headers})
        return request('options', url, **kwargs)

    @classmethod
    def head(cls,url, **kwargs):
        r"""Sends a HEAD request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes. If
            `allow_redirects` is not provided, it will be set to `False` (as
            opposed to the default :meth:`request` behavior).
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', False)
        kwargs.update({"headers": cls.headers})
        return request('head', url ,**kwargs)

    @classmethod
    def post(cls,url, data=None, json=None, **kwargs):
        r"""Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.update({"headers": cls.headers})
        return request('post', url, data=data, json=json, **kwargs)

    @classmethod
    def put(cls,url, data=None, **kwargs):
        r"""Sends a PUT request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.update({"headers": cls.headers})
        return request('put', url, data=data, **kwargs)

    @classmethod
    def patch(cls,url, data=None, **kwargs):
        r"""Sends a PATCH request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.update({"headers": cls.headers})
        return request('patch', url, data=data, **kwargs)

    @classmethod
    def delete(cls,url, **kwargs):
        r"""Sends a DELETE request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.update({"headers": cls.headers})
        return request('delete', url, **kwargs)

# 抽取unittest中的参数化所需要的数据
class UnittestParamData():

    @classmethod
    def data_info(cls):
        data_path = './data/login_data.json'
        data = HandlerJson.read_json(data_path)
        param_data_list = []
        print('*' * 50)
        for item in data:
            each_data = tuple(item.values())[0:4]
            param_data_list.append(each_data)
        return param_data_list

class HandlerCsv(object):
    @classmethod
    def read_csv(cls,csv_path,i):
        f = open(csv_path, encoding='utf-8')
        line_list = f.readlines()[1:]
        data_list = []
        for item in line_list:
            data_list.append(item.split(',')[0:i])
        f.close()
        data = []
        ids=[]
        for i in data_list:
            data.append(i[:-1])
            ids.append(i[-1])
        print(f'data={data},ids={ids}')
        return data,ids
    

class LoggerHandler(object):

    @classmethod
    def create_logger(cls,log_name):
        log_path = os.path.join(config.BASE_DIR, 'log',log_name)

        # 设置的日志器
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # 定义格式器
        fmt_str = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
        log_format = logging.Formatter(fmt=fmt_str)

        # 定义写入终端处理器
        stream_handler = logging.StreamHandler()  # 终端
        stream_handler.setFormatter(log_format)

        # 写入到日志文件的处理器
        file_handler = RotatingFileHandler(log_path,maxBytes=1024*1024,backupCount=20,encoding='utf-8')  # 理论上文件可以无限增长
        file_handler.setFormatter(log_format)

        # 将处理器和日志器进行关联
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        return logger



if __name__ == '__main__':
    log_path = os.path.join(config.BASE_DIR,'log','log1.log')
    log = LoggerHandler.create_logger(log_path)
    log.info('这是信息')
    log.error('这是信息')
    # # todo 1.0拿到操作句柄和连接对象
    # con,cur = HandlerMysql.create_con_cur('127.0.0.1','root','root','dingdong')
    # # todo 2.0 创建sql
    # sql1 = 'select  * from goods'
    # # todo 3.0 增删改查
    # # res1 = HandlerMysql.retrieve(cur,sql1,'这是')
    # # print(res1)
    # sql2 = 'delete from goods where id=%s'
    # # "delete from 'goods' where id=1 "
    # # HandlerMysql.delete(cur,con,sql2,32)
    #
    # sql3 = 'insert into goods(goods_name,goods_type,price) values(%s,%s,%s)'
    # # HandlerMysql.create(con,cur,sql3,'香蕉','水果',21.1)
    #
    # sql4 = 'update goods set goods_name=%s where id=%s'
    #
    # HandlerMysql.update(con,cur,sql4,'草莓',32)

