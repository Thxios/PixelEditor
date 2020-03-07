import pygame as pg
from pygame.locals import *
from src.Section import CanvasSection, ColorSection
from src.Brush import Brush
from OpenGL.GL import *
from OpenGL.GLU import *


class MainWindow:
    MOVE_SPEED = 1
    w, h = 1280, 960

    running = False
    screen = None
    clock = pg.time.Clock()
    fps = 126

    CanvasSection.Setup(320, 0, 960, 960)
    CanvasSection.SetupCanvas(32, 32)

    ColorSection.Setup(0, 0, 320, 960)

    # ----- for test -----
    # sprite = Canvas.Empty(20, 15, (0, 0, 0, 255))

    mouseButton = [0, 0, 0]
    mouseX, mouseY = 0, 0
    _mousePreviousX, _mousePreviousY = 0, 0

    Brush.SetBrush('Pencil')
    # ----- for test -----
    Brush.pencil.SetCurrentColor((255, 0, 127, 255))


    def Run(self):
        pg.init()
        self.screen = pg.display.set_mode((self.w, self.h), SRCALPHA | DOUBLEBUF | OPENGLBLIT, 32)
        self.running = True
        self.MainLoop()

    def MainLoop(self):
        cnt = 0
        while self.running:
            self._mousePreviousX, self._mousePreviousY = self.mouseX, self.mouseY
            self.mouseX, self.mouseY = pg.mouse.get_pos()
            events = pg.event.get()
            for event in events:
                self.EventFeedback(event)

            self.LateFeedback()

            # ----- for test -----
            CanvasSection.Draw(self.screen)
            ColorSection.Draw(self.screen)

            pg.display.update()
            self.clock.tick(self.fps)

            cnt += 1
            if cnt % 100 == 0:
                print(self.clock.get_fps())

    def EventFeedback(self, event):
        if event.type == QUIT:
            pg.quit()
            quit()

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouseButton[0] = 1

                # ----- for test -----
                if CanvasSection.IsClicked((self.mouseX, self.mouseY)):
                    CanvasSection.OnMouseDown(1, self.mouseX, self.mouseY)

            elif event.button == 2:
                self.mouseButton[1] = 1
                self._mousePreviousX, self._mousePreviousY = self.mouseX, self.mouseY

            elif event.button == 3:
                self.mouseButton[2] = 1

            elif event.button == 4:
                CanvasSection.Magnify(1, CanvasSection.LocalPosition((self.mouseX, self.mouseY)))

            elif event.button == 5:
                CanvasSection.Magnify(-1, CanvasSection.LocalPosition((self.mouseX, self.mouseY)))

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.mouseButton[0] = 0

            elif event.button == 2:
                self.mouseButton[1] = 0

            elif event.button == 3:
                self.mouseButton[2] = 0

    def LateFeedback(self):
        if self.mouseButton[0]:
            if CanvasSection.IsClicked((self.mouseX, self.mouseY)):
                CanvasSection.OnMouseDrag(1, self.mouseX, self.mouseY)
        elif self.mouseButton[1]:
            CanvasSection.MoveCanvas(
                round((self.mouseX - self._mousePreviousX) * self.MOVE_SPEED),
                round((self.mouseY - self._mousePreviousY) * self.MOVE_SPEED)
            )


MainWindow = MainWindow()
