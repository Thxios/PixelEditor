import pygame as pg
from pygame.locals import *
from src.Section import CanvasSection, UISection
from src.Brush import Brush


class MainWindow:
    MOVE_SPEED = 1
    w, h = 1280, 960

    running = False
    screen = None
    clock = pg.time.Clock()
    fps = 125

    CanvasSection.Setup(320, 0, 960, 960)
    CanvasSection.SetupCanvas(32, 32)

    UISection.Setup(0, 0, 320, 960)

    # ----- for test -----
    # sprite = Canvas.Empty(20, 15, (0, 0, 0, 255))

    mouseButtonDown = [0, 0, 0]
    mouseX, mouseY = 0, 0
    _mousePreviousX, _mousePreviousY = 0, 0

    Brush.SetBrush('Pencil')
    # ----- for test -----
    Brush.pencil.SetCurrentColor((255, 255, 255, 255))


    def Run(self):
        pg.init()
        self.screen = pg.display.set_mode((self.w, self.h), SRCALPHA, 32)
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
            UISection.Draw(self.screen)

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
                self.mouseButtonDown[0] = 1

                # ----- for test -----
                CanvasSection.OnMouseDown(1, self.mouseX, self.mouseY)

            elif event.button == 2:
                self.mouseButtonDown[1] = 1
                self._mousePreviousX, self._mousePreviousY = self.mouseX, self.mouseY

            elif event.button == 3:
                self.mouseButtonDown[2] = 1

            elif event.button == 4:
                CanvasSection.Magnify(1, CanvasSection.LocalPosition((self.mouseX, self.mouseY)))

            elif event.button == 5:
                CanvasSection.Magnify(-1, CanvasSection.LocalPosition((self.mouseX, self.mouseY)))

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.mouseButtonDown[0] = 0

            elif event.button == 2:
                self.mouseButtonDown[1] = 0

            elif event.button == 3:
                self.mouseButtonDown[2] = 0

    def LateFeedback(self):
        if self.mouseButtonDown[1]:
            pass
            CanvasSection.MoveCanvas(
                round((self.mouseX - self._mousePreviousX) * self.MOVE_SPEED),
                round((self.mouseY - self._mousePreviousY) * self.MOVE_SPEED)
            )


MainWindow = MainWindow()
