import hashlib


def secret_str(key,style='de',count=32):
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
    elif style == 'de' and count == 32:
        return (target_str.hexdigest())
    elif style == 'de' and count == 16:
        return (target_str.hexdigest())[8:-8]
    else:
        return None





if __name__ == '__main__':
    print(secret_str('asd123','lower',32))
    print(secret_str('asd123','upper',32))