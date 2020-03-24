from src.lib import *
from src import utility
import colorsys


class Color:
    _r: int
    _g: int
    _b: int
    _a: int

    _h: float
    _s: float
    _v: float

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

    @property
    def alpha(self):
        return self._a

    @alpha.setter
    def alpha(self, alpha):
        if alpha > 255 or alpha < 0:
            raise ValueError('alpha get ' + str(alpha))
        self._a = alpha

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

    @staticmethod
    def RGB(r, g, b, a=255):
        _color = Color()
        _color.rgba = (r, g, b, a)
        return _color

    @staticmethod
    def HSV(h, s, v):
        _color = Color()
        _color.hsv = (h, s, v)
        return _color


