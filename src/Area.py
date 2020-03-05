import pygame as pg


class Area:
    def __init__(self, x, y, wid, hei):
        self.x = x
        self.y = y
        self.w = wid
        self.h = hei

        self.rect = pg.Rect(x, y, wid, hei)
        self.sub = []

    def OnClicked(self, x, y):
        if not self.rect.collidepoint(x, y):
            return

        for sub in self.sub:
            sub.OnClicked(x, y)
