import pygame as pg
from src.Layer import Layer
from src.Brush import Brush


class _Frame:
    _layer = []
    _layerCount = 0

    def __init__(self, wid, hei):
        self.w = wid
        self.h = hei

    def AddLayer(self, layer: Layer):
        self._layer.append(layer)
        self._layerCount += 1

    def DeleteLayer(self, idx):
        if idx < 0 or idx >= self._layerCount:
            raise IndexError("DeleteLayer - number of layers doesn't match")
        if self._layerCount > 1:
            del self._layer[idx]
            self._layerCount -= 1
        else:
            raise ValueError("DeleteLayer - trial to delete last layer")

    def GetLayer(self, idx) -> Layer:
        if idx < 0 or idx >= self._layerCount:
            raise IndexError("GetLayer - number of layers doesn't match")
        return self._layer[idx]

    def GetSurface(self) -> pg.Surface:
        _surface = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        for _layer in self._layer:
            pg.surfarray.blit_array(_surface, _layer.GetArray())
        return _surface

    def LayerCount(self) -> int:
        return self._layerCount

    @staticmethod
    def Empty(wid, hei):
        _frame = _Frame(wid, hei)
        _frame.AddLayer(Layer.Empty(wid, hei))
        return _frame


class Sprite:
    _frame = []
    _currentFrame = 0
    _frameCount = 0
    _currentLayer = 0

    def __init__(self, wid, hei):
        self.w = wid
        self.h = hei

    def AddFrame(self, frame: _Frame):
        self._frame.append(frame)
        self._frameCount += 1
        if self._frameCount == 1:
            self.SetFrame(0)

    def GetSurface(self) -> pg.Surface:
        return self._CurrentFrame().GetSurface()

    def _CurrentFrame(self) -> _Frame:
        return self._frame[self._currentFrame]

    def CurrentLayer(self) -> Layer:
        return self._frame[self._currentFrame].GetLayer(self._currentLayer)

    def FrameCount(self) -> int:
        return self._frameCount

    def LayerCount(self) -> int:
        return self._CurrentFrame().LayerCount()

    def SetFrame(self, idx):
        if idx < 0 or idx > self._frameCount:
            raise IndexError("SetFrame - invalid index")
        self._currentFrame = idx
        if self.LayerCount() > self._currentLayer:
            self._currentLayer = self.LayerCount() - 1
        Brush.SetCurrentLayer(self.CurrentLayer())

    def SetLayer(self, idx):
        if idx < 0 or idx > self.LayerCount():
            raise IndexError("SetLayer - invalid index")
        self._currentLayer = idx
        Brush.SetCurrentLayer(self.CurrentLayer())

    @staticmethod
    def Empty(wid, hei, frameCount=1):
        _sprite = Sprite(wid, hei)
        for _ in range(frameCount):
            _sprite.AddFrame(_Frame.Empty(wid, hei))
        return _sprite

