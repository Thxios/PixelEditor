import numpy as np
import pygame as pg
from time import time
from src.utility import Clamp


t = 0
def Start():
    global t
    t = time()
def End():
    print(time() - t)


size = 10

a = np.array([
    [255 for _ in range(size)] for _ in range(size)
])

brush = np.array([
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0],
])

brushSize = brush.shape[0]
colorScala = 10

print(a.shape)


def Plot(x, y):
    xs, ys = x - brushSize // 2, y - brushSize // 2
    xe, ye = xs + brushSize, ys + brushSize
    print(x, y)
    print('x', xs, xe, 'y', ys, ye, '\n')

    des = a[max(xs, 0): min(xe, size), max(ys, 0): min(ye, size)]
    print(des.T)
    print('des range:', (max(xs, 0), min(xe, size)), (max(ys, 0), min(ye, size)), '\n')

    brush_des = brush[max(-xs, 0): min(brushSize - xe + size, brushSize),
                max(-ys, 0): min(brushSize - ye + size, brushSize)]
    print(brush[max(-xs, 0): min(brushSize - xe + size, brushSize),
          max(-ys, 0): min(brushSize - ye + size, brushSize)].T)
    print('brush range:',
          (max(-xs, 0), min(brushSize - xe + size, brushSize)),
          (max(-ys, 0), min(brushSize - ye + size, brushSize)), '\n')

    des -= des * brush_des
    des += colorScala * brush_des
    print(a.T, '\n\n')

Plot(2, 2)
Plot(0, 0)
Plot(9, 8)
