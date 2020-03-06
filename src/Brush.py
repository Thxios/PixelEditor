import pygame as pg
from src.Layer import Layer


class _Brush:
    currentColor = (0, 0, 0, 0)

    def OnMouseDown(self, clickedPixel, layer: Layer):
        pass

    def OnMouseDrag(self, clickedPixel, layer: Layer):
        pass

    def OnMouseUp(self, clickedPixel, layer: Layer):
        pass

    def SetCurrentColor(self, color):
        self.currentColor = color


class _PencilBrush(_Brush):
    def OnMouseDown(self, clickedPixel, layer: Layer):
        layer.SetPixel(*clickedPixel, self.currentColor)

    def OnMouseDrag(self, clickedPixel, layer: Layer):
        layer.SetPixel(*clickedPixel, self.currentColor)


class _EraserBrush(_Brush):
    def OnMouseDown(self, clickedPixel, layer: Layer):
        layer.SetPixel(*clickedPixel, self.currentColor)

    def OnMouseDrag(self, clickedPixel, layer: Layer):
        layer.SetPixel(*clickedPixel, self.currentColor)


class _FloodBrush(_Brush):
    def OnMouseDown(self, clickedPixel, layer: Layer):
        pass


class _PickerBrush(_Brush):
    def OnMouseDown(self, clickedPixel, layer: Layer) -> (int, int, int, int):
        self.currentColor = layer.GetPixel(*clickedPixel)
        return self.currentColor


class Brush:
    _layer = None

    pencil = _PencilBrush()
    eraser = _EraserBrush()
    flood = _FloodBrush()
    picker = _PickerBrush()

    _currentBrush: _Brush

    def OnMouseDown(self, clickedPixel):
        self._currentBrush.OnMouseDown(clickedPixel, self._layer)

    def OnMouseDrag(self, clickedPixel):
        self._currentBrush.OnMouseDrag(clickedPixel, self._layer)

    def OnMouseUp(self, clickedPixel):
        self._currentBrush.OnMouseUp(clickedPixel, self._layer)

    def SetBrush(self, brush):
        if brush == 'Pencil' or brush == 0:
            self._currentBrush = self.pencil
        elif brush == 'Eraser' or brush == 1:
            self._currentBrush = self.eraser
        elif brush == 'Flood' or brush == 2:
            self._currentBrush = self.flood
        elif brush == 'Picker' or brush == 3:
            self._currentBrush = self.picker

    def SetCurrentLayer(self, layer: Layer):
        self._layer = layer


Brush = Brush()
