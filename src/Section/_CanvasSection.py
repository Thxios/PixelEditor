from src.lib import *
from src.Section._Section import Section
from src.Brush import Brush
from src.Sprite import Sprite
from src.Command import Command
from src import utility
from math import ceil


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

    tileSize = 32
    _gray1 = pg.Surface((tileSize, tileSize), pg.SRCALPHA, 32)
    _gray2 = pg.Surface((tileSize, tileSize), pg.SRCALPHA, 32)
    _gray1.fill((127, 127, 127, 255))
    _gray2.fill((192, 192, 192, 255))

    # ----- for test -----
    limit = 20
    cursorColor = (60, 63, 65)

    def Setup(self, x, y, w, h):
        super().Setup(x, y, w, h)
        self.SetupCanvas()

    def Draw(self, screen):
        if self._hasChange:
            self.Update()
            self._hasChange = False
        _surface = self.surface.copy()
        self.DrawCursor(_surface)
        screen.blit(_surface, (self.x, self.y))
        pg.display.update(pg.draw.rect(screen, self._outlineColor, self.rect, 3))

    def SetupCanvas(self):
        # self.sprite = Sprite.Empty(w, h)
        self.canvasWidth = Sprite.w
        self.canvasHeight = Sprite.h
        self.canvas = pg.Rect(0, 0, self.canvasWidth * self.magnification, self.canvasHeight * self.magnification)
        self.canvas.center = self.LocalPosition(self.rect.center)
        self.canvasSurface = Sprite.GetSurface()

        self.backgroundOriginal = pg.Surface((self.canvasWidth, self.canvasHeight), pg.SRCALPHA, 32)
        for _x in range(ceil(self.canvasWidth / self.tileSize)):
            for _y in range(ceil(self.canvasHeight / self.tileSize)):
                if (_x + _y) % 2:
                    self.backgroundOriginal.blit(self._gray1, (_x * self.tileSize, _y * self.tileSize))
                else:
                    self.backgroundOriginal.blit(self._gray2, (_x * self.tileSize, _y * self.tileSize))
        self.background = pg.transform.scale(self.backgroundOriginal, self.canvas.size)

    def SetCanvasPosition(self, x, y):
        _x = utility.Clamp(x, self.w - self.limit, -self.canvas.w + self.limit)
        _y = utility.Clamp(y, self.h - self.limit, -self.canvas.h + self.limit)
        self.canvas.x = _x
        self.canvas.y = _y

    def MoveCanvas(self, dx, dy):
        self.canvas.move_ip(dx, dy)
        if self.canvas.x > self.w - self.limit or self.canvas.x < -self.canvas.w + self.limit:
            self.canvas.x = utility.Clamp(self.canvas.x,
                                          self.w - self.limit, -self.canvas.w + self.limit)
        if self.canvas.y > self.h - self.limit or self.canvas.y < -self.canvas.h + self.limit:
            self.canvas.y = utility.Clamp(self.canvas.y,
                                          self.h - self.limit, -self.canvas.h + self.limit)
        # print(self.canvas.topleft)
        self.Changed()

    def Magnify(self, mag, pivot):
        if self.magnification + mag < self.minMagnification or self.magnification + mag > self.maxMagnification:
            return
        if self.canvas.collidepoint(*pivot):
            p_x, p_y = pivot
        else:
            p_x = utility.Clamp(pivot[0], self.canvas.x + self.canvas.w, self.canvas.x)
            p_y = utility.Clamp(pivot[1], self.canvas.y + self.canvas.h, self.canvas.y)
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

    def DrawCursor(self, surface):
        _mouseX, _mouseY = pg.mouse.get_pos()
        if self.IsClicked((_mouseX, _mouseY)):
            pg.draw.circle(surface, self.cursorColor, self.LocalPosition((_mouseX, _mouseY)),
                           self.magnification * Brush.GetBrushThickness() // 2, 1)

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
        self.surface.blit(pg.transform.scale(Sprite.GetSurface(), self.canvas.size), self.canvas.topleft)
        # ----- for test -----
        # utility.TimerStart()
        # for _ in range(100):
        #     _toScale = Sprite.GetSurface()
        # utility.TimerEnd()
        # utility.TimerStart()
        # for _ in range(100):
        #     _toBlit = pg.transform.scale(_toScale, (self.canvas.w, self.canvas.h))  # 0.3578s
        # utility.TimerEnd()
        # TimerStart()
        # for _ in range(100):
        #     _temp = pg.transform.rotozoom(_toScale, 0, self.magnification)
        # TimerEnd()
        # utility.TimerStart()
        # for _ in range(100):
        #     self.surface.blit(_toBlit, self.canvas.topleft)  # 0.0713s
        # utility.TimerEnd()
        # pg.quit()
        # quit()

    def SpriteUpdate(self):
        self.SetupCanvas()
        self.Changed()

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
        x, y = self.LocalPosition((x, y))
        if button == 1:
            _pixelX, _pixelY, _valid = self.PositionToPixel(x, y)
            Brush.OnMouseDown((_pixelX, _pixelY))
            # _localX, _localY = self.LocalPosition((x, y))
            # _pixelX, _pixelY, _valid = self.PositionToPixel(_localX, _localY)
            # if _valid:
            #     Brush.OnMouseDown((_pixelX, _pixelY))
            #     self.Changed()
        elif button == 4:
            if Command.GetKey(pg.K_LCTRL):
                Brush.BrushMagnify(1)
            else:
                self.Magnify(1, (x, y))
        elif button == 5:
            if Command.GetKey(pg.K_LCTRL):
                Brush.BrushMagnify(-1)
            else:
                self.Magnify(-1, (x, y))

    def OnMouseDrag(self, button, x, y, _x, _y):
        x, y = self.LocalPosition((x, y))
        _x, _y = self.LocalPosition((_x, _y))
        if button == 1:
            _pixelX, _pixelY, _valid = self.PositionToPixel(x, y)
            _prePixelX, _prePixelY, _preValid = self.PositionToPixel(_x, _y)
            if _valid and _preValid:
                Brush.OnMouseDrag((_pixelX, _pixelY), (_prePixelX, _prePixelY))
                self.Changed()
        elif button == 2:
            self.MoveCanvas(x - _x, y - _y)

