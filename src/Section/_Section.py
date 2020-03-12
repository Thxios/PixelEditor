import pygame as pg


class Section:
    x: int
    y: int
    w: int
    h: int
    centerX: int
    centerY: int
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
        self.centerX = self.w // 2
        self.centerY = self.h // 2
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


