import pygame as pg


class Canvas:
    x, y = 0, 0
    w, h = 0, 0
    rect = pg.Rect(x, y, w, h)
    magnification = 10

    frame = []
    currentFrame = 0

    def SetRect(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(x, y, w, h)

    def Move(self, dx, dy):
        self.x += dx
        self.y += dy

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

