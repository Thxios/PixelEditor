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

        self.visible = True

    def __str__(self):
        return str(self._pixel.T)

    def Clear(self):
        self._pixel = np.zeros((self.w, self.h))
        self.Changed()

    def SetPixel(self, x, y, color):
        if self._pixel[x][y] != utility.RGBA2INT(color):
            self._pixel[x][y] = utility.RGBA2INT(color)
            self.Changed()

    def BrushDown(self, x, y, brush: np.ndarray, color):
        _brushWidth, _brushHeight = brush.shape
        xs, ys = x - _brushWidth // 2, y - _brushHeight // 2
        xe, ye = xs + _brushWidth, ys + _brushHeight
        # xe, ye = x + _brushWidth // 2, y + _brushHeight // 2
        # xs, ys = xe - _brushWidth, ye - _brushHeight
        # print((xs, xe), (ys, ye))
        # _destArrXs, _destArrXe = max(xs, 0), min(xe, self.w)
        # _destArrYs, _destArrYe = max(ys, 0), min(ye, self.h)
        # print((_destArrXs, _destArrXe), (_destArrYs, _destArrYe))
        _destArr = self._pixel[max(xs, 0): min(xe, self.w), max(ys, 0): min(ye, self.h)]
        # print(_destArr.shape)

        # print(brush)
        _destBrush = brush[max(-xs, 0): min(_brushWidth - xe + self.w, _brushWidth),
                           max(-ys, 0): min(_brushHeight - ye + self.h, _brushHeight)]

        _destArr -= _destBrush * _destArr
        _destArr += _destBrush * utility.RGBA2INT(color)
        # print(_destArr)
        self.Changed()

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
            self.Changed()

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
        return self._surface.copy()

    def GetArray(self) -> np.ndarray:
        return self._pixel

    def IsChanged(self):
        return self._hasChange

    def Applied(self):
        self._hasChange = False

    def Changed(self):
        self._hasChange = True

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
