from time import time


def RGBA2INT(color):
    if len(color) == 4:
        _r, _g, _b, _a = color
    else:
        _r, _g, _b = color
        _a = 255
    _c = _b + 256 * _g + 256 ** 2 * _r + 256 ** 3 * _a
    return _c

def INT2RGBA(color):
    _b = color % 256
    _g = color // 256 % 256
    _r = color // (256 ** 2) % 256
    _a = color // (256 ** 3) % 256
    return _r, _g, _b, _a


t = 0
def TimerStart():
    global t
    t = time()

def TimerEnd():
    d = time() - t
    print(d, 's')
