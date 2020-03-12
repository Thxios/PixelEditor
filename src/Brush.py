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
        if len(color) == 3:
            _r, _g, _b = color
            _a = 255
        else:
            _r, _g, _b, _a = color
        self.currentColor = (_r, _g, _b, _a)


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
    _layer: Layer

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

    def LayerChanged(self):
        return self._layer.IsChanged()

    def LayerApplied(self):
        self._layer.Applied()

    # ----- for test -----
    def DrawLine(self, x0, y0, x1, y1):
        # print('draw', (x0, y0), (x1, y1))
        dx = x1 - x0
        dy = y1 - y0
        ab = 1 if dy > 0 else -1
        if dx == 0:
            for y in range(y0, y1 + ab, ab):
                self.pencil.OnMouseDown((x0, y), self._layer)
            return
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            dy = -dy
            ab = -ab
        # print(' ')
        # print((x0, y0), (x1, y1))
        slope = abs(dy / dx)
        # print(dx, dy)
        # print(slope)
        error = 0
        if slope < 1:
            y = y0
            for x in range(x0, x1 + 1):
                # print((x, y), error)
                self.pencil.OnMouseDown((x, y), self._layer)
                error += slope
                if error > 0.5:
                    error -= 1
                    self.pencil.OnMouseDown((x, y), self._layer)
                    # print((x, y), error)
                    y += ab
        else:
            slope = 1 / slope
            x = x0
            for y in range(y0, y1 + ab, ab):
                self.pencil.OnMouseDown((x, y), self._layer)
                # print((x, y), error)
                error += slope
                if error > 0.5:
                    error -= 1
                    # print((x, y), error)
                    self.pencil.OnMouseDown((x, y), self._layer)
                    x += 1
            # if error > 0.5:
            #     for _ in [0] * int(error - 0.5):
            #         self.pencil.OnMouseDown((x, y), self._layer)
            #         y += ab
            #     error -= int(error - 0.5)


Brush = Brush()
