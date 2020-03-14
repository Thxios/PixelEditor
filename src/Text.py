from src.lib import *


class Text:
    pg.font.init()

    _fontName = 'd2coding'
    _fontSize = 16
    font = pg.font.SysFont(_fontName, _fontSize)
    color = (255, 255, 255)

    def TextSurface(self, text: str) -> pg.Surface:
        return self.font.render(text, True, self.color)

    def CenterAligned(
            self,
            text: str,
            surface: pg.Surface,
            rect: pg.Rect
    ):
        _text = self.TextSurface(text)
        _w, _h = _text.get_size()
        _x, _y = rect.center
        surface.blit(_text, (_x - _w // 2, _y - _h // 2))

    def LeftAligned(
            self,
            text: str,
            surface: pg.Surface,
            rect: pg.Rect,
            term=15
    ):
        _text = self.TextSurface(text)
        _w, _h = _text.get_size()
        _x, _y = rect.x, rect.centery
        surface.blit(_text, (_x + term, _y - _h // 2))


Text = Text()
