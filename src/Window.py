from src.lib import *
from src.Section.Section import *
from src.Command import Command
from src.Brush import Brush
from src.Interaction import Interaction


class MainWindow:
    bottomTerm = 20
    w, h = 1600, 900
    h += bottomTerm
    # bgColor = (78, 82, 84)
    bgColor = (20, 20, 20)

    running = False
    screen = None
    clock = pg.time.Clock()
    fps = 126

    Brush.SetBrush('Pencil')

    _topTerm = 30
    _left = 250
    _middle = 52
    _l1 = 250
    _l2 = 400 - _topTerm
    _l3 = 250
    _r1 = 800
    _r2 = 100 - _topTerm
    _bs = 52

    # CanvasSection.Setup(_left, _topTerm, w - _left, _r1)
    CanvasSection.Setup(_left + _middle, _topTerm, w - _left - _middle, _r1)
    # PaletteSection.Setup(0, _topTerm, _left - _bs, _l1)
    PaletteSection.Setup(0, _topTerm, _left, _l1)
    # BrushSection.Setup(_left - _bs, _topTerm, _bs, _l1)
    BrushSection.Setup(_left, _topTerm, _middle, _l1 + _l2 + _l3)
    # FrameSection.Setup(_left, _r1 + _topTerm, w - _left, _r2)
    FrameSection.Setup(_left + _middle, _r1 + _topTerm, w - _left - _middle, _r2)
    ColorSection.Setup(0, _l1 + _topTerm, _left, _l2)
    LayerSection.Setup(0, _l1 + _l2 + _topTerm, _left, _l3)

    # ----- for test -----
    Interaction.Initialize(
        palette=PaletteSection,
        color=ColorSection
    )
    # sprite = Canvas.Empty(20, 15, (0, 0, 0, 255))

    mouseButton = [0, 0, 0, 0]
    mouseButtonCount = len(mouseButton)
    mouseX, mouseY = 0, 0
    mousePreviousX, mousePreviousY = 0, 0
    currentSection = None

    def Run(self):
        pg.init()
        self.screen = pg.display.set_mode((self.w, self.h), pg.SRCALPHA, 32)
        self.screen.fill(self.bgColor)
        pg.display.update()
        self.running = True
        self.MainLoop()

    def MainLoop(self):
        cnt = 0
        while self.running:
            self.mousePreviousX, self.mousePreviousY = self.mouseX, self.mouseY
            self.mouseX, self.mouseY = pg.mouse.get_pos()
            Command.GetInput()
            events = pg.event.get()
            for event in events:
                self.EventFeedback(event)
            self.LateFeedback()

            # ----- for test -----
            CanvasSection.Draw(self.screen)
            PaletteSection.Draw(self.screen)
            FrameSection.Draw(self.screen)
            ColorSection.Draw(self.screen)
            LayerSection.Draw(self.screen)
            BrushSection.Draw(self.screen)

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
        elif LayerSection.IsClicked((self.mouseX, self.mouseY)):
            self.currentSection = LayerSection
        elif BrushSection.IsClicked((self.mouseX, self.mouseY)):
            self.currentSection = BrushSection
        else:
            self.currentSection = Empty

    def EventFeedback(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        elif event.type == pg.MOUSEBUTTONDOWN:
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

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button < len(self.mouseButton):
                self.mouseButton[event.button] = 0
            self.currentSection.OnMouseUp(event.button, self.mouseX, self.mouseY)

    def LateFeedback(self):
        for _button in range(1, self.mouseButtonCount):
            if self.mouseButton[_button]:
                self.currentSection.OnMouseDrag(
                    _button,
                    self.mouseX, self.mouseY,
                    self.mousePreviousX, self.mousePreviousY
                )


MainWindow = MainWindow()
