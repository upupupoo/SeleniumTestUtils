import requests
import ddddocr
from selenium import webdriver

login_url=''
login_api=''
code_api=''

#实例化session
session=requests.session()

#实例化ocr
ocr = ddddocr.DdddOcr()

#设置在driver关闭后，浏览器仍不会被关闭
option=webdriver.ChromeOptions()
option.add_experimental_option('detach',True)
driver=webdriver.Chrome(options=option)

#先用selenium进入登录页
driver.get(login_url)

#请求验证码接口
get_code=session.get(code_api)

#识别出验证码
code = ocr.classification(get_code.content)

#构造请求的数据
data={
    'userName':'',
    'password':'',
    'code':code
    }
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

#请求登录接口
res=session.post(login_api,data=data,headers=HEADERS)

#获取cookies
cookies=session.cookies.get_dict()

#获取到cookies中指定的session值
sess_value = cookies.get('JSESSIONID')

#回到selenium，删除所有cookies
driver.delete_all_cookies()

#构造cookies
cookies={
    'name': 'JSESSIONID',
    "value": sess_value
}

#添加cookies
driver.add_cookie(cookie_dict=cookies)

#重新访问url,等待自动跳转
driver.get(login_url)