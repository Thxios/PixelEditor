import pygame as pg
from src.Layer import Layer
from src.Brush import PencilBrush
from src import utility


OUTLINE_COLOR = (255, 255, 255)


class Section:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.bgColor = color
        self.surface = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.surface.fill(self.bgColor)
        self.sub = []

        self._hasChange = True

    def OnClicked(self, button, x, y):
        if not self.rect.collidepoint(x, y):
            return

        for sub in self.sub:
            sub.OnClicked(button, x, y)

    def Changed(self):
        self._hasChange = True

    def Draw(self, screen):
        if self._hasChange:
            self.Update()
            screen.blit(self.surface, (self.x, self.y))
            pg.draw.rect(screen, OUTLINE_COLOR, self.rect, 3)
            self._hasChange = False

    def LocalPosition(self, position):
        _x, _y = position
        return _x - self.x, _y - self.y

    def Update(self):
        self.surface.fill(self.bgColor)


class CanvasSection(Section):
    magnification = 10
    canvasWidth, canvasHeight = 32, 32
    canvas = pg.Rect(0, 0, canvasWidth * magnification, canvasHeight * magnification)

    # ----- for test -----

    pencilBrush = PencilBrush()

    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)

        self.bgColorInt = utility.RGBA2INT(color)
        self.bgImage = pg.image.load('data/TransparentBG.png')

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

    def Update(self):
        self.surface.fill(self.bgColor)
        self.surface.blit(self.bgImage, (self.canvas.x, self.canvas.y), self.canvas)

    def OnClicked(self, button, x, y):
        if self.canvas.collidepoint(x, y):
            _clickedPixelX = (x - self.canvas.x) // self.magnification
            _clickedPixelY = (y - self.canvas.y) // self.magnification
            self.pencilBrush.OnMouseDown((_clickedPixelX, _clickedPixelY))


class UISection(Section):
    pass


