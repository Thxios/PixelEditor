from src.lib import *
from src.Command import Command
from src.Section.Section import *


section = BrushSection
pg.init()

w, h = 66, 250
section.Setup(0, 0, w, h)

screen = pg.display.set_mode((w, h))
print(screen.get_size())
mouseX, mouseY = 0, 0
preX, preY = 0, 0

mouse = [0, 0, 0, 0]

clock = pg.time.Clock()

while 1:
    preX, preY = mouseX, mouseY
    mouseX, mouseY = pg.mouse.get_pos()
    Command.GetInput()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()

        elif e.type == pg.MOUSEBUTTONDOWN:
            section.OnMouseDown(e.button, mouseX, mouseY)
            if e.button < 3:
                mouse[e.button] = 1
                preX, preY = mouseX, mouseY

        elif e.type == pg.MOUSEBUTTONUP:
            section.OnMouseUp(e.button, mouseX, mouseY)
            if e.button < 3:
                mouse[e.button] = 0

    for i in range(1, len(mouse)):
        if mouse[i]:
            section.OnMouseDrag(i, mouseX, mouseY, preX, preY)


    section.Draw(screen)
    clock.tick(126)
