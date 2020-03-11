import pygame as pg
from pygame.locals import *
from src.Section import CanvasSection, PaletteSection, FrameSection, ColorSection, Empty
from src.Brush import Brush


class MainWindow:
    w, h = 1600, 960
    bgColor = (78, 82, 84)

    running = False
    screen = None
    clock = pg.time.Clock()
    fps = 126

    originX, originY = 250, h - 200

    Brush.SetBrush('Pencil')
    # ----- for test -----
    Brush.pencil.SetCurrentColor((255, 0, 127, 255))

    CanvasSection.Setup(originX, 0, w - originX, originY)
    CanvasSection.SetupCanvas(64, 64)

    PaletteSection.Setup(0, 0, originX, originY - 200)
    FrameSection.Setup(originX, originY, w - originX, h - originY)
    ColorSection.Setup(0, originY - 200, originX, h - originY + 200)

    # ----- for test -----
    # sprite = Canvas.Empty(20, 15, (0, 0, 0, 255))

    mouseButton = [0, 0, 0, 0]
    mouseButtonCount = len(mouseButton)
    mouseX, mouseY = 0, 0
    mousePreviousX, mousePreviousY = 0, 0
    currentSection = None

    def Run(self):
        pg.init()
        self.screen = pg.display.set_mode((self.w, self.h), SRCALPHA, 32)
        self.screen.fill(self.bgColor)
        pg.display.update()
        self.running = True
        self.MainLoop()

    def MainLoop(self):
        cnt = 0
        while self.running:
            self.mousePreviousX, self.mousePreviousY = self.mouseX, self.mouseY
            self.mouseX, self.mouseY = pg.mouse.get_pos()
            events = pg.event.get()
            for event in events:
                self.EventFeedback(event)
            self.LateFeedback()

            # ----- for test -----
            CanvasSection.Draw(self.screen)
            PaletteSection.Draw(self.screen)
            FrameSection.Draw(self.screen)
            ColorSection.Draw(self.screen)

            self.clock.tick(self.fps)

            cnt += 1
            if cnt % 200 == 0:
                print(self.clock.get_fps())

    def GetMouseSection(self):
        if CanvasSection.IsClicked((self.mouseX, self.mouseY)):
            self.currentSection = CanvasSection
        elif PaletteSection.IsClicked((self.mouseX, self.mouseY)):
            self.currentSection = PaletteSection
        elif FrameSection.IsClicked((self.mouseX, self.mouseY)):
            self.currentSection = FrameSection
        elif ColorSection.IsClicked((self.mouseX, self.mouseY)):
            self.currentSection = ColorSection
        else:
            self.currentSection = Empty

    def EventFeedback(self, event):
        if event.type == QUIT:
            pg.quit()
            quit()

        elif event.type == MOUSEBUTTONDOWN:
            self.GetMouseSection()
            self.currentSection.OnMouseDown(event.button, self.mouseX, self.mouseY)
            if event.button < self.mouseButtonCount:
                self.mouseButton[event.button] = 1
                self.mousePreviousY, self.mousePreviousY = self.mouseX, self.mouseY
            # if event.button == 1:
            #     self.mouseButton[0] = 1
            #
            #     # ----- for test -----
            #     if CanvasSection.IsClicked((self.mouseX, self.mouseY)):
            #         CanvasSection.OnMouseDown(1, self.mouseX, self.mouseY)
            #
            # elif event.button == 2:
            #     self.mouseButton[1] = 1
            #     self._mousePreviousX, self._mousePreviousY = self.mouseX, self.mouseY
            #
            # elif event.button == 3:
            #     self.mouseButton[2] = 1
            #
            # elif event.button == 4:
            #     CanvasSection.Magnify(1, CanvasSection.LocalPosition((self.mouseX, self.mouseY)))
            #
            # elif event.button == 5:
            #     CanvasSection.Magnify(-1, CanvasSection.LocalPosition((self.mouseX, self.mouseY)))

        elif event.type == MOUSEBUTTONUP:
            if event.button < len(self.mouseButton):
                self.mouseButton[event.button] = 0

    def LateFeedback(self):
        for _button in range(1, self.mouseButtonCount):
            if self.mouseButton[_button]:
                self.currentSection.OnMouseDrag(
                    _button,
                    self.mouseX, self.mouseY,
                    self.mousePreviousX, self.mousePreviousY
                )
        # if self.mouseButton[0]:
        #     if CanvasSection.IsClicked((self.mouseX, self.mouseY)):
        #         CanvasSection.OnMouseDrag(1, self.mouseX, self.mouseY)
        # elif self.mouseButton[1]:
        #     CanvasSection.MoveCanvas(
        #         round((self.mouseX - self._mousePreviousX) * self.MOVE_SPEED),
        #         round((self.mouseY - self._mousePreviousY) * self.MOVE_SPEED)
        #     )


MainWindow = MainWindow()
