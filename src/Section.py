import pygame as pg
from src.Sprite import Sprite
from src.Brush import Brush
from math import ceil, floor


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

    def Setup(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(x, y, w, h)
        self.surface = pg.Surface((w, h), pg.SRCALPHA, 32)
        self._hasChange = True

    def SetBackgroundColor(self, color):
        self.bgColor = color

    def OnMouseDown(self, button, x, y):
        if not self.rect.collidepoint(x, y):
            return
        raise NotImplementedError('For test')

    def Changed(self):
        self._hasChange = True

    def Draw(self, screen):
        if self._hasChange:
            self.Update()
            screen.blit(self.surface, (self.x, self.y))
            pg.draw.rect(screen, self._outlineColor, self.rect, 3)
            self._hasChange = False

    def LocalPosition(self, position) -> (int, int):
        _x, _y = position
        return _x - self.x, _y - self.y

    def Update(self):
        self.surface.fill(self.bgColor)


class CanvasSection(Section):
    canvasWidth: int
    canvasHeight: int
    canvas: pg.Rect

    magnification = 10
    bgImage = pg.image.load('data/TransparentBG.png')
    bgColor = (60, 63, 65)

    sprite = Sprite.Empty(32, 32)

    def SetupCanvas(self, w, h):
        self.canvasWidth = w
        self.canvasHeight = h
        self.canvas = pg.Rect(0, 0, w * self.magnification, h * self.magnification)

    def MoveCanvas(self, dx, dy):
        self.canvas.move_ip(dx, dy)
        self.Changed()

    def Magnify(self, mag, pivot):
        if self.magnification + mag < 1:
            return
        p_x, p_y = pivot
        dx = (self.canvas.x - p_x) / self.magnification
        dy = (self.canvas.y - p_y) / self.magnification
        self.magnification += mag
        new_dx = round(dx * self.magnification)
        new_dy = round(dy * self.magnification)
        self.canvas.x = new_dx + p_x
        self.canvas.y = new_dy + p_y
        self.canvas.w = self.canvasWidth * self.magnification
        self.canvas.h = self.canvasHeight * self.magnification
        self.Changed()

    def DisplayArea(self):
        _xs, _xe = max(0, self.canvas.x), min(self.w, self.canvas.x + self.canvas.w)
        _ys, _ye = max(0, self.canvas.y), min(self.h, self.canvas.y + self.canvas.h)

    def Update(self):
        self.surface.fill(self.bgColor)
        self.surface.blit(self.bgImage, (self.canvas.x, self.canvas.y), self.canvas)
        self.surface.blit(
            pg.transform.scale(self.sprite.GetSurface(), (self.canvas.w, self.canvas.h)),
            self.canvas.topleft
        )

    def OnMouseDown(self, button, x, y):
        print(x, y)
        if self.canvas.collidepoint(x, y):
            _localX, _localY = self.LocalPosition((x, y))
            _pixelX = _localX // self.magnification
            _pixelY = _localY // self.magnification
            Brush.OnMouseDown((_pixelX, _pixelY))


class UISection(Section):
    bgColor = (43, 43, 43)


CanvasSection = CanvasSection()
UISection = UISection()

