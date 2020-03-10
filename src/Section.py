import pygame as pg
from src.Sprite import Sprite
from src.Brush import Brush
from math import ceil
from src.utility import TimerStart, TimerEnd

_tileSize = 32
_gray1 = pg.Surface((_tileSize, _tileSize), pg.SRCALPHA, 32)
_gray2 = pg.Surface((_tileSize, _tileSize), pg.SRCALPHA, 32)
_gray1.fill((127, 127, 127, 255))
_gray2.fill((192, 192, 192, 255))


class Section:
    x: int
    y: int
    w: int
    h: int
    bgColor: (int, int, int)
    rect: pg.Rect
    surface: pg.Surface
    _hasChange: bool

    _outlineColor = (255, 255, 255)
    term = 5

    def Setup(self, x, y, w, h):
        self.x = x + self.term
        self.y = y + self.term
        self.w = w - self.term * 2
        self.h = h - self.term * 2
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.surface = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self._hasChange = True

    def SetBackgroundColor(self, color):
        self.bgColor = color

    def OnMouseDown(self, button, x, y):
        pass

    def OnMouseDrag(self, button, x, y, _x, _y):
        pass

    def OnMouseUp(self, button, x, y):
        pass

    def Changed(self):
        self._hasChange = True

    def Draw(self, screen):
        if self._hasChange:
            self.Update()
            screen.blit(self.surface, (self.x, self.y))
            pg.display.update(pg.draw.rect(screen, self._outlineColor, self.rect, 3))
            self._hasChange = False

    def IsClicked(self, mousePos) -> bool:
        return self.rect.collidepoint(*mousePos)

    def LocalPosition(self, position) -> (int, int):
        _x, _y = position
        return _x - self.x, _y - self.y

    def Update(self):
        self.surface.fill(self.bgColor)


class CanvasSection(Section):
    canvasWidth: int
    canvasHeight: int
    canvas: pg.Rect
    sprite: Sprite
    canvasSurface: pg.Surface
    backgroundOriginal: pg.Surface
    background = pg.Surface

    magnification = 10
    minMagnification = 1
    maxMagnification = 25
    bgColor = (60, 63, 65)
    canvasOutlineWidth = 2

    def SetupCanvas(self, w, h):
        self.sprite = Sprite.Empty(w, h)
        self.canvasWidth = w
        self.canvasHeight = h
        self.canvas = pg.Rect(0, 0, w * self.magnification, h * self.magnification)
        self.canvas.center = self.LocalPosition(self.rect.center)
        self.canvasSurface = self.sprite.GetSurface()

        self.backgroundOriginal = pg.Surface((self.canvasWidth, self.canvasHeight), pg.SRCALPHA, 32)
        for _x in range(ceil(self.canvasWidth / _tileSize)):
            for _y in range(ceil(self.canvasHeight / _tileSize)):
                if (_x + _y) % 2:
                    self.backgroundOriginal.blit(_gray1, (_x * _tileSize, _y * _tileSize))
                else:
                    self.backgroundOriginal.blit(_gray2, (_x * _tileSize, _y * _tileSize))
        self.background = pg.transform.scale(self.backgroundOriginal, self.canvas.size)

    def SetCanvasPosition(self, x, y):
        _x = max(min(x, self.w - self.canvas.w), 0)
        _y = max(min(y, self.h - self.canvas.h), 0)
        self.canvas.x = _x
        self.canvas.y = _y

    def MoveCanvas(self, dx, dy):
        self.canvas.move_ip(dx, dy)
        self.Changed()

    def Magnify(self, mag, pivot):
        if self.magnification + mag < self.minMagnification or self.magnification + mag > self.maxMagnification:
            return
        if self.canvas.collidepoint(*pivot):
            p_x, p_y = pivot
        else:
            p_x, p_y = self.canvas.center
        dx = (self.canvas.x - p_x) / self.magnification
        dy = (self.canvas.y - p_y) / self.magnification
        self.magnification += mag
        new_dx = round(dx * self.magnification)
        new_dy = round(dy * self.magnification)
        # self.SetCanvasPosition(new_dx + p_x, new_dy + p_y)
        self.canvas.x = new_dx + p_x
        self.canvas.y = new_dy + p_y
        self.canvas.w = self.canvasWidth * self.magnification
        self.canvas.h = self.canvasHeight * self.magnification
        self.background = pg.transform.scale(self.backgroundOriginal, self.canvas.size)
        self.Changed()

    def DisplayArea(self):
        _xs, _xe = max(0, self.canvas.x), min(self.w, self.canvas.x + self.canvas.w)
        _ys, _ye = max(0, self.canvas.y), min(self.h, self.canvas.y + self.canvas.h)

    def Update(self):
        self.surface.fill(self.bgColor)
        # self.surface.blit(self.bgImage, (self.canvas.x, self.canvas.y), self.canvas)
        pg.draw.rect(self.surface, (0, 0, 0), (self.canvas.x - self.canvasOutlineWidth,
                                               self.canvas.y - self.canvasOutlineWidth,
                                               self.canvas.w + 2 * self.canvasOutlineWidth,
                                               self.canvas.h + 2 * self.canvasOutlineWidth),
                     1)
        self.surface.blit(self.background, self.canvas.topleft)
        self.surface.blit(pg.transform.scale(self.sprite.GetSurface(), self.canvas.size), self.canvas.topleft)
        # ----- for test -----
        # TimerStart()
        # for _ in range(100):
        #     _toScale = self.sprite.GetSurface()
        # TimerEnd()
        # TimerStart()
        # for _ in range(100):
        #     _toBlit = pg.transform.scale(_toScale, (self.canvas.w, self.canvas.h))  # 0.3578s
        # TimerEnd()
        # TimerStart()
        # for _ in range(100):
        #     _temp = pg.transform.rotozoom(_toScale, 0, self.magnification)
        # TimerEnd()
        # TimerStart()
        # for _ in range(100):
        #     self.surface.blit(_toBlit, self.canvas.topleft)  # 0.0713s
        # TimerEnd()
        # pg.quit()
        # quit()

    def PositionToPixel(self, x, y) -> (int, int, bool):
        if self.canvas.collidepoint(x, y):
            _valid = True
        else:
            _valid = False
        _canvasLocalX, _canvasLocalY = x - self.canvas.x, y - self.canvas.y
        _pixelX = _canvasLocalX // self.magnification
        _pixelY = _canvasLocalY // self.magnification

        return _pixelX, _pixelY, _valid

    def OnMouseDown(self, button, x, y):
        if button == 1:
            pass
            # _localX, _localY = self.LocalPosition((x, y))
            # _pixelX, _pixelY, _valid = self.PositionToPixel(_localX, _localY)
            # if _valid:
            #     Brush.OnMouseDown((_pixelX, _pixelY))
            #     self.Changed()
        elif button == 4:
            self.Magnify(1, self.LocalPosition((x, y)))
        elif button == 5:
            self.Magnify(-1, self.LocalPosition((x, y)))

    def OnMouseDrag(self, button, x, y, _x, _y):
        if button == 1:
            _pixelX, _pixelY, _valid = self.PositionToPixel(*self.LocalPosition((x, y)))
            _prePixelX, _prePixelY, _preValid = self.PositionToPixel(*self.LocalPosition((_x, _y)))
            if _valid and _preValid:
                if abs(_prePixelX - _pixelX) > 1 or abs(_prePixelY - _pixelY) > 1:
                    Brush.DrawLine(_prePixelX, _prePixelY, _pixelX, _pixelY)
                else:
                    Brush.OnMouseDown((_pixelX, _pixelY))
                self.Changed()
        elif button == 2:
            self.MoveCanvas(x - _x, y - _y)


class PaletteSection(Section):
    bgColor = (43, 43, 43)


class FrameSection(Section):
    bgColor = (32, 32, 32)


class ColorSection(Section):
    bgColor = (43, 43, 43)


CanvasSection = CanvasSection()
PaletteSection = PaletteSection()
FrameSection = FrameSection()
ColorSection = ColorSection()
Empty = Section()
