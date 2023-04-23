import requests
import sys
import ddddocr
sys.path.append("..")
sys.path.append("./utils")

def get_code(req,url,type='auto'):
    
    code=req.get(url)
    ocr = ddddocr.DdddOcr()
    with open('data/code.jpg', 'wb') as f:
        f.write(code.content)
    with open('data/code.jpg', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    #https://www.bbiquge.net网站验证码二次处理
    # res=res.replace('日','8',4).replace('口','0',4).replace('己','2',4).replace('d','0',4)
    if type=='auto':
        return req,res
    elif type=='hand':
        a=input('输入验证码：')
        return req,res