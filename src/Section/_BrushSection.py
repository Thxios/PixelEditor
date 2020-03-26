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

    def Setup(self, x, y, w, h):
        super().Setup(x, y, w, h)
        for _brush in range(self.brushCount):
            self.buttonRect.append(
                pg.Rect(6, 6 + (self.buttonSize + self.buttonTerm) * _brush, self.buttonSize, self.buttonSize)
            )

    def Update(self):
        self.surface.fill(self.bgColor)
        for _brush in range(self.brushCount):
            if _brush == self.currentBrush:
                self.surface.blit(self.buttonSelectedImage, (6, 6 + (self.buttonSize + self.buttonTerm) * _brush))
            else:
                self.surface.blit(self.buttonImage, (6, 6 + (self.buttonSize + self.buttonTerm) * _brush))
        self.surface.blit(self.buttonIconImage, (0, 0))

    def OnMouseDown(self, button, x, y):
        x, y = self.LocalPosition((x, y))
        for _brush, _button in enumerate(self.buttonRect):
            if _button.collidepoint(x, y):
                self.currentBrush = _brush
                Brush.SetBrush(_brush)
                self.Changed()
                break
