import pygame as pg
import numpy as np
from src.Canvas import Canvas
from src.Layer import Layer
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
    canvas = Canvas.Empty(20, 15)

    # ----- for test -----
    pg.draw.circle(canvas.CurrentFrame().layer[0]._surface, (255, 0, 0, 255), (10, 5), 6)

    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h, color)

        self.bgColorInt = utility.RGBA2INT(color)
        self.bgImage = pg.image.load('data/TransparentBG.png')

    def Update(self):
        self.surface.fill(self.bgColor)
        self.surface.blit(self.bgImage, (self.canvas.x, self.canvas.y), self.canvas.ScreenSpaceResolution())
        self.surface.blit(self.canvas.GetSurface(), (self.canvas.x, self.canvas.y))


