import pygame as pg
from src.Section._Section import Section
from src.Brush import Brush
from src.Command import Command
from src import utility
from math import sin, cos, atan2, degrees, radians, sqrt


R, G, B = 0, 1, 2
H, S, V = 0, 1, 2
WHEEL, VALUE, ALPHA = 0, 1, 2

class ColorSection(Section):
    colorCenterX: int
    colorCenterY: int

    bgColor = (43, 43, 43)

    colorRGB = (166, 106, 150)
    colorHSV = utility.RGB2HSV(colorRGB)
    alpha = 255
    scrollStep = 5

    colorWheelImage = pg.image.load('data/hue4.png')
    valueWheelImage = pg.image.load('data/value_wheel.png')
    # radius = colorWheelImage.get_width() // 2
    radius = 100
    radiusTerm = colorWheelImage.get_width() // 2 - radius

    dotImage: pg.Surface
    dotDarkImage = pg.image.load('data/dot_dark.png')
    dotBrightImage = pg.image.load('data/dot_bright.png')
    dotRadius = 3

    barWidth = 200
    barHeight = 20
    valueImage = pg.image.load('data/value.png')
    alphaImage = pg.image.load('data/alpha.png')
    valueBarRect: pg.Rect
    alphaBarRect: pg.Rect
    previewAlphaImage = pg.image.load('data/preview_alpha.png')
    preViewSurface = pg.Surface(previewAlphaImage.get_size(), pg.SRCALPHA, 32)

    colorChange = [0, 0, 0]

    # ----- for test -----
    wheelCenterX = 120
    wheelCenterY = 120

    def Setup(self, x, y, w, h):
        super().Setup(x, y, w, h)

        self.SetColorRGB(self.colorRGB)
        self.valueBarRect = pg.Rect((self.w - self.barWidth) // 2,
                                    self.wheelCenterY + self.radius + self.radiusTerm + 15 + 1,
                                    self.barWidth,
                                    self.barHeight)
        self.alphaBarRect = pg.Rect((self.w - self.barWidth) // 2,
                                    self.wheelCenterY + self.radius + self.radiusTerm + 15 + 1 + self.barHeight + 5,
                                    self.barWidth,
                                    self.barHeight)

    def Update(self):
        # print(self.w - self.barWidth)
        # print(self.wheelCenterY + self.radius + self.radiusTerm + 15 + 1)
        self.surface.fill(self.bgColor)
        self.DrawColorWheel()
        self.DrawColorBar()
        self.DrawPreview()

    def SetColorRGB(self, color: (int, int, int)):
        if len(color) == 4:
            _r, _g, _b, _ = color
        else:
            _r, _g, _b = color
        self.SetColorHSV(utility.RGB2HSV(self.colorRGB))

    def SetColorHSV(self, color: (float, float, float)):
        self.colorHSV = color
        self.colorRGB = utility.HSV2RGB(color)
        self.Changed()
        Brush.SetCurrentColor((*self.colorRGB, self.alpha))
        if self.colorHSV[V] > 50:
            self.dotImage = self.dotDarkImage
        else:
            self.dotImage = self.dotBrightImage

    def SetAlpha(self, alpha):
        self.alpha = alpha
        Brush.SetCurrentColor((*self.colorRGB, self.alpha))
        self.Changed()

    def DrawColorWheel(self):
        _theta = radians(90 - self.colorHSV[H])
        _x = round(cos(_theta) * self.radius * self.colorHSV[S] / 100)
        _y = -round(sin(_theta) * self.radius * self.colorHSV[S] / 100)
        # print(_x, _y)
        self.surface.blit(self.colorWheelImage,
                          (self.wheelCenterX - self.radius - self.radiusTerm,
                           self.wheelCenterY - self.radius - self.radiusTerm))
        self.valueWheelImage.set_alpha(255 - round(self.colorHSV[V] / 100 * 255))
        self.surface.blit(self.valueWheelImage,
                          (self.wheelCenterX - self.radius - self.radiusTerm,
                           self.wheelCenterY - self.radius - self.radiusTerm))
        self.surface.blit(self.dotImage,
                          (self.wheelCenterX + _x - self.dotRadius,
                           self.wheelCenterY + _y - self.dotRadius))

    def DrawColorBar(self):
        _baseColor = (self.colorHSV[H], self.colorHSV[S], 100)

        pg.draw.rect(self.surface, utility.HSV2RGB(_baseColor), self.valueBarRect)
        pg.draw.rect(self.surface, self.colorRGB, self.alphaBarRect)
        self.surface.blit(self.valueImage, self.valueBarRect.topleft)
        self.surface.blit(self.alphaImage, self.alphaBarRect.topleft)
        self.surface.blit(self.dotImage, (self.valueBarRect.x + self.colorHSV[V] / 100 * self.barWidth - self.dotRadius,
                                          self.valueBarRect.centery - self.dotRadius))
        self.surface.blit(self.dotImage, (self.alphaBarRect.x + self.alpha / 255 * self.barWidth - self.dotRadius,
                                          self.alphaBarRect.centery - self.dotRadius))

    def DrawPreview(self):
        self.preViewSurface.fill((*self.colorRGB, self.alpha))
        self.surface.blit(self.previewAlphaImage, (20, 310))
        self.surface.blit(self.preViewSurface, (20, 310))

    def Position2HSV(self, x, y) -> (float, float, float):
        _theta = atan2(self.wheelCenterY - y, x - self.wheelCenterX)
        _h = 90 - degrees(_theta)
        if _h < 0:
            _h += 360
        _s = min(self.DistToOrigin(x, y), 100)
        _v = self.colorHSV[V]
        return _h, _s, _v

    def Position2Value(self, x) -> (float, float, float):
        _dx = utility.Clamp(x - self.valueBarRect.x, self.barWidth, 0)
        _v = _dx / self.barWidth * 100
        _h, _s, _ = self.colorHSV
        return _h, _s, _v

    def DiffHSV(self, dh=0, ds=0, dv=0):
        _h = self.colorHSV[H] + dh
        if _h >= 360:
            _h -= 360
        elif _h < 0:
            _h += 360
        _s = utility.Clamp(self.colorHSV[S] + ds, 100, 0)
        _v = utility.Clamp(self.colorHSV[V] + dv, 100, 0)
        self.SetColorHSV((_h, _s, _v))

    def Position2Alpha(self, x) -> int:
        _dx = utility.Clamp(x - self.valueBarRect.x, self.barWidth, 0)
        return round(_dx / self.barWidth * 255)

    def DistToOrigin(self, x, y) -> float:
        return sqrt((x - self.wheelCenterX) ** 2 + (y - self.wheelCenterY) ** 2)

    def OnMouseDown(self, button, x, y):
        x, y = self.LocalPosition((x, y))
        if button == 1:
            if self.DistToOrigin(x, y) < self.radius + self.radiusTerm:
                self.colorChange[WHEEL] = 1
            elif self.valueBarRect.collidepoint(x, y):
                self.colorChange[VALUE] = 1
            elif self.alphaBarRect.collidepoint(x, y):
                self.colorChange[ALPHA] = 1
        elif button == 4:
            if self.DistToOrigin(x, y) < self.radius + self.radiusTerm:
                if Command.GetKey(pg.K_LCTRL):
                    self.DiffHSV(dh=self.scrollStep)
                else:
                    self.DiffHSV(ds=self.scrollStep)
            elif self.valueBarRect.collidepoint(x, y):
                self.DiffHSV(dv=self.scrollStep)
            elif self.alphaBarRect.collidepoint(x, y):
                self.SetAlpha(utility.Clamp(self.alpha + self.scrollStep, 255, 0))
        elif button == 5:
            if self.DistToOrigin(x, y) < self.radius + self.radiusTerm:
                if Command.GetKey(pg.K_LCTRL):
                    self.DiffHSV(dh=-self.scrollStep)
                else:
                    self.DiffHSV(ds=-self.scrollStep)
            elif self.valueBarRect.collidepoint(x, y):
                self.DiffHSV(dv=-self.scrollStep)
            elif self.alphaBarRect.collidepoint(x, y):
                self.SetAlpha(utility.Clamp(self.alpha - self.scrollStep, 255, 0))

    def OnMouseDrag(self, button, x, y, _x, _y):
        x, y = self.LocalPosition((x, y))
        if self.colorChange[WHEEL]:
            self.SetColorHSV(self.Position2HSV(x, y))
        elif self.colorChange[VALUE]:
            self.SetColorHSV(self.Position2Value(x))
        elif self.colorChange[ALPHA]:
            self.SetAlpha(self.Position2Alpha(x))

    def OnMouseUp(self, button, x, y):
        self.colorChange = [0, 0, 0]
