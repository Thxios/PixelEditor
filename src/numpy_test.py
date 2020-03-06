import numpy as np
import pygame as pg
from time import time


t = 0
def Start():
    global t
    t = time()
def End():
    print(time() - t)


pg.init()

a = pg.Rect(10, 10, 50, 50)
a.w = 70
a.h = 100
print(a)
print(a.center)
