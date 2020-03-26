from src.lib import *
from src.Layer import Layer


_pencil = 0
_eraser = 1
_flood = 2
_picker = 3


class _Brush:
    currentColor = (0, 0, 0, 0)

    def OnMouseDown(self, clickedPixel, layer: Layer):
        pass

    def OnMouseDrag(self, clickedPixel, layer: Layer):
        pass

    def OnMouseUp(self, clickedPixel, layer: Layer):
        pass

    def SetCurrentColor(self, color):
        if len(color) == 3:
            _r, _g, _b = color
            _a = 255
        else:
            _r, _g, _b, _a = color
        self.currentColor = (_r, _g, _b, _a)


class _PencilBrush(_Brush):

    # ----- for test -----
    brush = [
        np.array([
            [1],
        ], dtype=np.uint32).T,
        np.array([
            [1, 1],
            [1, 1],
        ], dtype=np.uint32).T,
        np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ], dtype=np.uint32).T,
        np.array([
            [0, 1, 1, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 1, 1, 0],
        ], dtype=np.uint32).T,
        np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
        ], dtype=np.uint32).T,
    ]

    brushSize = 4

    def OnMouseDown(self, clickedPixel, layer: Layer):
        # layer.SetPixel(*clickedPixel, self.currentColor)
        layer.BrushDown(*clickedPixel, self.brush[self.brushSize], self.currentColor)


class _EraserBrush(_Brush):

    # ----- for test -----
    brush = [
        np.array([
            [1],
        ], dtype=np.uint32).T,
        np.array([
            [1, 1],
            [1, 1],
        ], dtype=np.uint32).T,
        np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ], dtype=np.uint32).T,
        np.array([
            [0, 1, 1, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 1, 1, 0],
        ], dtype=np.uint32).T,
        np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
        ], dtype=np.uint32).T,
    ]

    brushSize = 4


    def OnMouseDown(self, clickedPixel, layer: Layer):
        layer.BrushDown(*clickedPixel, self.brush[self.brushSize], self.currentColor)

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
    _layer: Layer

    pencil = _PencilBrush()
    eraser = _EraserBrush()
    flood = _FloodBrush()
    picker = _PickerBrush()

    _currentBrush: _Brush
    currentBrushIdx: int

    def __init__(self):
        self.SetBrush('Pencil')

    def OnMouseDown(self, clickedPixel):
        # self._currentBrush.OnMouseDown(clickedPixel, self._layer)
        pass

    def OnMouseDrag(self, clickedPixel, previousPixel=None):
        _pixelX, _pixelY = clickedPixel
        _prePixelX, _prePixelY = previousPixel
        if self.currentBrushIdx == 0 or self.currentBrushIdx == 1:
            if abs(_prePixelX - _pixelX) > 1 or abs(_prePixelY - _pixelY) > 1:
                self._DrawLine(*clickedPixel, *previousPixel)
            else:
                self._currentBrush.OnMouseDown(clickedPixel, self._layer)
        else:
            self._currentBrush.OnMouseDrag(clickedPixel, self._layer)

    def OnMouseUp(self, clickedPixel):
        self._currentBrush.OnMouseUp(clickedPixel, self._layer)

    def SetBrush(self, brush):
        if brush == 'Pencil' or brush == _pencil:
            self._currentBrush = self.pencil
            self.currentBrushIdx = 0
        elif brush == 'Eraser' or brush == _eraser:
            self._currentBrush = self.eraser
            self.currentBrushIdx = 1
        elif brush == 'Flood' or brush == _flood:
            self._currentBrush = self.flood
            self.currentBrushIdx = 2
        elif brush == 'Picker' or brush == _picker:
            self._currentBrush = self.picker
            self.currentBrushIdx = 3

    def SetCurrentLayer(self, layer: Layer):
        self._layer = layer

    def SetCurrentColor(self, color):
        if len(color) == 3:
            _r, _g, _b = color
            _a = 255
        else:
            _r, _g, _b, _a = color

        self.pencil.SetCurrentColor((_r, _g, _b, _a))
        self.flood.SetCurrentColor((_r, _g, _b, _a))

    def GetCurrentBrushIndex(self):
        return self.currentBrushIdx

    # ----- for test -----
    def _DrawLine(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        ab = 1 if dy > 0 else -1
        if dx == 0:
            for y in range(y0, y1 + ab, ab):
                self._currentBrush.OnMouseDown((x0, y), self._layer)
            return
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            dy = -dy
            ab = -ab
        slope = abs(dy / dx)
        error = 0
        if slope < 1:
            y = y0
            for x in range(x0, x1 + 1):
                self._currentBrush.OnMouseDown((x, y), self._layer)
                error += slope
                if error > 0.5:
                    error -= 1
                    self._currentBrush.OnMouseDown((x, y), self._layer)
                    y += ab
        else:
            slope = 1 / slope
            x = x0
            for y in range(y0, y1 + ab, ab):
                self._currentBrush.OnMouseDown((x, y), self._layer)
                error += slope
                if error > 0.5:
                    error -= 1
                    self._currentBrush.OnMouseDown((x, y), self._layer)
                    x += 1


Brush = Brush()
