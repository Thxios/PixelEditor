from src.lib import *
from src.Section._Section import Section
from src.Brush import Brush


class BrushSection(Section):
    bgColor = (43, 43, 43)

    buttonImage = pg.image.load('data/BrushButton.png')
    buttonSelectedImage = pg.image.load('data/BrushButton_selected.png')
    buttonIconImage = pg.image.load('data/ButtonIcon.png')
    buttonSize = buttonImage.get_width()
    buttonTerm = 3
    buttonRect: List[pg.Rect] = []

    brushCount = 7

    currentBrush = Brush.GetCurrentBrushIndex()

    brushThicknessBG = pg.transform.scale(pg.image.load('data/brushes/brushBG.png'), (60, 60))
    brushThicknessImage = [None] + [
        pg.transform.scale(pg.image.load('data/brushes/' + str(i) + '.png'), (60, 60)) for i in range(1, 6)
    ]

    def Setup(self, x, y, w, h):
        super().Setup(x, y, w, h)
        for _brush in range(self.brushCount):
            self.buttonRect.append(
                pg.Rect(self.w - 36,
                        6 + (self.buttonSize + self.buttonTerm) * _brush,
                        self.buttonSize,
                        self.buttonSize)
            )
        # print('brushSection', self.x, self.y, self.w, self.h)

    def Update(self):
        self.surface.fill(self.bgColor)
        for _brush in range(self.brushCount):
            if _brush == self.currentBrush:
                # self.surface.blit(self.buttonSelectedImage, (6, 6 + (self.buttonSize + self.buttonTerm) * _brush))
                self.surface.blit(self.buttonSelectedImage,
                                  (self.w - 36, 6 + (self.buttonSize + self.buttonTerm) * _brush))
            else:
                # self.surface.blit(self.buttonImage, (6, 6 + (self.buttonSize + self.buttonTerm) * _brush))
                self.surface.blit(self.buttonImage,
                                  (self.w - 36, 6 + (self.buttonSize + self.buttonTerm) * _brush))
        self.surface.blit(self.buttonIconImage, (self.w - 42, 0))

        self.surface.blit(self.brushThicknessBG, (20, 160))
        self.surface.blit(self.brushThicknessImage[Brush.GetBrushThickness()], (20, 160))

    def OnMouseDown(self, button, x, y):
        x, y = self.LocalPosition((x, y))
        for _brush, _button in enumerate(self.buttonRect):
            if _button.collidepoint(x, y):
                self.currentBrush = _brush
                Brush.SetBrush(_brush)
                self.Changed()
                break
