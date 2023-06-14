# from selenium import webdriver
# from helium import *
# class DriverTool:
#     # 网页操作driver
    
#     def __init__(self) -> None:
#         self.driver = None
#     def create_driver(self):
#         if self.driver is None:
#             # 加启动配置
#             chrome_options = webdriver.ChromeOptions()
#             chrome_options.add_experimental_option('detach', True)  # 不自动关闭浏览器
#             # 配置自己的config文件中的headers
#             # chrome_options.add_argument('--user-agent='+config.HEADERS["User-Agent"])  # 设置请求头的User-Agent
#             # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])#禁止打印日志
#             # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])#实现了规避监测
#             chrome_options.add_experimental_option(
#                 "excludeSwitches", ['enable-automation', 'enable-logging'])  # 上面两个可以同时设置
#             # chrome_options.add_argument('--headless') # 无头模式
#             chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
#             chrome_options.add_argument('--start-maximized')  # 最大化
#             # chrome_options.add_argument('--disable-extensions')  # 禁用扩展
#             chrome_options.add_argument(
#                 '--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
#             # chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
#             # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
#             # chrome_options.add_argument('--disable-javascript')  # 禁用javascript
#             # chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
#             # chrome_options.add_argument('--disable-software-rasterizer')  # 禁用 3D 软件光栅化器
#             chrome_options.add_argument('--incognito')  # 无痕隐身模式
#             chrome_options.add_argument("disable-cache")  # 禁用缓存
#             chrome_options.add_argument(
#                 '--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
#             # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
#             chrome_options.add_argument('log-level=3')
#             self.driver = webdriver.Chrome(options=chrome_options)
#             return self.driver
#     def close_driver(self):
#         '''
#         退出driver
#         '''
#         if self.driver:
#             self.driver.close()
#             self.driver = None
# def hewrite(value, element):
#     '''
#     在输入框中输入数据
#     :param value: 输入值
#     :param element: 元素
#     '''
#     try:
#         write(value, into=element)
#     except Exception as e:
#         print(f'------------------------->{element}当前元素未获取')


# b1=DriverTool()
# driver=b1.create_driver()
# set_driver(driver)
# go_to('https://www.baidu.com/')
# hewrite('123',S('#kw'))
from UIutils import JsonTool
print(JsonTool.get_testcase_data('data.json'))