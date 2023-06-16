import os
import json
import pymysql
from requests import request
import logging
from logging.handlers import RotatingFileHandler
import ddddocr

#寻找文件路径
class FilePath(object):
    @classmethod
    def current_file_path(cls):
        '''
        当前的方法，返回的是文件的位置
        :return:
        '''
        #__file__为当前文件路径
        #os.path.realpath 返回绝对路径
        return os.path.realpath(__file__)

    @classmethod
    def current_file_dir(cls):
        '''
        返回的当前文件所在的目录
        :return:
        '''
        #os.path.dirname获取当前文件的父目录
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

#操作json
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

# 操作mysql
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
    def select(cls,cur,sql,count:int=-1):
        '''
        当前的方法用于返回数据
        :param cur: 操作句柄
        :param sql: 查询语句
        :param count: 需要返回的数量，-1为默认值，默认将查询结果全部返回，必须是int类型
        :return:根据count的数值返回对应的数据
        '''
        cur.execute(sql)

        if isinstance(count,int):
            #结果全部返回
            if count == -1:
                return cur.fetchall()
            #只返回第一行
            elif count == 1:
                return cur.fetchone()
            #返回指定行数的数据
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

#这是一个使用 requests 库进行 HTTP 请求的封装类 RequestProxy，它提供了常见的 HTTP 请求方法，包括 GET、POST、PUT、PATCH、DELETE 等。
class RequestProxy(object):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    @classmethod
    def get(cls,url, params=None,headers=None,**kwargs):
        """
        发送 GET 请求。
        :param url: 新的 `Request` 对象的 URL。
        :param params: (可选) 用于发送查询字符串的字典、元组列表或字节。
        :param **kwargs: `request` 方法可接受的可选参数。
        :return:`Response` 对象
        """
        #是否允许重定向
        kwargs.setdefault('allow_redirects', True)
        #更新请求头
        kwargs.update({"headers":cls.headers})
        return request('get', url, params=params ,**kwargs)

    #查询服务器支持的请求方法、头部信息、认证要求等
    @classmethod
    def option(cls,url, **kwargs):
        """
        发送 OPTIONS 请求。
        :param url: 新的 `Request` 对象的 URL。
        :param **kwargs: `request` 方法可接受的可选参数。
        :return: :class:`Response` 对象
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)
        kwargs.update({"headers": cls.headers})
        return request('options', url, **kwargs)

    @classmethod
    def head(cls,url, **kwargs):
        """
        发送 HEAD 请求。

        :param url: 新的 `Request` 对象的 URL。
        :param **kwargs: `request` 方法可接受的可选参数。如果未提供 `allow_redirects` 参数，将被设置为 `False`（与 `request` 的默认行为相反）。
        :return:`Response` 对象e
        """

        kwargs.setdefault('allow_redirects', False)
        kwargs.update({"headers": cls.headers})
        return request('head', url ,**kwargs)

    @classmethod
    def post(cls,url, data=None, json=None, **kwargs):
        '''
        :param url: 新的 :class:`Request` 对象的 URL。
        :param data: （可选）要发送到 :class:`Request` 的请求体中的字典、元组列表、字节或类似文件的对象。
        :param json: （可选）要发送到 :class:`Request` 的请求体中的 JSON 数据。
        :param \*\*kwargs: ``request`` 接受的可选参数。
        :return:`Response <Response>` 对象
        '''
        kwargs.update({"headers": cls.headers})
        return request('post', url, data=data, json=json, **kwargs)

    @classmethod
    def put(cls,url, data=None, **kwargs):
        """
        :param url: 新的 :class:`Request` 对象的 URL。
        :param data: （可选）要发送到 :class:`Request` 的请求体中的字典、元组列表、字节或类似文件的对象。
        :param json: （可选）要发送到 :class:`Request` 的请求体中的 JSON 数据。
        :param \*\*kwargs: ``request`` 接受的可选参数。
        :return:`Response <Response>` 对象
        """
        kwargs.update({"headers": cls.headers})
        return request('put', url, data=data, **kwargs)

    @classmethod
    def patch(cls,url, data=None, **kwargs):
        """
        :param url: 新的 :class:`Request` 对象的 URL。
        :param data: （可选）要发送到 :class:`Request` 的请求体中的字典、元组列表、字节或类似文件的对象。
        :param json: （可选）要发送到 :class:`Request` 的请求体中的 JSON 数据。
        :param \*\*kwargs: 可选参数，将传递给 ``request`` 方法。
        :return:`Response <Response>` 对象
        """
        kwargs.update({"headers": cls.headers})
        return request('patch', url, data=data, **kwargs)

    @classmethod
    def delete(cls,url, **kwargs):
        """    
        :param url: 新的 :class:`Request` 对象的 URL。
        :param \*\*kwargs: 可选参数，将传递给 ``request`` 方法。
        :return: :class:`Response <Response>` 对象
        :rtype: requests.Response
        """
        kwargs.update({"headers": cls.headers})
        return request('delete', url, **kwargs)

# 抽取pytest中的参数化所需要的数据
class PytestParamData():
    #抽取json的前i列数据
    @classmethod
    def data_json(cls,json_path,i=None):
        '''
        传入i将每行前i列数据装在list中，不会进行注释处理
        如果不传入i则默认将key为'name'的列识别成数据的注释
        '''
        data = HandlerJson.read_json(json_path)
        param_data_list = []
        if i:
            for item in data:
                each_data = tuple(item.values())[0:i]
                param_data_list.append(each_data)
        else:
           for item in data:
                idata = {key: value for key, value in item.items() if key != 'name'}
                param_data_list.append([item.get('name'), idata])

        return param_data_list
    @classmethod
    def data_csv(cls,csv_path,i,annotation:int=1):
        '''
        对csv数据进行测试数据的参数化抽取，csv最后一列需为该行数据的注释
        :param csv_path:csv文件路径
        :param i:取csv的i列数据
        :param annotation:是否进行注释处理,1是 0否
        :return data:参数化数据
        :return ids:数据的注释
        '''
        with open(csv_path,encoding='utf-8') as f:
            #去除首行
            line_list = f.readlines()[1:]
        data_list = [[field.rstrip('\n') for field in line.split(',')[:i]] for line in line_list]
        
        if annotation:
            #前i-1列为数据，装在一个list中
            #最后一列为该行数据的注释，所有注释在一个list中
            data_list = [[i[-1], i[:-1]] for i in data_list]
        return data_list

#创建logger
class LoggerHandler(object):

    @classmethod
    def create_logger(log_name):
        '''
        当前的函数完成的功能
        添加日志文件,输出文件到控制台
        :param log_name: 文件的名字
        :return: 日志操作句柄
        '''
        

        # 当前文件父目录
        path = os.path.dirname(os.path.abspath(__name__))
        #根目录
        path = os.path.dirname(path)
        #根目录下log目录
        log_path = os.path.join(path, 'log')
        #创建日志记录器
        logger = logging.getLogger(log_name)
        logger.setLevel('INFO')
        #创建日志格式化器
        #%(levelno)s: 打印日志级别的数值
        # %(levelname)s: 打印日志级别名称
        # %(pathname)s: 打印当前执行程序的路径,其实就是sys.argv[0]
        # %(filename)s: 打印当前执行程序名
        # %(funcName)s: 打印日志的当前函数
        # %(lineno)d: 打印日志的当前行号
        # %(asctime)s: 打印日志的时间
        # %(thread)d: 打印线程ID
        # %(threadName)s: 打印线程名称
        # %(process)d: 打印进程ID
        # %(message)s: 打印日志信息
        # %(name)s: 打印log文件名
        # %(lineno)d: 该log由第几行打印
        fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
        log_formate = logging.Formatter(fmt)
        # 日志写入路径
        file_name = os.path.join(log_path, log_name)
        
        # 创建文件日志处理器
        file_handler = RotatingFileHandler(
            file_name, maxBytes=20*1024*1024, backupCount=10, encoding='utf-8')
        file_handler.setLevel('INFO')
        # 创建流日志处理器,也就是在控制台输出
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel('INFO')
        # 设置处理器的日志格式化器
        file_handler.setFormatter(log_formate)
        stream_handler.setFormatter(log_formate)
        # 将流日志处理器和文件日志处理器添加到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger

#md5加密
def md5_util(key:str,style:str='lower',count:int=32)->str:
    '''
    md5加密
    :param key: 要加密的数据
    :param style:加密后的数据大小写
    :param count:加密的位数
    :return: 加密后的md5值
    '''
    import hashlib
    target_str = hashlib.md5()
    target_str.update(key.encode("utf-8"))

    if style == 'upper' and count == 32:
        return (target_str.hexdigest()).upper()
    elif style == 'lower' and count == 32:
        return (target_str.hexdigest()).lower()

    elif style == 'upper' and count == 16:
        return (target_str.hexdigest())[8:-8].upper()

    elif style == 'lower' and count == 16:
        return (target_str.hexdigest())[8:-8].lower()
    else:
        return None

#图片验证码处理
def get_code(session,url,type=0):
    '''
    图片验证码处理，注意修改验证码保存路径
    :param req:session对象
    :param url:请求的验证码url
    :param type:0 自动识别,1 保存图片到本地手动识别
    :return code:识别的验证码
    '''
    ocr = ddddocr.DdddOcr()
    code=session.get(url)
    
    
    code = ocr.classification(code.content)
    #可对识别不准确的验证码二次处理
    # res=res.replace('日','8',4).replace('口','0',4).replace('己','2',4).replace('d','0',4)
    if type:
        #将验证码保存到指定目录，手动识别
        with open('data/code.jpg', 'wb') as f:
            f.write(code.content)
        code=input('输入验证码：')
    return code
# if __name__ == '__main__':
#     log_path = os.path.join(config.BASE_DIR,'log','log1.log')
#     log = LoggerHandler.create_logger(log_path)
#     log.info('这是信息')
#     log.error('这是信息')
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

