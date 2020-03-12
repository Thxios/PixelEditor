import pygame as pg
from src.Section._Section import Section
from src.Brush import Brush
from src import utility
from math import sin, cos, atan2, degrees, radians, sqrt


R, G, B = 0, 1, 2
H, S, V = 0, 1, 2

class ColorSection(Section):
    colorCenterX: int
    colorCenterY: int

    bgColor = (43, 43, 43)
    colorWheelImage = pg.image.load('data/hue4.png')
    # radius = colorWheelImage.get_width() // 2
    radius = 100
    upperTerm = 15
    colorRGB = (0, 255, 0)
    colorHSV = utility.RGB2HSV(colorRGB)
    print(colorRGB, colorHSV)
    dotImage = pg.image.load('data/dot.png')
    dotRadius = dotImage.get_width() // 2
    radiusTerm = colorWheelImage.get_width() // 2 - radius
    print(radius, radiusTerm, colorWheelImage.get_width())

    colorChange = False

    # ----- for test -----
    wheelCenterX = 120
    wheelCenterY = 120

    def Update(self):
        self.surface.fill(self.bgColor)
        self.DrawColor()

    def SetColorRGB(self, color: (int, int, int)):
        if len(color) == 4:
            _r, _g, _b, _ = color
        else:
            _r, _g, _b = color
        self.colorRGB = (_r, _g, _b)
        self.colorHSV = utility.RGB2HSV(self.colorRGB)
        self.Changed()
        Brush.pencil.SetCurrentColor(self.colorRGB)

    def SetColorHSV(self, color: (float, float, float)):
        self.colorHSV = color
        self.colorRGB = utility.HSV2RGB(color)
        self.Changed()
        Brush.pencil.SetCurrentColor(self.colorRGB)

    def DrawColor(self):
        _theta = radians(90 - self.colorHSV[H])
        _x = round(cos(_theta) * self.radius * self.colorHSV[S] / 100)
        _y = -round(sin(_theta) * self.radius * self.colorHSV[S] / 100)
        # print(_x, _y)
        self.surface.blit(self.colorWheelImage,
                          (self.wheelCenterX - self.radius - self.radiusTerm,
                           self.wheelCenterY - self.radius - self.radiusTerm))
        self.surface.blit(self.dotImage,
                          (self.wheelCenterX + _x - self.dotRadius,
                           self.wheelCenterY + _y - self.dotRadius))

    def Position2HSV(self, x, y) -> (float, float, float):
        _theta = atan2(self.wheelCenterY - y, x - self.wheelCenterX)
        _h = 90 - degrees(_theta)
        _s = min(self.DistToOrigin(x, y), 100)
        _v = self.colorHSV[V]
        return _h, _s, _v

    def DistToOrigin(self, x, y) -> float:
        return sqrt((x - self.wheelCenterX) ** 2 + (y - self.wheelCenterY) ** 2)

    def OnMouseDown(self, button, x, y):
        x, y = self.LocalPosition((x, y))
        if self.DistToOrigin(x, y) < self.radius + self.radiusTerm:
            self.colorChange = True

    def OnMouseDrag(self, button, x, y, _x, _y):
        x, y = self.LocalPosition((x, y))
        if self.colorChange:
            self.SetColorHSV(self.Position2HSV(x, y))

    def OnMouseUp(self, button, x, y):
        self.colorChange = False


