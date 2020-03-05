import pygame as pg
from src.Sprite import Sprite


class Canvas:
    x, y = 0, 0
    w, h = 0, 0
    magnification = 10

    frame = []
    currentFrame = 0

    def Move(self, dx, dy):
        self.x += dx
        self.y += dy

    def Magnify(self, mag, pivot):
        if self.magnification + mag < 1:
            return
        p_x, p_y = pivot
        dx = (self.x - p_x) / self.magnification
        dy = (self.y - p_y) / self.magnification
        self.magnification += mag
        new_dx = round(dx * self.magnification)
        new_dy = round(dy * self.magnification)
        self.x = new_dx + p_x
        self.y = new_dy + p_y

    def CurrentFrame(self):
        return self.frame[self.currentFrame]

    def Draw(self, surface):
        surface.blit(pg.transform.scale(self.CurrentFrame().GetSurface(),
                                        (self.w * self.magnification, self.h * self.magnification)),
                     (self.x, self.y))

    def GetSurface(self):
        return pg.transform.scale(self.CurrentFrame().GetSurface(),
                                  (self.w * self.magnification, self.h * self.magnification))

    def ScreenSpaceResolution(self):
        # _xs, _xe = max(self.x, 0), min(self.x + self.w * self.magnification, xLimit)
        # _ys, _ye = max(self.y, 0), min(self.y + self.h * self.magnification, yLimit)
        #
        # return (_xs, _xe), (_ys, _ye)
        return self.x, self.y, self.w * self.magnification, self.h * self.magnification

    @staticmethod
    def Empty(wid, hei, color=(0, 0, 0, 0)):
        _canvas = Canvas()
        _canvas.frame = [Sprite.Empty(wid, hei, color)]
        _canvas.w, _canvas.h = wid, hei
        return _canvas
