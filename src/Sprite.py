import pygame as pg
from src.Layer import Layer


class Frame:
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

    def GetLayer(self, idx):
        if idx < 0 or idx >= self._layerCount:
            raise IndexError("GetLayer - number of layers doesn't match")
        return self._layer[idx]

    def LayerCount(self):
        return self._layerCount

    @staticmethod
    def Empty(wid, hei):
        _frame = Frame(wid, hei)
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

    def AddFrame(self, frame: Frame):
        self._frame.append(frame)
        self._frameCount += 1

    def CurrentFrame(self):
        return self._frame[self._currentFrame]

    def CurrentLayer(self):
        return self._frame[self._currentFrame].GetLayer(self._currentLayer)

    def FrameCount(self):
        return self._frameCount

    @staticmethod
    def Empty(wid, hei, frameCount=1):
        _sprite = Sprite(wid, hei)
        for _ in range(frameCount):
            _sprite.AddFrame(Frame.Empty(wid, hei))
        return _sprite

