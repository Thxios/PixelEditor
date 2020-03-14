from src.lib import *
from src.Section._Section import Section
from src.Sprite import Sprite
from src.Text import Text


class LayerSection(Section):
    bgColor = (43, 43, 43)
    layerCount = Sprite.LayerCount()

    # ----- for test -----
    rectTerm = 15
    verticalTerm = 7
    layerRectHeight = 30
    layerRect: [pg.Rect] = []
    layerName = Sprite.CurrentFrame().GetLayerName()

    def Setup(self, x, y, w, h):
        super().Setup(x, y, w, h)

        # ----- for test -----
        self.MakeRect()

    def Update(self):
        self.surface.fill(self.bgColor)
        for i, rect in enumerate(self.layerRect):
            pg.draw.rect(self.surface, (255, 255, 255), rect, 2)
            Text.LeftAligned(self.layerName[i], self.surface, rect, 10)

    def MakeRect(self):
        for i in range(self.layerCount):
            self.layerRect.append(pg.Rect(self.rectTerm,
                                          self.rectTerm + (self.layerRectHeight + self.verticalTerm) * i,
                                          self.w - self.rectTerm * 2,
                                          self.layerRectHeight))
