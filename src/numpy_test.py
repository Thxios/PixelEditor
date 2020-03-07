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
    dx = x1 - x0
    dy = y1 - y0
    e = 0
    if abs(dy) > abs(dx):
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        x = x0
        slope = abs(dx / dy)
        print(slope)
        for y in range(y0, y1 + 1):
            arr[x, y] = 1
            print(x, y, e)
            e += slope
            if e > 0.5:
                x += 1
                e -= 1
    else:
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        y = y0
        slope = abs(dy / dx)
        print(slope)
        for x in range(x0, x1 + 1):
            arr[x, y] = 1
            print(x, y, e)
            e += slope
            if e > 0.5:
                y += 1
                e -= 1


a = np.zeros((32, 32), dtype=np.int8)
for i in a:
    print(*i)
print('------------------------------------')
draw(a, 31, 0, 10, 31)
for i in a:
    print(*i)
