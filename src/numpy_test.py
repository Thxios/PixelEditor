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
a = pg.Surface((5, 5), pg.SRCALPHA)
a.fill((200, 0, 127, 255))
s = pg.display.set_mode((100, 100), pg.SRCALPHA)

b = pg.surfarray.pixels2d(a)
print(b)
c = b[0, 0]
print(c%256, (c//256)%256, (c//256//256)%256, (c//256//256//256)%256)
Start()
pix = pg.surfarray.pixels2d(s)
for _ in range(10000):
    d = pg.surfarray.make_surface(b)
    print(d.get_size())
    s.blit(d, (0, 0))
End()
Start()
for _ in range(10000):
    pix[0:5, 0:5] = b
End()

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    pg.display.update()

