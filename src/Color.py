from src.lib import *
from src import utility
import colorsys


class Color:
    def __init__(self, r, g, b, a=255):
        self._r = r
        self._g = g
        self._b = b
        self._a = a

        self._h, self._s, self._v = Color.RGB2HSV((r, g, b))

    @property
    def rgb(self) -> (int, int, int):
        return self._r, self._g, self._b

    @rgb.setter
    def rgb(self, rgb: (int, int, int)):
        self._r, self._g, self._b = rgb
        self._h, self._s, self._v = Color.RGB2HSV(self.rgb)

    @property
    def rgba(self) -> (int, int, int, int):
        return self._r, self._g, self._b, self._a

    @rgba.setter
    def rgba(self, rgba: (int, int, int, int)):
        self._r, self._g, self._b, self._a = rgba
        self._h, self._s, self._v = Color.RGB2HSV(self.rgb)

    @property
    def hsv(self) -> (float, float, float):
        return self._h, self._s, self._v

    @hsv.setter
    def hsv(self, hsv: (float, float, float)):
        self._h, self._s, self._v = hsv
        self._r, self._g, self._b = Color.HSV2RGB(self.hsv)

    @staticmethod
    def RGB2HSV(rgb: (int, int, int)) -> (float, float, float):
        r, g, b = rgb
        _h, _s, _v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        return _h * 360, _s * 100, _v * 100

    @staticmethod
    def HSV2RGB(hsv: (float, float, float)) -> (int, int, int):
        _h, _s, _v = hsv
        if _h < 0:
            raise TypeError('Hue value is invalid')
        _r, _g, _b = colorsys.hsv_to_rgb(_h / 360, _s / 100, _v / 100)
        return round(_r * 255), round(_g * 255), round(_b * 255)


