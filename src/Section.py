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

    def OnClicked(self, button, x, y):
        if not self.rect.collidepoint(x, y):
            return

        for sub in self.sub:
            sub.OnClicked(button, x, y)

    def Draw(self, screen):
        self.Update()
        screen.blit(self.surface, (self.x, self.y))
        pg.draw.rect(screen, OUTLINE_COLOR, self.rect, 3)

    def LocalPosition(self, position):
        _x, _y = position
        return _x - self.x, _y - self.y

    def Update(self):
        raise NotImplementedError()


class CanvasSection(Section):
    canvasX, canvasY = 0, 0
    canvasWidth, canvasHeight = 20, 15
    magnification = 10
    canvasRect = pg.Rect(canvasX, canvasY, canvasWidth * magnification, canvasHeight * magnification)

    # ----- for test -----

    pencilBrush = PencilBrush()

    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)

        self.bgColorInt = utility.RGBA2INT(color)
        self.bgImage = pg.image.load('data/TransparentBG.png')

    def MoveCanvas(self, dx, dy):
        self.canvasX += dx
        self.canvasY += dy
        self.canvasRect.move_ip(dx, dy)

    def Magnify(self, mag, pivot):
        if self.magnification + mag < 1:
            return
        p_x, p_y = pivot
        dx = (self.canvasX - p_x) / self.magnification
        dy = (self.canvasY - p_y) / self.magnification
        self.magnification += mag
        new_dx = round(dx * self.magnification)
        new_dy = round(dy * self.magnification)
        self.canvasX = new_dx + p_x
        self.canvasY = new_dy + p_y
        self.canvasRect.w = self.canvasWidth * self.magnification
        self.canvasRect.h = self.canvasHeight * self.magnification

    def Update(self):
        self.surface.fill(self.bgColor)
        self.surface.blit(self.bgImage, (self.canvasX, self.canvasY), self.canvasRect)

    def OnClicked(self, button, x, y):
        if self.canvasRect.collidepoint(x, y):
            _clickedPixelX = (x - self.canvasX) // self.magnification
            _clickedPixelY = (y - self.canvasY) // self.magnification
            self.pencilBrush.OnMouseDown((_clickedPixelX, _clickedPixelY))


