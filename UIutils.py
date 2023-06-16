from helium import *
import time
from PIL import Image
import pytesseract
from appium import webdriver as appdriver
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
sys.path.append('.')
# config为自己的配置文件
#import config


class AppDriverTool:
    # app操作driver
    _driver = None

    @classmethod
    def get_driver(cls, app_pack: str = 'com.android.launcher3', appact: str = '.launcher3.Launcher') -> appdriver:
        '''
        app获取driver
        :param app_pack: app包名
        :param appact:Activity名
        :return: driver
        '''
        if cls._driver is None:
            desired_caps = dict(
                platformName='Android',  # 平台,是Android还是IOS
                platformVersion='9',  # 安卓的版本
                deviceName='emulator-5554',
                automationName='uiautomator2',
                # 包名
                appPackage=app_pack,
                # 界面名
                appActivity=appact
            )
            cls._driver = appdriver.Remote(
                'http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
            return cls._driver
        else:
            return cls._driver

    @classmethod  # 类方法修改的是类属性
    def quit_driver(cls):
        '''
        退出driver
        '''
        if cls._driver:
            cls._driver.quit()
            cls._driver = None

class DriverTool:
    # 网页操作driver
    driver = None

    @classmethod
    def create_driver(cls) -> webdriver:
        '''
        创建driver
        :return:driver
        '''
        if cls.driver is None:
            # 加启动配置
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option('detach', True)  # 不自动关闭浏览器
            # 配置自己的config文件中的headers
            # chrome_options.add_argument('--user-agent='+config.HEADERS["User-Agent"])  # 设置请求头的User-Agent
            # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])#禁止打印日志
            # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])#实现了规避监测
            chrome_options.add_experimental_option(
                "excludeSwitches", ['enable-automation', 'enable-logging'])  # 上面两个可以同时设置
            # chrome_options.add_argument('--headless') # 无头模式
            chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
            chrome_options.add_argument('--start-maximized')  # 最大化
            # chrome_options.add_argument('--disable-extensions')  # 禁用扩展
            chrome_options.add_argument(
                '--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
            # chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
            # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            # chrome_options.add_argument('--disable-javascript')  # 禁用javascript
            # chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            # chrome_options.add_argument('--disable-software-rasterizer')  # 禁用 3D 软件光栅化器
            chrome_options.add_argument('--incognito')  # 无痕隐身模式
            chrome_options.add_argument("disable-cache")  # 禁用缓存
            chrome_options.add_argument(
                '--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
            # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
            chrome_options.add_argument('log-level=3')
            cls.driver = webdriver.Chrome(chrome_options=chrome_options)
            return cls.driver
        else:
            return cls.driver

    @classmethod
    def close_driver(cls):
        '''
        退出driver
        '''
        if cls.driver:
            cls.driver.close()
            cls.driver = None

# helium处理
class HeliumTool:
    # helium定位元素
    @classmethod
    def s(cls, value: str, **local) -> S.web_element:
        '''
        定位app中的元素
        :param value:定位方式对应的值
        :return: 将元素进行返回
        '''
        try:
            element = S(value)
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
            print('-------------------->定位不到元素,出错的语句是', value)

    # helium點擊
    @classmethod
    def heclick(cls, element):
        '''
        在输入框中输入数据
        :param element: 元素
        '''
        try:
            click(element)
        except Exception as e:
            print(f'------------------------->{element}当前元素未获取')

    # helium輸入
    @classmethod
    def hewrite(cls, value, element):
        '''
        在输入框中输入数据
        :param value: 输入值
        :param element: 元素
        '''
        try:
            write(value, into=element)
        except Exception as e:
            print(f'------------------------->{element}当前元素未获取')

    # helium獲取元素屬性
    @classmethod
    def get_ele_attribute(cls, element, att):
        '''
        获取元素的属性
        :param element:要获取属性的元素
        :param element:要获取的属性
        :return:获取属性的值
        '''
        try:
            if att == 'text':
                return element.web_element.text
            else:
                return element.web_element.get_attribute(att)
        except Exception as e:
            print(f'------------------------->{element}当前元素未获取')

    # helium悬浮
    @classmethod
    def hehover(cls, element):
        '''
        helium鼠标悬浮
        :param element:要悬浮的属性
        '''
        try:
            hover(element)
        except Exception as e:
            print(f'------------------------->{element}当前元素未获取')

# selenium和appium处理
class SeleniumTool:
    def get_single_element(cls, driver, style, value):
        '''
        定位app中的元素
        :param driver: appium操作句柄
        :param style: 定位元素的方式
        :param value:方式对应的值
        :return: 将元素进行返回
        '''
        try:
            element = WebDriverWait(driver, 10).until(
                lambda x: x.find_element(style, value))
            return element
        except Exception as e:
            print('-------------------->定位不到元素,出错的语句是', value)
            element = None
            return element

    def get_elements(cls, driver, style, value):
        '''
        获取多个元素
        :param driver:
        :param style:
        :param value:
        :return: 返回的是多个元素组成的列表
        '''
        try:
            element = WebDriverWait(driver, 10).until(
                lambda x: x.find_elements(style, value))
            return element
        except Exception as e:
            print('-------------------->定位不到元素,出错的语句是', value)
            element = None
            return element

    def input_text(cls, element, data):
        '''
        在输入框中输入数据
        :param element: 元素
        :param data: 数据
        '''
        if element:
            element.clear()
            element.send_keys(data)
        else:
            print('------------------------->当前元素未获取')

    def click_element(cls, element):
        '''
        点击元素
        :param element: 元素
        '''
        if element:
            element.click()
        else:
            print('------------------------->当前元素未获取')
         
# 鼠标操作
class HandleMouseActionTool:
    def __init__(self,driver):
        self.action = ActionChains(driver)

    # 右击
    def right_click(self,element):
        self.action.context_click(element)
        self.action.perform()
    # 双击
    def twice_click(self,element):
        self.action.double_click(element)
        self.action.perform()

    # 拖动
    def drag_drop(self,source,target):
        '''
        :param source:要拖动的元素
        :param target:目标元素
        '''
        self.action.drag_and_drop(source,target).perform()

    # 悬停
    def move_element(self,element):
        self.action.move_to_element(element)
        self.action.perform()   

# 键盘操作
class HandleKeysTool:

    # 删除键
    def delete_key(self,element):
        element.send_keys(Keys.BACK_SPACE)

    # 全选
    def all_choose(self,element):
        element.send_keys(Keys.CONTROL,'a')

    # 复制
    def ctrl_c(self,element):
        element.send_keys(Keys.CONTROL, 'c')

    # 粘贴
    def ctrl_v(self,element):
        element.send_keys(Keys.CONTROL, 'v')
    # 回车
    def enter(self,element):
        element.send_keys(Keys.ENTER)
 
#alert/confirm/prompt操作   
class AlertTool:
    def __init__(self, driver):
        self.alert = driver.switch_to.alert
    #获取alert文本
    def alert_info(self):
        return self.alert.text
    #确认弹窗
    def alert_accept(self):
        self.alert.accept()
    #拒绝弹窗
    def alert_dismiss(self):
        self.alert.dismiss()   
    #在prompt中输入数据
    def alert_input_info(self,info):
        '''
        当前的方法,用于在prompt中输入数据
        :param info:
        :return:
        '''
        self.alert.send_keys(info)

# 切换frame
class HandleIframeTool:
    def __init__(self,driver):
        self.driver = driver

    # 切入到iframe
    def switch_iframe(self,element):
        self.driver.switch_to.frame(element)

    # 切回原始页面
    def back_page(self):
        self.driver.switch_to.default_content()

# 切换窗口
def switch_windows(driver,index:int):
    '''
    根据传入的index切换窗口
    :param index:句柄下标，-1为最新的窗口
    :return new_handle:返回选定的窗口句柄
    '''
    # 获取当前窗口的句柄
    current_handle = driver.current_window_handle
    # 获取所有的窗口句柄
    handle_list = driver.window_handles
    # 切换
    driver.switch_to.window(handle_list[index])
    new_handle = driver.current_window_handle
    return new_handle

#下拉菜单的选择
def handle_select(select_element,style,value):
    '''
    下拉菜单的选择
    :param select_element: 通过定位拿到的select对象
    :param style: 下拉菜单选择方式
    :param value: 下拉选择框的数据
    :return: 成功返回1,不成功返回-1
    '''
    select = Select(select_element)
    if style == 'index':
        # 根据option索引来定位,从0开始
        select.select_by_index(value)
    elif style == 'value':
        # 根据option属性,value来定位
        select.select_by_value(value)
    elif style == 'text':
        # 根据option显示文本来定位
        select.select_by_visible_text(value)
    #操作成功返回1,不成功返回0方便做判断
    else:
        return 0
    return 1

# 滚动条向下滚动
def handle_scroll(driver,num):
    '''
    通过执行js代码实现浏览器的滚动条滚动
    :param num:滚动的像素
    '''
    js = f"var q=document.documentElement.scrollTop={num}"
    # js = "var q=document.getElementById('id').scrollTop={num}".format(num)
    driver.execute_script(js)

# app高级手势操作
class HandAppActionTool:
    @classmethod
    def back_prepage(cls,driver):
        '''
        app返回上一级
        :param driver: driver
        '''
        element = SeleniumTool.get_single_element(
            driver, By.XPATH, "//*[@content-desc='转到上一层级']")
        if element:
            element.click()

        else:
            print('----------->返回上一页失败,返回键定位不到')

    # app滑动,appium-python-client2.0后停用swipe
    # @classmethod
    # def handler_swipe(cls,driver, start_x, start_y, end_x, end_y,duration):
    #     '''
    #     app滑动
    #     :param driver:driver
    #     :param start_X: 起始位置
    #     :param start_y:起始位置
    #     :param end_x:结束位置
    #     :param end_y:结束位置
    #     :param duration:滑动时间/毫秒
    #     '''
    #     driver.swipe(start_x, start_y, end_x, end_y,duration)
        
    # app长按
    @classmethod
    def handler_long_press(cls, driver, location_x=None, location_y=None, element=None, press_time=1000):
        '''
        长按操作
        :param driver: driver对象
        :param location_x: 元素的横坐标
        :param location_y: 元素的纵坐标
        :param element: 要操作的元素
        :param press_time: 长按的时间,毫秒,默认是1000
        '''
        action = TouchAction(driver)
        if element:
            action.long_press(element=element, duration=press_time).release().perform()
        elif location_x is not None and location_y is not None:
            action.long_press(x=location_x, y=location_y, duration=press_time).release().perform()
        else:
            raise ValueError("请提供元素或位置坐标")
    
    # 轻敲
    @classmethod
    def handler_tap(cls, driver,element=None, location_x=None, location_y=None):
        '''
        轻敲操作
        :param driver: driver
        :param location_x: 元素的位置 x
        :param location_y: 元素的位置 y
        :param element: 元素对象
        '''
        action =  TouchAction(driver)
        if element:
            action.tap(element).perform()
        elif location_x and location_y:
            action.tap(x=location_x, y=location_y).perform()
        else:
            raise ValueError("请提供元素或位置坐标")

    # 长按移动/滑动
    @classmethod
    def handler_pressmove(cls, driver,target_x, target_y,duration=1000,element=None,start_x=None, start_y=None, ):
        '''
        长按移动,传入要移动的element对象或者坐标,以及要移到的坐标
        :param driver:driver
        :param duration:长按时间
        :param element:元素对象
        :param start_x:起始位置
        :param start_y:起始位置
        :param target_x:结束位置
        :param target_y:结束位置
        '''
        action = TouchAction(driver)
        if element:
            action.press(element).wait(duration).move_to(
                x=target_x, y=target_y).release().perform()
        elif start_x and start_y:
            action.press(x=start_x, y=start_y).wait(duration).move_to(
                x=target_x, y=target_y).release().perform()
        else:
            raise ValueError("请提供要移动的元素或位置坐标")

    # 一边滑动,一遍寻找目标元素
    @classmethod
    def swipe_find_element(cls,driver, element, style, value,direction='x'):
        '''
        对于元素的滑动寻找
        :param element: 容器元素
        :param style: 定位方法
        :param value: 定位规则
        :return:
        '''
        ele_size = element.size  # 获取元素大小
        width = ele_size["width"]  # 获取元素的宽度
        height = ele_size["height"]  # 获取元素的高度
        # 获了element元素左上角点的坐标
        ele_position = element.location
        x = ele_position["x"]  # 获取左上角点的x坐标值
        y = ele_position["y"]  # 获取左上角点的y坐标值
        if direction=='x':
            start_x = x + width * 0.9  # 获取的是起始点X的值
            start_y,end_y = y + height * 0.5  # 获取的是起始及终止点的Y的值
            end_x = x + width * 0.1  # 获取的是终止点X的值
        elif direction=='y':
            start_y = y + height * 0.9  # 获取的是起始点X的值
            start_x,end_x = x + width * 0.5  # 获取的是起始及终止点的Y的值
            end_y = y + height * 0.1  # 获取的是终止点X的值
        else:
            raise ValueError("请提供正确的滑动方向")
        i=1
        while True:
            page = driver.page_source  # 记录查找前的页面资源,通过对比页面资源来退出死循环
            ele=SeleniumTool.get_single_element(driver, style, value)
            if ele:
                return ele
            else:
                print(f"第{i}次循环,没有找到该元素！")    
                # 没有找到元素,那么滑屏后再对比并重新查找
                action = TouchAction(driver)
                action.press(start_x, start_y).move_to(end_x, end_y).release().perform()
                i+=1
                time.sleep(1)
                if page == driver.page_source:
                    print("滑屏操作完成且没有找到元素信息")
                    return False


# 安卓系统操作
class HandleSysTool:

    # 设置网络
    @classmethod
    def change_network(cls,driver, ntype=2):
        '''
         | Value (Alias)         |数据  | Wifi | 飞行模式       |
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
        :param ntype: 网络模式,默认是2
        :return:
        '''
        driver.set_network_connection(ntype)

    # 模拟键盘操作
    @classmethod
    def system_keys(cls,driver,num):
        '''
        模拟系统的操作
        HOME  3
        BACK  4
        ENTER  66
        :param num: 数值可查询,以上是常用的按键
        :return:
        '''
        driver.press_keycode(num)

    # 打开通知栏
    @classmethod
    def bulletin_board(cls,driver):
        driver.open_notifications()
    # 封装滑屏操作方法
    @classmethod
    def handler_swipe(cls,driver, direction:str, count:int=1):
        '''
        :param driver:driver
        :param direction:滑动方式 top/down/left/right
        :param count:滑动次数
        '''
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

#json数据处理使用utils的PytestParamData类的data_info方法
# class JsonTool:
#     @classmethod
#     def get_testcase_data(cls, file_path):
#         '''
#         实现读取外部数据,拼接成[(),(),()]
#         :return:  需要将拼接的数据做返回,让测试用例使用
#         '''
#         # 打开文件
#         file = open(file_path, encoding='utf-8')
#         # 读取文件
#         content = file.read()
#         # json.dumps()  # 将python数据类型转换成json字符串
#         content_list = json.loads(content)  # 将字符串还原成原始的列表或者字典
#         data_list = []
#         for item in content_list:
#             data = tuple(item.values())
#             data_list.append(data)
#         return data_list

class PicTool:
    # 获取toast信息
    def toast_info(driver, pic_path, left, upper, right, lower):
        '''
        获取toast消息,返回文本内容,配合使用
        :param pic_path: 获取的文件存储名,以png后缀
        :param left: 截取的部分距离左边的距离
        :param upper: 截取的部分距离上边的距离
        :param right: 截取的部分距离右边的距离
        :param lower: 距离的部分距离底部的距离
        :return: 返回页面上的数字
        '''
        #先通过定位方式找到 Toast 元素,如果找到则直接返回元素的文本内容
        common_login_element = SeleniumTool.get_single_element(driver, By.XPATH, "//android.widget.Toast")
        if common_login_element:
            return common_login_element.text
        #找不到就截图并对图片进行识别
        else:
            path = './img/login_toast_png/' + pic_path
            driver.get_screenshot_as_file(path)
            img = Image.open(path)
            new_img = img.crop((left, upper, right, lower))
            new_img.save(path)
            text = ''.join(pytesseract.image_to_string(
                Image.open(path), lang='chi_sim').split(' '))
            print('-------------->获取到的字符串是', text)
            if "!" in text:
                return text.replace('!', '！').strip()
            else:
                return text.strip()

    # 识别selenium的截图
    def get_target_pic(xmin: int, ymin: int, xmax: int, ymax: int, img_path: str, new_img_path: str, driver: object):
        '''
        当前函数用于使用selenium截图页面,进行截图使用
        :param xmin: 裁剪位置
        :param ymin: 裁剪位置
        :param xmax: 裁剪位置
        :param ymax: 裁剪位置
        :param img_path: 存储截图的路径
        :param new_img_path: 裁剪的图片的路径
        :return: 返回截取的图片所在的路径
        '''
        driver.get_screenshot_as_file(img_path)

        im = Image.open(img_path)  # 用PIL打开一个图片
        box = (xmin, ymin, xmax, ymax)  # box代表需要剪切图片的位置格式为:xmin ymin xmax ymax
        ng = im.crop(box)  # 对im进行裁剪 保存为ng(这里im保持不变)
        ng.save(new_img_path)
        return new_img_path

    #获取图片上的中文
    def pic_img(pic_path: str):
        '''
        获取图片上的中文
        :param pic_path: 图片路径
        :return: 返回图片上的文字
        '''
        # 读取图片
        image_obj = Image.open(pic_path)

        text = pytesseract.image_to_string(image_obj, lang='chi_sim')
        return text





