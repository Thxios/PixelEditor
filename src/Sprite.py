from src.lib import *
from src.Layer import Layer
from src.Brush import Brush


class Frame:
    _layer: List[Layer]
    _layerCount = 0

    surface = pg.Surface

    def __init__(self, wid, hei):
        self.w = wid
        self.h = hei
        self.surface = pg.Surface((wid, hei), pg.SRCALPHA, 32)
        self._layer = []

    def AddLayer(self, layer: Layer):
        self._layer.append(layer)
        self._layerCount += 1

    def AddLayerEmpty(self, name=None):
        if name is None:
            name = 'Layer ' + str(self._layerCount)
        _layer = Layer.Empty(self.w, self.h, name)
        self.AddLayer(_layer)

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
        self.surface.fill((0, 0, 0, 0))
        for i in range(self._layerCount - 1, -1, -1):
            if self._layer[i].visible:
                self.surface.blit(self._layer[i].GetSurface(), (0, 0))
        return self.surface

    def GetLayerName(self) -> List[str]:
        _name = []
        for _layer in self._layer:
            _name.append(_layer.name)
        return _name

    def LayerCount(self) -> int:
        return self._layerCount

    @staticmethod
    def Empty(wid, hei):
        _frame = Frame(wid, hei)
        _frame.AddLayer(Layer.Empty(wid, hei, 'Layer 0'))
        return _frame


class Sprite:
    surface: pg.Surface

    _frame: List[Frame] = []
    _currentFrame: int = 0
    _frameCount: int = 0
    _currentLayer: int = 0

    def __init__(self, wid, hei):
        self.w = wid
        self.h = hei

    def AddFrame(self, frame: Frame):
        self._frame.append(frame)
        self._frameCount += 1
        if self._frameCount == 1:
            self.SetFrame(0)

    def GetSurface(self) -> pg.Surface:
        if self.CurrentLayer().IsChanged():
            self.surface = self.CurrentFrame().GetSurface()
            self.CurrentLayer().Applied()
        return self.surface

    def SetCurrentLayer(self, idx):
        self._currentLayer = idx
        Brush.SetCurrentLayer(self.CurrentFrame().GetLayer(idx))

    def CurrentFrame(self) -> Frame:
        return self._frame[self._currentFrame]

    def CurrentLayer(self) -> Layer:
        return self._frame[self._currentFrame].GetLayer(self._currentLayer)

    def FrameCount(self) -> int:
        return self._frameCount

    def LayerCount(self) -> int:
        return self.CurrentFrame().LayerCount()

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
            _sprite.AddFrame(Frame.Empty(wid, hei))
        return _sprite


Sprite = Sprite.Empty(64, 64)
Sprite.CurrentFrame().AddLayerEmpty()
Sprite.CurrentFrame().AddLayerEmpty()
Sprite.CurrentFrame().AddLayerEmpty()

