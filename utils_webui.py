from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def get_driver(driver_path='./libs/chromedriver.exe'):
    '''
    获取操作句柄
    :param driver_path: 浏览器驱动
    :return: driver
    '''
    driver = webdriver.Chrome(executable_path=driver_path)
    return driver

def get_element(driver,value,style=By.ID,*args,**kwargs):
    '''
    当前的方法，用于定位元素，如果存在元素，则返回，如果不存在，则返回空值
    :param driver: 操作句柄
    :param value: 定位语句
    :param style: 定位方式
    :param args:
    :param kwargs:
    :return: 元素或者None
    '''
    try:
        element = driver.find_element(by=style, value=value)
        return element
    except Exception as e:
        print('*********当前定位语句出现问题：',value,'*********')
        return None


def get_elements(driver,value,style=By.ID,*args,**kwargs):
    '''
    当前的方法，用于定位元素，如果存在元素，则返回元素列表，如果不存在，则返回空值
    :param driver: 操作句柄
    :param value: 定位语句
    :param style: 定位方式
    :param args:
    :param kwargs:
    :return: 多个元素或者None
    '''
    try:
        element = driver.find_elements(by=style, value=value)
        return element
    except Exception as e:
        print('*********当前定位语句出现问题：',value,'*********')
        return None


# alert弹窗
class HandleAlert:

    def __init__(self,driver):
        self.alert = driver.switch_to.alert

    def alert_info(self):
        return self.alert.text

    def alert_accept(self):
        self.alert.accept()

    def alert_dismiss(self):
        self.alert.dismiss()

# confirm
class HandleConfirm:

    def __init__(self, driver):
        self.alert = driver.switch_to.alert

    def alert_info(self):
        return self.alert.text

    def alert_accept(self):
        self.alert.accept()

    def alert_dismiss(self):
        self.alert.dismiss()


# prompt
class HandlePrompt:
    def __init__(self,driver):
        self.alert = driver.switch_to.alert

    def alert_info(self):
        return self.alert.text

    def alert_accept(self):
        self.alert.accept()

    def alert_dismiss(self):
        self.alert.dismiss()

    def alert_input_info(self,info):
        '''
        当前的方法，用于在prompt中输入数据
        :param info:
        :return:
        '''
        self.alert.send_keys(info)


# select下拉选择框
def handle_select(select_element,style,value):
    '''
    下拉菜单的选择
    :param select_element: 通过定位拿到的select对象
    :param style: 下拉菜单选择方式
    :param value: 下拉选择框的数据
    :return: 成功返回1，不成功返回-1
    '''
    select = Select(select_element)
    if style == 'index':
        # 根据option索引来定位，从0开始
        select.select_by_index(value)
    elif style == 'value':
        # 根据option属性，value来定位
        select.select_by_value(value)
    elif style == 'text':
        # 根据option显示文本来定位
        select.select_by_visible_text(value)
    else:
        return -1
    return 1


# 鼠标
class HandleActionChain:

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
        self.action.drag_and_drop(source,target).perform()

    # 悬停
    def move_element(self,element):
        self.action.move_to_element(element)
        self.action.perform()


# 键盘
class HandleKeys:

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

# 切换窗口
def switch_windows(driver,index):
    # 获取当前窗口的句柄
    current_handle = driver.current_window_handle
    # 获取所有的窗口句柄
    handle_list = driver.window_handles
    # 切换
    driver.switch_to.window(handle_list[index])
    new_handle = driver.current_window_handle
    return current_handle,new_handle


# 切换frame
class HandleIframe:

    def __init__(self,driver):
        self.driver = driver

    # 切入到iframe
    def switch_iframe(self,element):
        self.driver.switch_to.frame(element)

    # 切回原始页面
    def back_page(self):
        self.driver.switch_to.default_content()


# 滚动条向下滚动
def handle_scroll(driver,num):
    js = "var q=document.documentElement.scrollTop={}".format(num)
    # js = "var q=document.getElementById('id').scrollTop={num}".format(num)
    driver.execute_script(js)


if __name__ == '__main__':
    pass







