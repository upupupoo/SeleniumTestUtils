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


class SeleniumTool():
    #获取单个元素
    def get_element(self,style, value):
        '''
        定位app中的元素
        :param style: 定位元素的方式
        :param value:方式对应的值
        :return: 将元素进行返回
        '''
        try:
            element = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element(style, value))
            return element
        except Exception as e:
            print('-------------------->定位不到元素,出错的语句是', value)
            element = None
            return element
    #获取element组
    def get_elements(self,style, value):
        '''
        获取多个元素
        :param style:
        :param value:
        :return: 返回的是多个元素组成的列表
        '''
        try:
            element = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_elements(style, value))
            return element
        except Exception as e:
            print('-------------------->定位不到元素,出错的语句是', value)
            element = None
            return element
    #文本框输入
    def input_text(self, element, data):
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
    #点击元素
    def click_element(self, element):
        '''
        点击元素
        :param element: 元素
        '''
        if element:
            element.click()
        else:
            print('------------------------->当前元素未获取')

# helium处理
class HeliumTool():
    def __init__(self,driver) -> None:
        set_driver(driver)
        


    # helium定位单个元素
    def get_element(self,widget, value, **local):
        '''
        定位app中的元素
        :param widget:定位方式(S,Text,Link,ListItem,Button,Image,TextField,ComboBox,CheckBox,RadioButton)
        :param value: 定位方式对应的值
        :param local: 可选的位置参数(above,below,to_right_of,to_left_of)
        :return: 将元素进行返回
        '''
        try:
            # @ 对应name
            # . 对应class
            # # 对应id
            # //对应xpath或者css selector
            if widget in ['s','S']:
                element = S(value, **local)
            #文本控件定位
            #可使用.value获取元素的文本
            elif widget in ['text','Text']:
                element = Text(value, **local)
            #链接控件定位
            #可使用.herf获取元素的url    
            elif widget in ['link','Link']:
                element = Link(value, **local)
            #序列控件定位
            elif widget in ['ListItem','listitem']:
                element = ListItem(value, **local)
            #按钮控件定位
            #可使用.is_enabled()判断按钮是否选中
            elif widget in ['button','Button']:
                element = Button(value, **local)
            #图片控件定位
            elif widget in ['image','Image']:
                element = Image(value, **local)
            #文本框控件定位
            #可使用.is_enabled()判断文本框不可选中不可编辑
            #可使用.is_editable()判断文本框可选中不可编辑
            elif widget in ['TextField','textfield']:
                element = TextField(value, **local)
            #下拉列表控件定位
            #可使用.value获取已选中的值
            #使用.option获取所有可以选择的内容
            #使用is_editable()方法判断下拉框是否可以通过搜索匹配下拉内容
            elif widget in ['ComboBox','combobox']:
                element = ComboBox(value, **local)
            #复选框控件定位
            #可使用.is_enabled()判断是否可交互
            #可使用.is_checked()判断是否选中
            elif widget in ['CheckBox','checkbox']:
                element = CheckBox(value, **local)
            #单选框控件定位
            #可使用.is_selected()判断是否选中
            elif widget in ['RadioButton','radiobutton']:
                element = RadioButton(value, **local)
            return element
        except Exception as e:
            print('-------------------->定位不到元素,出错的语句是',widget,value)
    #helium定位多个元素
    def get_elements(self,widget,value,**local):
        return find_all(self.get_element(widget,value,**local))
    #helium点击元素click(element)
    #helium双击doubleclick(element)
    #helium右击rightclick(element)
    #helium悬浮hover(element)
    #helium輸入write(value, element)
    #helium上传文件attach_file(filepath,to=text)
    #helium下拉框选择select(combo_box,value)
    #刷新页面 refresh()
    #隐式等待Config.implicit_wait_secs(10)
    #将helium的element转为selenium的element,elment.web_element
    #创建坐标点对象Point(x,y),__add__和__sub__进行坐标点的加减
    #关闭浏览器 kill_browser()
    #高亮某一元素 highlight(element)
    
    
    #helium获取元素属性
    def get_ele_attribute(self,element, att):
        '''
        获取元素的属性
        :param element:要获取属性的元素
        :param element:要获取的属性
        :return:获取属性的值
        '''
        html_att=['x','y','top_left','width','height']
        if att == 'text':
            return element.web_element.text
        elif att in html_att:
            return getattr(element,att,None)
        else:
            return element.web_element.get_attribute(att)

    #helium拖拽
    def drag_drop(self,value,to,type=1):
        if type:
            drag(value, to)
        else:
            drag_file(value, to)
    
    #helium切换窗口
    #windows().handle获取当前窗口的selenium句柄
    def switch_windows(self,value):
        if  type(value)==int:
            switch_to(find_all(Window())[value])
        else:
            switch_to(Window(value))
    
    #按住/松开鼠标左键
    def press_mouse_left(element,type=1):
        if type:
            press_mouse_on(element)
        else:
            release_mouse_over(element)
    
    #滚动屏幕
    def scroll(self,type,px=100):
        if type=='up':
            scroll_up(px)
        elif type=='down':
            scroll_down(px)
        elif type=='left':
            scroll_left(px)
        elif type=='right':
            scroll_right(px)
        else:
            scroll_down(px)
                
            

            
class AppTool(SeleniumTool):
    # app操作driver
    def __init__(self,app_pack='com.android.launcher3', appact= '.launcher3.Launcher'):
        self.app_pack=app_pack
        self.appact=appact
        self.driver = None
    def get_driver(self):
        '''
        app获取driver
        :param app_pack: app包名
        :param appact:Activity名
        :return: driver
        '''
        desired_caps = dict(
            platformName='Android',  # 平台,是Android还是IOS
            platformVersion='9',  # 安卓的版本
            deviceName='emulator-5554',
            automationName='uiautomator2',
            # 包名
            appPackage=self.app_pack,
            # 界面名
            appActivity=self.appact
        )
        self.driver = appdriver.Remote(
            'http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
        self.action = TouchAction(self.driver)
        return self.driver
    def close_driver(self):
        '''
        退出driver
        '''
        self.driver.close()
        self.driver=None
    
    
    #返回上一级
    def back_prepage(self):
        '''
        app返回上一级
        '''
        try:
            element = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element(By.XPATH, "//*[@content-desc='转到上一层级']"))
        except Exception as e:
            print('----------->返回上一页失败,返回键定位不到')
            element = None
        element.click()
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
    def handler_long_press(self,location_x=None, location_y=None, element=None, press_time=1000):
        '''
        长按操作
        :param location_x: 元素的横坐标
        :param location_y: 元素的纵坐标
        :param element: 要操作的元素
        :param press_time: 长按的时间,毫秒,默认是1000
        '''
        action = TouchAction(self)
        if element:
            action.long_press(element=element, duration=press_time).release().perform()
        elif location_x is not None and location_y is not None:
            action.long_press(x=location_x, y=location_y, duration=press_time).release().perform()
        else:
            raise ValueError("请提供元素或位置坐标")
    # 轻敲
    def handler_tap(self,element=None, location_x=None, location_y=None):
        '''
        轻敲操作
        :param location_x: 元素的位置 x
        :param location_y: 元素的位置 y
        :param element: 元素对象
        '''
        action =  TouchAction(self.driver)
        if element:
            action.tap(element).perform()
        elif location_x and location_y:
            action.tap(x=location_x, y=location_y).perform()
        else:
            raise ValueError("请提供元素或位置坐标")
    # 长按移动/滑动
    def handler_pressmove(self,target_x, target_y,duration=1000,element=None,start_x=None, start_y=None, ):
        '''
        长按移动,传入要移动的element对象或者坐标,以及要移到的坐标
        :param duration:长按时间
        :param element:元素对象
        :param start_x:起始位置
        :param start_y:起始位置
        :param target_x:结束位置
        :param target_y:结束位置
        '''
        action = TouchAction(self.driver)
        if element:
            action.press(element).wait(duration).move_to(
                x=target_x, y=target_y).release().perform()
        elif start_x and start_y:
            action.press(x=start_x, y=start_y).wait(duration).move_to(
                x=target_x, y=target_y).release().perform()
        else:
            raise ValueError("请提供要移动的元素或位置坐标")
    # 一边滑动,一遍寻找目标元素
    def swipe_find_element(self, element, style, value,direction='x'):
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
            page = self.driver.page_source  # 记录查找前的页面资源,通过对比页面资源来退出死循环
            element=self.get_single_element(self.driver, style, value)
            if element:
                return element
            else:
                print(f"第{i}次循环,没有找到该元素！")    
                # 没有找到元素,那么滑屏后再对比并重新查找
                self.action.press(start_x, start_y).move_to(end_x, end_y).release().perform()
                i+=1
                time.sleep(1)
                if page == self.driver.page_source:
                    print("滑屏操作完成且没有找到元素信息")
                    return False
  
  
  
    # 设置网络
    def change_network(self,ntype=2):
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
        self.driver.set_network_connection(ntype)

    # 模拟键盘操作
    def system_keys(self,num):
        '''
        模拟系统的操作
        HOME  3
        BACK  4
        ENTER  66
        :param num: 数值可查询,以上是常用的按键
        :return:
        '''
        self.driver.press_keycode(num)

    # 打开通知栏
    def bulletin_board(self):
        self.driver.open_notifications()
    # 封装滑屏操作方法
    def handler_swipe(self, direction:str, count:int=1):
        '''
        :param driver:driver
        :param direction:滑动方式 top/down/left/right
        :param count:滑动次数
        '''
        w = self.driver.get_window_size()["width"]  # 获取手机屏幕的宽度
        h = self.driver.get_window_size()["height"]  # 获取手机屏幕的高度
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
            self.driver.swipe(*zb, duration=1200)
            time.sleep(1)
            
            
            
            

# selenium处理
class WebTool(SeleniumTool):
    #初始化driver路径
    def __init__(self, path):
        self.chromedriver_path = path
        self.driver = None
        self.action = None
    #根据配置创建driver
    def create_driver(self) -> webdriver:
        '''
        创建driver
        :return:driver
        '''
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
        self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=self.chromedriver_path)
        self.action=ActionChains(self.driver)
        return self.driver
    #关闭并初始化driver
    def close_driver(self):
        '''
        退出driver
        '''
        self.driver.close()
        self.driver=None
        
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

        
    # 鼠标右击
    def right_click(self,element):
        self.action.context_click(element)
        self.action.perform()  
    # 鼠标悬浮
    def move_element(self,element):
        self.action.move_to_element(element)
        self.action.perform()  
    # 鼠标双击
    def twice_click(self,element):
        self.action.double_click(element)
        self.action.perform()
    # 鼠标拖拽
    def drag_drop(self,source,target):
        '''
        :param source:要拖动的元素
        :param target:目标元素
        '''
        self.action.drag_and_drop(source,target).perform()




    # 删除键
    def delete_key(element):
        element.send_keys(Keys.BACK_SPACE)
    # 全选
    def all_choose(element):
        element.send_keys(Keys.CONTROL,'a')
    # 复制
    def ctrl_c(element):
        element.send_keys(Keys.CONTROL, 'c')
    # 粘贴
    def ctrl_v(element):
        element.send_keys(Keys.CONTROL, 'v')
    # 回车
    def enter(element):
        element.send_keys(Keys.ENTER)
    
    
    #切换到alert/confirm/prompt
    def switch_alert(self, driver):
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



    # 切入到iframe
    def switch_iframe(self,element):
        self.driver.switch_to.frame(element)
    # 切回原始页面
    def back_page(self):
        self.driver.switch_to.default_content()
    #切换浏览器窗口
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

    # 滚动条向下滚动
    def handle_scroll(self,num):
        '''
        通过执行js代码实现浏览器的滚动条滚动
        :param num:滚动的像素
        '''
        js = f"var q=document.documentElement.scrollTop={num}"
        # js = "var q=document.getElementById('id').scrollTop={num}".format(num)
        self.driver.execute_script(js)



    

# 获取app的toast信息
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








