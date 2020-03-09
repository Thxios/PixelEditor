import numpy as np
import pygame as pg
from time import time


t = 0
def Start():
    global t
    t = time()
def End():
    print(time() - t)


def draw(arr, x0, y0, x1, y1):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    print(x0, y0)
    print(x1, y1)
    dx = x1 - x0
    dy = y1 - y0
    slope = abs(dy / dx)
    print(slope)
    ab = 1 if dy > 0 else -1
    error = 0
    y = y0
    for x in range(x0, x1 + 1):
        arr[x, y] = 1
        error += slope
        if error > 0.5:
            for _ in [0] * int(error + 0.5):
                arr[x, y] = 1
                y += ab
            error -= int(error + 0.5)


a = np.zeros((32, 32), dtype=np.int8)
for i in a:
    print(*i)
print('------------------------------------')
draw(a,
     5, 15,
     30, 30)
for i in a.T:
    print(*i)
