from src.lib import *


class Text:
    fontName: str = 'd2coding'
    maxFontSize: int = 32

    def __init__(self):
        pg.font.init()

        # font: pg.font.Font = pg.font.SysFont(_fontName, _fontSize)
        self.font: Dict[pg.font.Font] = {
            size: pg.font.SysFont(self.fontName, size) for size in range(10, self.maxFontSize + 1)
        }
        self.color= (255, 255, 255)

    def TextSurface(self, text: str, size) -> pg.Surface:
        return self.font[size].render(text, True, self.color)

    def CenterAligned(
            self,
            text: str,
            surface: pg.Surface,
            rect: pg.Rect,
            size=16
    ):
        _text = self.TextSurface(text, size)
        _w, _h = _text.get_size()
        _x, _y = rect.center
        surface.blit(_text, (_x - _w // 2, _y - _h // 2))

    def LeftAligned(
            self,
            text: str,
            surface: pg.Surface,
            rect: pg.Rect,
            size=16,
            term=15
    ):
        _text = self.TextSurface(text, size)
        _w, _h = _text.get_size()
        _x, _y = rect.x, rect.centery
        surface.blit(_text, (_x + term, _y - _h // 2))


Text = Text()
