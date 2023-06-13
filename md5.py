import hashlib


def secret_str(key:str,style:str='lower',count:int=32)->str:
    '''
    md5加密
    :param key: 要加密的数据
    :param style:加密后的数据大小写
    :param count:加密的位数
    :return: 加密后的md5值
    '''
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
