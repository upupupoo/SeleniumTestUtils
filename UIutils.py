from helium  import *
import time
import json
from PIL import Image
import pytesseract
from appium import webdriver as appdriver
from selenium import webdriver 
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
import sys
sys.path.append('.')
#config为自己的配置文件
import config




class AppDriverTool:

    _driver = None
    @classmethod
    def get_driver(cls,app_pack='com.android.launcher3',appact='.launcher3.Launcher'):
        if cls._driver is None:
            desired_caps = dict(
                platformName='Android',  # 平台，是Android还是IOS
                platformVersion='9',  # 安卓的版本
                deviceName='emulator-5554',
                automationName='uiautomator2',
                # 包名
                appPackage=app_pack,
                # 界面名
                appActivity=appact
            )
            cls._driver = appdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
            return cls._driver
        else:
            return cls._driver

    @classmethod  # 类方法修改的是类属性
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None

class DriverTool:
    driver=None
    @classmethod
    def create_driver(cls):
        if cls.driver is None:
            # 加启动配置
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option('detach',True) #不自动关闭浏览器
            #配置自己的config文件中的headers
            chrome_options.add_argument('--user-agent='+config.HEADERS["User-Agent"])  # 设置请求头的User-Agent
            #chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])#禁止打印日志
            #chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])#实现了规避监测
            chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])#上面两个可以同时设置
            #chrome_options.add_argument('--headless') # 无头模式
            chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
            chrome_options.add_argument('--start-maximized')#最大化
            #chrome_options.add_argument('--disable-extensions')  # 禁用扩展
            chrome_options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
            #chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
            #chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            #chrome_options.add_argument('--disable-javascript')  # 禁用javascript
            #chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            #chrome_options.add_argument('--disable-software-rasterizer')  # 禁用 3D 软件光栅化器
            chrome_options.add_argument('--incognito')#无痕隐身模式
            chrome_options.add_argument("disable-cache")#禁用缓存
            chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
            chrome_options.add_argument('log-level=3')#INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
            cls.driver = webdriver.Chrome(chrome_options=chrome_options)
            return cls.driver
        else:
            return cls.driver
    @classmethod
    def close_driver(cls):
        if cls.driver is not None:
            cls.driver.close()
            cls.driver=None

# helium处理
#helium定位元素
def s(value,**local):
    '''
    定位app中的元素
    :param value:方式对应的值
    :return: 将元素进行返回
    '''
    try:
        element=S(value)
        # else:
        #     for direction in local.keys():
        #         if direction=='below':
        #             element=S(value,below=local[direction])
        #         elif direction=='above':
        #             element=S(value,above=local[direction])
        #         elif direction=='to_right_of':
        #             element=S(value,to_right_of=local[direction])
        #         elif direction=='to_left_of':
        #             element=S(value,to_left_of=local[direction])
        return element
    except Exception as e:
        print('-------------------->定位不到元素，出错的语句是',value)
        return value

#helium點擊
def heclick(element):
    '''
    在输入框中输入数据
    :param element: 元素
    :return:
    '''
    try:
        click(element)
    except Exception as e:
        print(f'------------------------->{element}当前元素未获取')

#helium輸入
def hewrite(value,element):
    '''
    在输入框中输入数据
    :param value: 输入值
    :param element: 元素
    :return:
    '''
    try:
        write(value,into=element)
    except Exception as e:
        print(f'------------------------->{element}当前元素未获取')

#helium獲取元素屬性
def get_ele_attribute(element,att):
    try:
        if att=='text':
            return element.web_element.text
        else:
            return element.web_element.get_attribute(att)
    except Exception as e:
        print(f'------------------------->{element}当前元素未获取')

#helium悬浮
def hehover(element):
    try:
        hover(element)
    except Exception as e:
        print(f'------------------------->{element}当前元素未获取')

# selenium处理
def get_single_element(driver,style,value):
    '''
    定位app中的元素
    :param driver: appium操作句柄
    :param style: 定位元素的方式
    :param value:方式对应的值
    :return: 将元素进行返回
    '''

    try:
        element = WebDriverWait(driver,10).until(lambda x:x.find_element(style,value))
        return element
    except Exception as e:
        print('-------------------->定位不到元素，出错的语句是',value)
        element = None
        return element

def get_elements(driver,style,value):
    '''
    获取多个元素
    :param driver:
    :param style:
    :param value:
    :return: 返回的是多个元素组成的列表
    '''
    try:
        element = WebDriverWait(driver,10).until(lambda x:x.find_elements(style,value))
        return element
    except Exception as e:
        print('-------------------->定位不到元素，出错的语句是',value)
        element = None
        return element


def input_text(element,data):
    '''
    在输入框中输入数据
    :param element: 元素
    :param data: 数据
    :return:
    '''
    if element:
        element.clear()
        element.send_keys(data)
    else:
        print('------------------------->当前元素未获取')


def click_element(element):
    if element:
        element.click()
    else:
        print('------------------------->当前元素未获取')

def back_prepage(driver):
    element = get_single_element(driver,By.XPATH,"//*[@content-desc='转到上一层级']")
    if element:
        element.click()

    else:
        print('----------->返回上一页失败，返回键定位不到')


# 滑动
def handler_swipe(driver,start_x,start_y,end_x,end_y):
    driver.swipe(start_x,start_y,end_x,end_y)



# 高级手势操作
class HandAction:
    # 长按
    @classmethod
    def handler_long_press(cls,location_x,location_y,press_time=1000):
        '''
        长按操作
        :param location_x: 元素的坐标  x
        :param location_y: 元素的坐标  y
        :param press_time: 长按的事件，毫秒,默认是1000
        :return:None
        '''
        ta = TouchAction(AppDriverTool.get_driver())
        ta.long_press(x=location_x,y=location_y,duration=press_time).perform()
        # ta.press(x=150, y=330).wait(1000).release().perform()


    # 轻敲
    @classmethod
    def handler_tap(cls,location_x,location_y):
        '''
        轻敲操作
        :param location_x: 元素的位置 x
        :param location_y: 元素的位置 y
        :return:
        '''
        ta = TouchAction(AppDriverTool.get_driver())
        ta.tap(x=location_x, y=location_y).perform()


    # 长按移动
    @classmethod
    def handler_pressmove(cls,start_x,start_y,target_x,target_y):
        ta = TouchAction(AppDriverTool.get_driver())
        ta.press(x=start_x, y=start_y).move_to(x=target_x, y=target_y).release().perform()

    # 一边滑动，一遍寻找目标元素
    @classmethod
    def swipe_find_element(cls,element,style,value):
        '''
        对于元素的滑动寻找
        :param element: 元素
        :param style: 定位方法
        :param value: 定位规则
        :return:
        '''
        driver = AppDriverTool.get_driver()
        ele_size = element.size  # 获取元素大小
        width = ele_size["width"]  # 获取元素的宽度
        height = ele_size["height"]  # 获取元素的高度
        # 获了element元素左上角点的坐标
        ele_position = element.location
        x = ele_position["x"]  # 获取左上角点的x坐标值
        y = ele_position["y"]  # 获取左上角点的y坐标值

        start_x = x + width * 0.9  # 获取的是起始点X的值
        y = y + height * 0.5  # 获取的是起始及终止点的Y的值
        end_x = x + width * 0.1  # 获取的是终止点X的值
        while True:
            page = driver.page_source  # 记录查找前的页面资源,通过对比页面资源来退出死循环
            try:
                # 如果有找到对应的元素那么点击并返回
                get_single_element(driver,style,value)
                return True
            except Exception as e:
                print("没有找到该元素！")
            driver.swipe(start_x, y, end_x, y, duration=1000)  # 没有找到元素，那么滑屏后再对比并重新查找
            time.sleep(1)
            if page == driver.page_source:
                print("滑屏操作完成且没有找到元素信息")
                return False


# 安卓系统操作
class HandleSys:

    # 设置网络
    @classmethod
    def change_network(cls,ntype=2):
        '''
         | Value (Alias)      | Data | Wifi | Airplane Mode |
            +====================+======+======+===============+
            | 0 (None)           | 0    | 0    | 0             |
            +--------------------+------+------+---------------+
            | 1 (Airplane Mode)  | 0    | 0    | 1             |
            +--------------------+------+------+---------------+
            | 2 (Wifi only)      | 0    | 1    | 0             |
            +--------------------+------+------+---------------+
            | 4 (Data only)      | 1    | 0    | 0             |
            +--------------------+------+------+---------------+
            | 6 (All network on) | 1    | 1    | 0             |
            +--------------------+------+------+---------------+
        :param ntype: 网络模式，默认是2
        :return:
        '''
        AppDriverTool.get_driver().set_network_connection(ntype)

    # 模拟键盘操作
    @classmethod
    def system_keys(cls,num):
        '''
        模拟系统的操作
        HOME  3
        BACK  4
        ENTER  66
        :param num: 数值可查询，以上是常用的按键
        :return:
        '''
        AppDriverTool.get_driver().press_keycode(num)

    # 打开通知栏
    @classmethod
    def bulletin_board(cls):
        AppDriverTool.get_driver().open_notifications()

    @classmethod
    def handler_swipe(cls,direction,count=1):
        # 封装滑屏操作方法
        driver = AppDriverTool.get_driver()
        w = driver.get_window_size()["width"]  # 获取手机屏幕的宽度
        h = driver.get_window_size()["height"]  # 获取手机屏幕的高度
        # w=1080  h=1920
        if direction == "top":  # 往上滑
            zb = (w / 2, h * 0.9, w / 2, h * 0.1)
        elif direction == "down":  # 往下滑
            zb = (w / 2, h * 0.1, w / 2, h * 0.9)
        elif direction == 'left':  # 往左滑
            zb = (w * 0.9, h / 2, w * 0.1, h / 2)
        else:  # 往右滑
            zb = (w * 0.1, h / 2, w * 0.9, h / 2)
        for i in range(count):
            driver.swipe(*zb, duration=1200)
            time.sleep(1)


class JsonTool:

    @classmethod
    def get_testcase_data(cls,file_path):
        '''
        实现读取外部数据，拼接成[(),(),()]
        :return:  需要将拼接的数据做返回，让测试用例使用
        '''
        # 打开文件
        file = open(file_path, encoding='utf-8')
        # 读取文件
        content = file.read()
        # json.dumps()  # 将python数据类型转换成json字符串
        content_list = json.loads(content)  # 将字符串还原成原始的列表或者字典
        data_list = []
        for item in content_list:
            data = tuple(item.values())
            data_list.append(data)

        return data_list


# 获取toast信息
def toast_info_pic(pic_path,left, upper, right, lower):
    '''
    获取toast消息，返回文本内容，配合使用
    :param pic_path: 获取的文件存储名，以png后缀
    :param left: 截取的部分距离左边的距离
    :param upper: 截取的部分距离上边的距离
    :param right: 截取的部分距离右边的距离
    :param lower: 距离的部分距离底部的距离
    :return: 返回页面上的数字
    '''
    path = './img/login_toast_png/'+pic_path
    AppDriverTool.get_driver().get_screenshot_as_file(path)
    img = Image.open(path)
    new_img = img.crop((left,upper,right,lower))
    new_img.save(path)

    # text = pytesseract.image_to_string(Image.open(path), lang='chi_sim')
    text = ''.join(pytesseract.image_to_string(Image.open(path), lang='chi_sim').split(' '))
    print('-------------->获取到的字符串是', text)
    if "!" in text:

        return text.replace('!','！').strip()
    else:
        return text.strip()

def toast_info(driver,pic_path,left, upper, right, lower):
    common_login_element = get_single_element(driver, By.XPATH, "//android.widget.Toast")
    if common_login_element:
        return common_login_element.text
    else:
        path = './img/login_toast_png/' + pic_path
        driver.get_screenshot_as_file(path)
        img = Image.open(path)
        new_img = img.crop((left, upper, right, lower))
        new_img.save(path)
        text = ''.join(pytesseract.image_to_string(Image.open(path), lang='chi_sim').split(' '))
        print('-------------->获取到的字符串是', text)
        if "!" in text:

            return text.replace('!', '！').strip()
        else:
            return text.strip()

def get_target_pic(xmin:int ,ymin:int, xmax:int ,ymax:int,img_path:str,new_img_path:str,driver:object):
    '''
    当前函数用于使用selenium截图页面，进行截图使用
    :param xmin: 裁剪位置
    :param ymin: 裁剪位置
    :param xmax: 裁剪位置
    :param ymax: 裁剪位置
    :param img_path: 存储截图的路径
    :param new_img_path: 裁剪的图片的路径
    :return: 返回截取的图片所在的路径
    '''

    from PIL import Image

    driver.get_screenshot_as_file(img_path)

    im = Image.open(img_path)  # 用PIL打开一个图片
    box = (xmin, ymin, xmax, ymax)  # box代表需要剪切图片的位置格式为:xmin ymin xmax ymax
    ng = im.crop(box)  # 对im进行裁剪 保存为ng(这里im保持不变)
    ng.save(new_img_path)
    return new_img_path


def pic_img(pic_path:str):
    '''
    获取图片上的中文
    :param pic_path: 图片路径
    :return: 返回图片上的文字
    '''
    from PIL import Image
    import pytesseract

    # 读取图片
    image_obj = Image.open(pic_path)

    text = pytesseract.image_to_string(image_obj, lang='chi_sim')
    return text


def create_logger(log_name):
    '''
    当前的函数完成的功能
    添加日志文件，输出文件到控制台
    :param log_name: 文件的名字
    :return: 日志操作句柄
    '''
    import logging
    import os
    from logging.handlers import RotatingFileHandler


    # 日志
    path = os.path.dirname(os.path.abspath(__name__))
    project_path = os.path.dirname(path)

    log_path = os.path.join(project_path,'log')

    logger = logging.getLogger(log_name)
    logger.setLevel('INFO')
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - % (message)s'
    log_formate = logging.Formatter(fmt)

    # 日志写入路径
    file_name = os.path.join(log_path,log_name)

    file_handler = RotatingFileHandler(file_name,maxBytes=20*1024*1024,backupCount=10,encoding='utf-8')
    file_handler.setLevel('INFO')
    file_handler.setFormatter(log_formate)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel('INFO')
    stream_handler.setFormatter(log_formate)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

if __name__ == '__main__':
    log = create_logger('case.log')
    log.info('呵呵呵呵')







