from src.lib import *
from src.Section._Section import Section


class PaletteSection(Section):
    bgColor = (43, 43, 43)
    paletteBoxColor = (0, 0, 0)
    paletteBoxTerm = 5

    colorBoxSize = 30
    colorBoxTerm = 3

    color: List[Tuple[int, int, int, int]] = []
    colorCount = 0
    colorRect: List[pg.Rect] = []

    # ----- for test -----
    palettePath = 'palette/0.txt'

    def Setup(self, x, y, w, h):
        super().Setup(x, y, w, h)

        self.ImportPalette(self.palettePath)

    def Update(self):
        self.surface.fill(self.bgColor)
        self.MakeColorRect()
        print(self.color)
        print(self.colorRect)

        for i, colorRect in enumerate(self.colorRect):
            pg.draw.rect(self.surface, self.paletteBoxColor,
                         colorRect.inflate(2 * self.colorBoxTerm, 2 * self.colorBoxTerm))
            pg.draw.rect(self.surface, self.color[i], colorRect)

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

    def OnMouseDown(self, button, x, y):
        x, y = self.LocalPosition((x, y))
        if button == 1:
            pass
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
