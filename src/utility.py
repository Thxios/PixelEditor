import colorsys
import os
import sys
from time import time


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def RGBA2INT(color: (int, int, int, int)) -> int:
    if len(color) == 4:
        _r, _g, _b, _a = color
    else:
        _r, _g, _b = color
        _a = 255
    _c = _b + 256 * _g + 256 ** 2 * _r + 256 ** 3 * _a
    return _c

def INT2RGBA(color: int) -> (int, int, int, int):
    _b = color % 256
    _g = color // 256 % 256
    _r = color // (256 ** 2) % 256
    _a = color // (256 ** 3) % 256
    return _r, _g, _b, _a


def RGB2HSV(color: (int, int, int)) -> (float, float, float):
    _r, _g, _b = color
    _h, _s, _v = colorsys.rgb_to_hsv(_r / 255, _g / 255, _b / 255)
    return _h * 360, _s * 100, _v * 100


def HSV2RGB(color: (float, float, float)) -> (int, int, int):
    _h, _s, _v = color
    _r, _g, _b = colorsys.hsv_to_rgb(_h / 360, _s / 100, _v / 100)
    return round(_r * 255), round(_g * 255), round(_b * 255)


t = 0
def TimerStart():
    global t
    t = time()

def TimerEnd():
    d = time() - t
    print(d, 's')

