import numpy as np
import pygame as pg
from time import time


t = 0
def Start():
    global t
    t = time()
def End():
    print(time() - t)


class Test:
    c = (0, 0, 0)

    @property
    def aa(self):
        return self.c

    @aa.setter
    def aa(self, val):
        print(val)
        self.c = val

    def __get__(self, instance, owner):
        print('s')


i = Test()
print(i.aa)
i.aa = (255, 255, 255)
print(i.aa)

pg.init()
screen = pg.display.set_mode((640, 400))
screen.fill(i)
