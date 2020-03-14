from src.lib import *
from src import utility


class Layer:
    def __init__(self, wid, hei, name, color=None):
        self.w = wid
        self.h = hei
        self.resolution = (self.w, self.h)
        self._surface = pg.Surface((wid, hei), pg.SRCALPHA, 32)
        self._hasChange = True
        self.name = name

        if color is not None:
            self._surface.fill(color)
        self._pixel = pg.surfarray.pixels2d(self._surface)

    def __str__(self):
        return str(self._pixel.T)

    def Clear(self):
        self._pixel = np.zeros((self.w, self.h))
        self._hasChange = True

    def SetPixel(self, x, y, color):
        if self._pixel[x][y] != utility.RGBA2INT(color):
            self._pixel[x][y] = utility.RGBA2INT(color)
            self._hasChange = True

    def GetPixel(self, x, y) -> (int, int, int, int):
        return utility.INT2RGBA(self._pixel[x][y])

    def SetName(self, name):
        self.name = name

    def Paste(self, x, y, layer):
        if isinstance(layer, Layer):
            xs, ys = max(x, 0), max(y, 0)
            xe, ye = min(self.w, x + layer.w), min(self.h, y + layer.h)
            crop_xs, crop_ys = max(-x, 0), max(-y, 0)
            crop_xe, crop_ye = min(self.w - x, layer.w), min(self.h - y, layer.h)

            self._pixel[xs:xe, ys:ye] = layer._pixel[crop_xs:crop_xe, crop_ys:crop_ye]
            self._hasChange = True

    def CropLayer(self, xRange, yRange):
        _xs, _xe = xRange
        _ys, _ye = yRange
        _xs, _xe = max(_xs, 0), min(_xe, self.w)
        _ys, _ye = max(_ys, 0), min(_ye, self.h)
        _w, _h = _xe - _xs, _ye - _ys
        _layer = Layer(_w, _h, '')
        _layer._pixel = self._pixel[_xs:_xe, _ys:_ye]
        return _layer

    def GetSurface(self) -> pg.Surface:
        return self._surface

    def GetArray(self) -> np.ndarray:
        return self._pixel

    def IsChanged(self):
        return self._hasChange

    def Applied(self):
        self._hasChange = False

    @staticmethod
    def FromArray(array: np.ndarray, name):
        try:
            _w, _h = array.shape
        except ValueError:
            return None
        _layer = Layer(_w, _h, name)
        _layer._surface = pg.surfarray.make_surface(array)
        _layer._pixel = pg.surfarray.pixels2d(_layer._surface)
        return _layer

    @staticmethod
    def FromSurface(surface: pg.Surface, name):
        _w, _h = surface.get_size()
        _layer = Layer(_w, _h, name)
        _layer._surface = surface
        _layer._pixel = pg.surfarray.pixels2d(surface)
        return _layer

    @staticmethod
    def Empty(wid, hei, name):
        return Layer(wid, hei, name)

    @staticmethod
    def Solid(wid, hei, color, name):
        return Layer(wid, hei, color, name)

