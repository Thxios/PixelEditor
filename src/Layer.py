import numpy as np
import pygame as pg
from src import utility


class Layer:
    def __init__(self, wid, hei, color=None):
        self.w = wid
        self.h = hei
        self.resolution = (self.w, self.h)
        self._surface = pg.Surface((wid, hei), pg.SRCALPHA, 32)

        if color is not None:
            self._surface.fill(color)
        self._pixel = pg.surfarray.pixels2d(self._surface)
        # _color = utility.RGBA2INT(color)
        # self._pixel = np.array([
        #     [_color for _ in range(self.h)] for _ in range(self.w)
        # ])

    def __str__(self):
        return str(self._pixel.T)

    def Clear(self):
        self._pixel = np.zeros((self.w, self.h))

    def SetPixel(self, x, y, color):
        self._pixel[x][y] = utility.RGBA2INT(color)

    def GetPixel(self, x, y):
        return utility.INT2RGBA(self._pixel[x][y])

    def Paste(self, x, y, layer):
        if isinstance(layer, Layer):
            xs, ys = max(x, 0), max(y, 0)
            xe, ye = min(self.w, x + layer.w), min(self.h, y + layer.h)
            crop_xs, crop_ys = max(-x, 0), max(-y, 0)
            crop_xe, crop_ye = min(self.w - x, layer.w), min(self.h - y, layer.h)

            self._pixel[xs:xe, ys:ye] = layer._pixel[crop_xs:crop_xe, crop_ys:crop_ye]

    def Crop(self, xRange, yRange):
        _xs, _xe = xRange
        _ys, _ye = yRange
        _xs, _xe = max(_xs, 0), min(_xe, self.w)
        _ys, _ye = max(_ys, 0), min(_ye, self.h)
        _w, _h = _xe - _xs, _ye - _ys
        _layer = Layer(_w, _h)
        _layer._pixel = self._pixel[_xs:_xe, _ys:_ye]
        return _layer

    def GetSurface(self):
        return self._surface

    def GetArray(self):
        return self._pixel

    @staticmethod
    def FromArray(array):
        if isinstance(array, np.ndarray):
            _w, _h = array.shape
            _layer = Layer(_w, _h)
            _layer._surface = pg.surfarray.make_surface(array)
            _layer._pixel = pg.surfarray.pixels2d(_layer._surface)
            return _layer

    @staticmethod
    def FromSurface(surface):
        if isinstance(surface, pg.Surface):
            _w, _h = surface.get_size()
            _layer = Layer(_w, _h)
            _layer._surface = surface
            _layer._pixel = pg.surfarray.pixels2d(surface)
            return _layer


if __name__ == '__main__':
    a = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ])
    b = np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
    ])

    aa = Layer.FromArray(a)
    bb = Layer.FromArray(b)
    print(aa)
    print(bb)
    aa.Paste(1, 2, bb)
    print(aa)
