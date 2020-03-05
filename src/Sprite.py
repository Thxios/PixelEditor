import pygame as pg
from src.Layer import Layer


class Sprite:
    layer = []

    def __init__(self, wid, hei):
        self.w = wid
        self.h = hei
        self.surface = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)

    def GetSurface(self):
        self.surface.fill((0, 0, 0, 0))
        for layer in self.layer:
            pg.surfarray.blit_array(self.surface, layer.GetArray())
        return self.surface

    @staticmethod
    def FromLayer(*layer):
        _sprite = Sprite(layer[0].w, layer[0].h)
        _sprite.layer = list(layer)
        return _sprite

    @staticmethod
    def Empty(wid, hei, color=(0, 0, 0, 0)):
        _sprite = Sprite(wid, hei)
        _sprite.layer = [Layer(wid, hei, color)]
        return _sprite


