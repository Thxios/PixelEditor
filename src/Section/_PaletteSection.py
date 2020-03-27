from src.lib import *
from src.Section._Section import Section
from src.Interaction import Interaction
from src.Brush import Brush


class PaletteSection(Section):
    bgColor = (43, 43, 43)
    paletteBoxColor = (0, 0, 0)
    paletteBoxTerm = 5

    colorBoxSize = 30
    colorBoxTerm = 3

    color: List[Tuple[int, int, int, int]] = []
    colorCount = 0
    colorRect: List[pg.Rect] = []

    selectedIndex = 1
    selectedBoxColor = (255, 255, 0, 127)

    # ----- for test -----
    palettePath = 'palette/0.txt'

    def Setup(self, x, y, w, h):
        super().Setup(x, y, w, h)

        self.ImportPalette(self.palettePath)

        from src.Section.Section import ColorSection

    def Update(self):
        self.surface.fill(self.bgColor)
        self.MakeColorRect()
        # print(self.color)
        # print(self.colorRect)

        for i, colorRect in enumerate(self.colorRect):
            pg.draw.rect(self.surface, self.paletteBoxColor,
                         colorRect.inflate(2 * self.colorBoxTerm, 2 * self.colorBoxTerm))
            pg.draw.rect(self.surface, self.color[i], colorRect)
            pg.draw.rect(self.surface, (255, 255, 255), colorRect, 1)

        if self.selectedIndex >= 0:
            pg.draw.rect(self.surface, self.selectedBoxColor, self.colorRect[self.selectedIndex].inflate(2, 2), 3)

    def MakeColorRect(self):
        self.colorRect = []
        n = (self.rect.w - 2 * self.paletteBoxTerm - self.colorBoxTerm) // (self.colorBoxSize + self.colorBoxTerm)
        for i, color in enumerate(self.color):
            x, y = i % n, i // n
            self.colorRect.append(pg.Rect(
                self.paletteBoxTerm + self.colorBoxTerm + x * (self.colorBoxSize + self.colorBoxTerm),
                self.paletteBoxTerm + self.colorBoxTerm + y * (self.colorBoxSize + self.colorBoxTerm),
                self.colorBoxSize,
                self.colorBoxSize
            ))

    def SetColorIndex(self, idx):
        if idx == self.selectedIndex:
            return
        self.selectedIndex = idx
        if idx != -1:
            Interaction.colorSection.SetColorRGB(*self.color[idx], outer=True)
            Brush.SetCurrentColor(self.color[idx])
        self.Changed()

    def OnMouseDown(self, button, x, y):
        x, y = self.LocalPosition((x, y))
        if button == 1:
            for i, colorRect in enumerate(self.colorRect):
                if colorRect.collidepoint(x, y):
                    self.SetColorIndex(i)
        elif button == 4:
            pass
        elif button == 5:
            pass

    def AddColor(self, color: (int, int, int)):
        if len(color) == 3:
            r, g, b = color
            a = 255
        elif len(color) == 4:
            r, g, b, a = color
        else:
            return

        self.color.append((r, g, b, a))
        self.colorCount += 1
        self.Changed()

    def ImportPalette(self, path):
        try:
            with open(path, 'r') as f:
                colors = f.readlines()
        except FileNotFoundError:
            print('Palette File Not Found in:', path)
            return
        for color in colors:
            rgb = tuple(map(int, color.split()))
            if len(rgb) == 3 or len(rgb) == 4:
                self.AddColor(rgb)
