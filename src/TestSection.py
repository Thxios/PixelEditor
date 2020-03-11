import pygame as pg
from src.Section import ColorSection


section = ColorSection
pg.init()

w, h = 250, 400
section.Setup(0, 0, w, h)

screen = pg.display.set_mode((w, h))
mouseX, mouseY = 0, 0

while 1:
    mouseX, mouseY = pg.mouse.get_pos()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()
        elif e.type == pg.MOUSEBUTTONDOWN:
            section.OnMouseDown(e.button, mouseX, mouseY)

    section.Draw(screen)
