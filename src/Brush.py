import pygame as pg
from src.Layer import Layer


class Brush:
    currentColor = (0, 0, 0, 0)

    _layer = None

    def OnMouseDown(self, clickedPixel):
        raise NotImplementedError

    def OnDrag(self):
        pass

    def OnMouseDrag(self, clickedPixel):
        pass

    def SetCurrentLayer(self, layer):
        if isinstance(layer, Layer):
            self._layer = layer

    def SetCurrentColor(self, color):
        self.currentColor = color


class PencilBrush(Brush):
    def OnMouseDown(self, clickedPixel):
        self._layer.SetPixel(*clickedPixel, self.currentColor)

    def OnMouseDrag(self, clickedPixel):
        self._layer.SetPixel(*clickedPixel, self.currentColor)


class PickerBrush(Brush):
    def OnMouseDown(self, clickedPixel):
        self.currentColor = self._layer.GetPixel(*clickedPixel)
        return self.currentColor


class FloodBrush(Brush):
    def OnMouseDown(self, clickedPixel):
        pass


PencilBrush = PencilBrush()
FloodBrush = FloodBrush()
