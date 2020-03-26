from src.lib import *
from src.Section._Section import Section
from src.Sprite import Sprite
from src.Text import Text


class LayerSection(Section):
    bgColor: (int, int, int) = (43, 43, 43)
    layerCount: int = Sprite.LayerCount()
    selectedLayer: int = 0
    # ----- for test -----
    rectTerm: int = 10
    verticalTerm: int = 2
    leftTerm: int = 20
    layerRectHeight: int = 30
    layerRect: List[pg.Rect] = []
    layerName: List[str] = Sprite.CurrentFrame().GetLayerName()

    layerColor: (int, int, int) = (60, 63, 65)
    selectedColor: (int, int, int) = (75, 110, 175)
    buttonColor = (96, 98, 99)

    visibleIconImage = pg.image.load('data/visibleIcon.png')
    invisibleIconImage = pg.image.load('data/invisibleIcon.png')

    def Setup(self, x, y, w, h):
        super().Setup(x, y, w, h)

        # ----- for test -----
        self.MakeRect()

    def Update(self):
        # sprint('re')
        self.surface.fill(self.bgColor)
        for i, rect in enumerate(self.layerRect):
            pg.draw.rect(self.surface, self.layerColor, rect)
            if i == self.selectedLayer:
                pg.draw.rect(self.surface,
                             self.selectedColor,
                             rect.inflate(-2 * self.verticalTerm, -2 * self.verticalTerm))
            pg.draw.rect(self.surface, self.buttonColor, (rect.right - 4 - 22, rect.top + 4, 22, 22), 2)
            Text.LeftAligned(self.layerName[i], self.surface, rect, term=10)

    def MakeRect(self):
        for i in range(self.layerCount):
            self.layerRect.append(pg.Rect(self.rectTerm,
                                          self.rectTerm + (self.layerRectHeight + self.verticalTerm) * i,
                                          self.w - self.rectTerm * 2 - self.leftTerm,
                                          self.layerRectHeight))

    def SetLayer(self, idx):
        if idx < self.layerCount:
            self.selectedLayer = idx
        else:
            raise IndexError(str(self.layerCount) + ' layer but given ' + str(idx))
        self.Changed()

    def OnMouseDown(self, button, x, y):
        x, y = self.LocalPosition((x, y))
        if button == 1:
            for i, rect in enumerate(self.layerRect):
                if rect.collidepoint(x, y):
                    Sprite.SetCurrentLayer(i)
                    self.selectedLayer = i
                    self.Changed()
