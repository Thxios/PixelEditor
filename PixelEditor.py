import pygame as pg
import numpy as np
import sys
from PIL import Image
from pygame.locals import *
from tkinter import Tk
from tkinter import filedialog
from _collections import deque



class Button:
    def __init__(self, code, x, y, wid, hei):
        self.rect = pg.Rect(x, y, wid, hei)
        self.x = x
        self.y = y
        self.w = wid
        self.h = hei
        self.code = code

    def IsClicked(self, m_x, m_y):
        return self.rect.collidepoint(m_x, m_y)

class UIBox(Button):
    def __init__(self, x, y, wid, hei, code):
        super().__init__(code, x, y, wid, hei)
        self.button = []
        self.clicked = ''

    def AddButton(self, *button):
        for b in button:
            self.button.append(b)
            clickedButton[b.code] = 0

    def IsClicked(self, m_x, m_y):
        if super().IsClicked(m_x, m_y):
            for b in self.button:
                if b.IsClicked(m_x, m_y):
                    self.clicked = b.code
                    return True
        return False

    def ClickedCode(self):
        return self.clicked

    def Draw(self, wid=3):
        pg.draw.rect(screen, UI_boxLineColor, self.rect, wid)

def MakeNewSurface(width, height):
    return pg.Surface((width, height), SRCALPHA)


dataPath = 'pre_data/'

pg.init()
pg.display.set_caption('Pixel Editor v1.0')
pg.font.init()

root = Tk()
root.withdraw()

WIDTH, HEIGHT = 960, 720  # window width, height
bgColor = (43, 43, 43)
surfaceBgColor = (187, 187, 187)
UI_boxColor = (60, 63, 65)
UI_boxLineColor = (255, 255, 255)
selectColor = (0, 162, 232)

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

w, h = 32, 32
surface = MakeNewSurface(w, h)
sArr = pg.surfarray.pixels2d(surface)
magnification = 5
mag_max, mag_min = 25, 1
canvasRect = pg.Rect(206, 0, 754, 664)
surface_x = canvasRect.centerx - (w * magnification) // 2
surface_y = canvasRect.centery - (h * magnification) // 2
# background = pg.Surface((canvasRect.w, canvasRect.h))

mouseInput = [0, 0, 0, 0, 0, 0, 0, 0]  # left, wheel_click, right, scroll_up, scroll_down
pre_x, pre_y = 0, 0  # previous mouse position
mouse_x, mouse_y = 0, 0  # current mouse position
clickedButton = {
    'SlideBar_R': 0,
    'SlideBar_G': 0,
    'SlideBar_B': 0,
    'SlideBar_A': 0,
    'TextInput_R': 0,
    'TextInput_G': 0,
    'TextInput_B': 0,
    'TextInput_A': 0,
}
keyInput = {
    'ctrl': 0,
}
keyPressed = {}
selectDrag = False
selected = False
ss_x, ss_y = 0, 0
se_x, se_y = 0, 0
partialSurf = None
moveSurf = False
moveStart_x, moveStart_y = 0, 0


palette = []
def LoadPalette():
    with open(dataPath + 'palette.txt') as f:
        lines = f.readlines()

    for c in lines:
        palette.append([*map(int, c.rstrip().split()), 255])
        # palette.append(tuple([*map(int, c.rstrip().split())]))

LoadPalette()
currentPalette = 0
cColor = palette[currentPalette]
slideBarLength = 80
currentBrush = 0
brushThickness = 0
bSize = (0, 1, 2, 4, 7)


UI_RGBAFont = pg.image.load(dataPath + 'FontRGBA.png')
UI_SlideBar = pg.image.load(dataPath + 'SlideBar.png')

penCursor = pg.image.load(dataPath + 'PenCursor.png')
pickerCursor = pg.image.load(dataPath + 'PickerCursor.png')
floodCursor = pg.image.load(dataPath + 'FloodFillCursor.png')
selectCursor = pg.image.load(dataPath + 'SelectCursor.png')
moveCursor = pg.image.load(dataPath + 'MoveCursor.png')

bgImage = pg.image.load(dataPath + 'TransparentBG.png')
brushImage = pg.image.load(dataPath + 'BrushIcon.png')
brushDisabledImage = pg.image.load(dataPath + 'BrushIcon_disabled.png')
ThicknessImage = pg.image.load(dataPath + 'Thickness.png')

font = pg.font.SysFont('Consolas', 11)

PaletteUIBox = UIBox(3, 3, 200, 515, 'PaletteBox')
PaletteUIBox.AddButton(
    Button('SlideBar_R', 29, 421, slideBarLength, 10),
    Button('SlideBar_G', 29, 444, slideBarLength, 10),
    Button('SlideBar_B', 29, 467, slideBarLength, 10),
    Button('SlideBar_A', 29, 490, slideBarLength, 10),
    Button('Palette', 16, 300, 272, 101),
    Button('BrushSelect', 19, 226, 168, 24),
    Button('ThicknessSelect', 20, 262, 166, 22),
)
tempUIBox = UIBox(3, 517, 200, 200, 'temp')
AnimationBox = UIBox(202, 667, 756, 50, 'Animation')




def OpenFile():
    path = filedialog.askopenfilenames(
        title='open project from',
        filetypes=[
            ('image files', '*.png'),
            ('image files', '*.jpg'),
            ('all files', '*.*'),
        ]
    )
    print(path)
    for f in path:
        try:
            _img = pg.image.load(f)
            global surface, sArr, w, h
            surface = _img
            sArr = pg.surfarray.pixels2d(surface)
            w, h = sArr.shape
        except pg.error:
            pass

def SaveFileWindow():
    path = filedialog.asksaveasfilename(
        title='save project as',
        initialfile='제목 없음.png',
        defaultextension='*.png',
        filetypes=[
            ('image files', '*.png'),
            ('all files', '*.*')
        ]
    )
    print(path)
    return path

def FloodFill(tx, ty, c):
    q = deque([(tx, ty)])
    ic = sArr[tx, ty]
    to_fill = RGBA2Int(c)

    while len(q):
        cx, cy = q.popleft()
        if sArr[cx, cy] == to_fill:
            continue
        sArr[cx, cy] = to_fill
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                if sArr[nx, ny] == ic:
                    q.append((nx, ny))

def ClickedPixel(mx, my, valid=True):
    _p_x, _p_y = (mx - surface_x) // magnification, (my - surface_y) // magnification

    if valid:
        if 0 <= _p_x < w and 0 <= _p_y < h:
            return _p_x, _p_y
        return -1, -1
    else:
        return _p_x, _p_y

def MoveSurface(dx, dy):
    global surface_x, surface_y
    surface_x += dx
    surface_y += dy

def Center():
    return surface_x + (w * magnification) // 2, surface_y + (h * magnification) // 2

def Magnify(diff):
    center_x, center_y = Center()
    global magnification
    if mag_min <= magnification + diff <= mag_max:
        magnification += diff
    else:
        return

    new_x, new_y = Center()
    MoveSurface(center_x - new_x, center_y - new_y)

def Text(text, x, y, outline=False):
    render = font.render(text, True, UI_boxLineColor)
    screen.blit(render, (x, y))
    if outline:
        _rect = render.get_rect()
        _rect.x = x - 2
        _rect.y = y - 1
        _rect.w += 4
        _rect.h += 2
        pg.draw.rect(screen, UI_boxLineColor, _rect, 1)

def CPaletteColor():
    return palette[currentPalette]

def SetPixel(xx, yy, c):
    # surface.set_at((xx, yy), c)
    sArr[xx, yy] = RGBA2Int(c)
    UpdateSurfaceArray()

def UpdateSurfaceArray():
    pg.surfarray.blit_array(surface, sArr)

# def DashedLine(s, start, end, dash_len=5):
#     x1, y1 = start
#     x2, y2 = end

def DrawSurface():
    screen.blit(bgImage, (0, 0))
    to_draw = pg.transform.scale(surface, (w * magnification, h * magnification))
    # if surface_y >= canvasRect.y:
    pg.draw.rect(screen, bgColor, (canvasRect.x, canvasRect.y, canvasRect.w, surface_y))
    # if surface_x >= canvasRect.x:
    pg.draw.rect(screen, bgColor, (canvasRect.x, canvasRect.y, surface_x - canvasRect.x, canvasRect.h))
    pg.draw.rect(screen, bgColor,
                 (surface_x + w * magnification,
                  canvasRect.y,
                  canvasRect.right - surface_x - w * magnification,
                  canvasRect.h))
    pg.draw.rect(screen, bgColor, (canvasRect.x, surface_y + h * magnification, canvasRect.w, canvasRect.h - surface_y))
    # pg.draw.rect(screen, surfaceBgColor, (surface_x, surface_y, w * magnification, h * magnification))
    screen.blit(to_draw, (surface_x, surface_y))

def DrawUI():
    pg.draw.rect(screen, UI_boxColor, (0, 0, 206, HEIGHT))
    pg.draw.rect(screen, UI_boxColor, (206, 660, 754, 60))

    PaletteUIBox.Draw()
    tempUIBox.Draw()
    AnimationBox.Draw()
    screen.blit(UI_RGBAFont, (14, 422))

    DrawPalette()

def DrawPalette():
    DrawCurrentColor(cColor)
    DrawPaletteColor()
    DrawBrushSelect()
    # DrawBrushThickness()

    for i in range(4):
        DrawRGBABar(i, palette[currentPalette][i])

def DrawPaletteColor():
    for _y in range(4):
        for _x in range(7):
            pg.draw.rect(screen, UI_boxLineColor, (16 + 26 * _x, 300 + 28 * _y, 18, 18), 1)
            if len(palette) > _y * 7 + _x:
                pg.draw.rect(screen, palette[_y * 7 + _x], (17 + 26 * _x, 301 + 28 * _y, 16, 16))
    pg.display.update((16, 300, 272, 101))

def DrawCurrentColor(c):
    pg.draw.rect(screen, c, (153, 422, 30, 30))
    for ii in range(4):
        DrawRGBABar(ii, c[ii])
    pg.display.update((153, 422, 30, 30))

def DrawBrushSelect():
    screen.blit(brushImage, (17, 224))
    pg.draw.rect(screen, selectColor, (18 + 36 * currentBrush, 225, 26, 26), 3)
    pg.display.update((17, 224, 172, 28))

    DrawBrushThickness()

def DrawBrushThickness():
    screen.blit(ThicknessImage, (19, 261))
    if currentBrush in (0, 2):
        pg.draw.rect(screen, selectColor, (19 + 36 * brushThickness, 261, 23, 23), 2)
    else:
        screen.blit(brushDisabledImage, (19, 261))
    pg.display.update((19, 261, 168, 24))

def DrawRGBABar(code, value):
    pg.draw.rect(screen, UI_boxColor, (28, 420 + 23 * code, 110, 14))

    pg.draw.line(screen, UI_boxLineColor, (29, 426 + 23 * code), (28 + slideBarLength, 426 + 23 * code), 1)
    screen.blit(UI_SlideBar, (27 + round(value * slideBarLength / 255), 423 + 23 * code))
    # Text(str(value), 116, 421 + 23 * code, True)
    Text(str(value), 116, 421 + 23 * code)
    pg.display.update((28, 420 + 23 * code, 110, 14))

def InputFeedback():
    pass

def OnMouseLeftDown(m_x, m_y):
    global cColor, currentBrush, brushThickness, selected, selectDrag

    if PaletteUIBox.IsClicked(m_x, m_y):
        selected = False
        selectDrag = False
        code = PaletteUIBox.ClickedCode()

        if code == 'Palette':
            xx, diff_x = (m_x - 16) // 26, (m_x - 16) % 26
            yy, diff_y = (m_y - 300) // 28, (m_y - 300) % 28
            if diff_x <= 18 and diff_y <= 18:
                if yy * 7 + xx < len(palette):
                    cColor = palette[yy * 7 + xx]
                    DrawCurrentColor(cColor)

        elif code == 'BrushSelect':
            xx, diff_x = (m_x - 19) // 36, (m_x - 19) % 36
            if diff_x < 24:
                currentBrush = xx
                DrawBrushSelect()

        elif code == 'ThicknessSelect':
            if currentBrush in (0, 2):
                xx, diff_x = (m_x - 20) // 36, (m_x - 20) % 36
                if diff_x < 22:
                    brushThickness = xx
                    DrawBrushThickness()

        elif code:
            clickedButton[code] = 1

    else:
        _p_x, _p_y = ClickedPixel(m_x, m_y)
        if _p_x >= 0:
            if currentBrush == 1:
                FloodFill(_p_x, _p_y, cColor)
            elif currentBrush == 3:
                cColor = tuple(reversed(Int2RGBA(sArr[_p_x, _p_y])))
                print(cColor)
            elif currentBrush == 4:
                global ss_x, ss_y, moveSurf, moveStart_x, moveStart_y
                if selected:
                    if ss_x <= _p_x <= se_x and ss_y <= _p_y <= se_y:
                        moveSurf = True
                        moveStart_x = ss_x
                        moveStart_y = ss_y
                else:
                    selectDrag = True
                    selected = True
                    ss_x = _p_x
                    ss_y = _p_y


def OnMouseLeftDrag(m_x, m_y):
    if canvasRect.collidepoint(m_x, m_y):
        _p_x, _p_y = ClickedPixel(m_x, m_y)
        if _p_x >= 0:
            xs, xe = max(_p_x - bSize[brushThickness], 0), _p_x + bSize[brushThickness] + 1
            ys, ye = max(_p_y - bSize[brushThickness], 0), _p_y + bSize[brushThickness] + 1
            if currentBrush == 0:
                sArr[xs:xe, ys:ye] = RGBA2Int(cColor)
                UpdateSurfaceArray()
                # SetPixel(_p_x, _p_y, cColor)
            elif currentBrush == 2:
                sArr[xs:xe, ys:ye] = RGBA2Int((0, 0, 0, 0))
                UpdateSurfaceArray()
            elif currentBrush == 4:
                _p_x, _p_y = ClickedPixel(m_x, m_y, False)
                if moveSurf:
                    pass
                elif selectDrag:
                    global se_x, se_y
                    se_x = max(min(_p_x, w - 1), 0)
                    se_y = max(min(_p_y, h - 1), 0)


def OnMouseRightDrag(m_x, m_y):
    if canvasRect.collidepoint(m_x, m_y):
        _p_x, _p_y = ClickedPixel(m_x, m_y)
        if _p_x >= 0:
            SetPixel(_p_x, _p_y, (0, 0, 0, 0))

def RGBScrollBar(code, m_x):
    _pos = max(0, min(slideBarLength, m_x - 29))
    _value = round(_pos * 255 / slideBarLength)
    cColor[code] = _value
    DrawRGBABar(code, _value)
    DrawCurrentColor(cColor)


def Int2RGBA(code):
    r = code % 256
    g = (code // 256) % 256
    b = (code // (256 ** 2)) % 256
    a = (code // (256 ** 3)) % 256
    return a, r, g, b

def RGBA2Int(c):
    r, g, b, a = c
    return a * (256 ** 3) + r * (256 ** 2) + g * 256 + b

def SaveProject(partial=False):
    to_save = partialSurf if partial else sArr
    file = SaveFileWindow()
    if file:
        b = np.stack(np.flip(Int2RGBA(to_save), 0), axis=2).astype(np.uint8)
        img = Image.fromarray(np.swapaxes(b, 0, 1), 'RGBA')
        img.save(file)



DrawUI()
pg.display.update()
# pg.mouse.set_visible(False)

# OpenFile()
# SaveFile()

cnt = 0
while True:
    keyPressed = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            print(pg.mouse.get_pos())
            mouseInput[event.button] = 1
            if event.button == 1:
                OnMouseLeftDown(*pg.mouse.get_pos())
            elif event.button == 4:
                # if keyInput['ctrl']:
                if keyPressed[K_LCTRL]:
                    if magnification < mag_max:
                        Magnify(1)
                else:
                    if currentBrush in (0, 2):
                        if brushThickness < 4:
                            brushThickness += 1
                            DrawBrushThickness()
            elif event.button == 5:
                # if keyInput['ctrl']:
                if keyPressed[K_LCTRL]:
                    if magnification > mag_min:
                        Magnify(-1)
                else:
                    if currentBrush in (0, 2):
                        if brushThickness > 0:
                            brushThickness -= 1
                            DrawBrushThickness()

        elif event.type == MOUSEBUTTONUP:
            mouseInput[event.button] = 0
            for bb in clickedButton:
                clickedButton[bb] = 0
            if selectDrag:
                selectDrag = False
                sx, ex = min(ss_x, se_x), max(ss_x, se_x)
                sy, ey = min(ss_y, se_y), max(ss_y, se_y)
                partialSurf = sArr[sx:ex + 1, sy:ey + 1]

        elif event.type == KEYDOWN:
            if event.key == K_s:
                if keyPressed:
                    SaveProject(selected)
            elif event.key == K_o:
                if keyPressed:
                    OpenFile()
            elif event.key == K_LCTRL:
                keyInput['ctrl'] = 1

        elif event.type == KEYUP:
            if event.key == K_LCTRL:
                keyInput['ctrl'] = 0

    InputFeedback()
    mouse_x, mouse_y = pg.mouse.get_pos()
    # print(mouse_x, mouse_y, mouseInput)
    if mouseInput[1]:  # left click
        OnMouseLeftDrag(mouse_x, mouse_y)
    if mouseInput[2]:  # wheel click
        MoveSurface(mouse_x - pre_x, mouse_y - pre_y)
    if mouseInput[3]:  # right click
        OnMouseRightDrag(mouse_x, mouse_y)

    if clickedButton['SlideBar_R']:
        RGBScrollBar(0, mouse_x)
    if clickedButton['SlideBar_G']:
        RGBScrollBar(1, mouse_x)
    if clickedButton['SlideBar_B']:
        RGBScrollBar(2, mouse_x)
    if clickedButton['SlideBar_A']:
        RGBScrollBar(3, mouse_x)

    if currentBrush == 3:
        p_x, p_y = ClickedPixel(mouse_x, mouse_y)
        if p_x >= 0:
            DrawCurrentColor(Int2RGBA(sArr[p_x, p_y]))
        else:
            DrawCurrentColor(cColor)

    pre_x, pre_y = pg.mouse.get_pos()

    # UpdateSurface()
    pg.draw.rect(screen, bgColor, canvasRect)

    DrawSurface()
    if selected:
        sx, ex = min(ss_x, se_x), max(ss_x, se_x)
        sy, ey = min(ss_y, se_y), max(ss_y, se_y)
        col = (0, 128, 255) if selectDrag else (0, 0, 0)
        pg.draw.rect(screen, col,
                     (surface_x + magnification * sx,
                      surface_y + magnification * sy,
                      magnification * (ex - sx + 1),
                      magnification * (ey - sy + 1)),
                     1)
        pg.draw.rect(screen, (255, 255, 255),
                     (surface_x + magnification * sx + 1,
                      surface_y + magnification * sy + 1,
                      magnification * (ex - sx + 1) - 2,
                      magnification * (ey - sy + 1) - 2),
                     1)

    if canvasRect.collidepoint(mouse_x, mouse_y):
        pg.mouse.set_visible(False)
        p_x, p_y = ClickedPixel(mouse_x, mouse_y)
        if currentBrush == 0:
            screen.blit(penCursor, (mouse_x, mouse_y - 21))
        elif currentBrush == 1:
            screen.blit(floodCursor, (mouse_x, mouse_y - 21))
        elif currentBrush == 2:
            if p_x >= 0:
                pg.draw.rect(screen, (0, 0, 0), (
                    surface_x + (p_x - bSize[brushThickness]) * magnification,
                    surface_y + (p_y - bSize[brushThickness]) * magnification,
                    (bSize[brushThickness] * 2 + 1) * magnification,
                    (bSize[brushThickness] * 2 + 1) * magnification), 1)
                pg.draw.rect(screen, (255, 255, 255), (
                    surface_x + (p_x - bSize[brushThickness]) * magnification + 1,
                    surface_y + (p_y - bSize[brushThickness]) * magnification + 1,
                    (bSize[brushThickness] * 2 + 1) * magnification - 2,
                    (bSize[brushThickness] * 2 + 1) * magnification - 2))
            else:
                pg.mouse.set_visible(True)
        elif currentBrush == 3:
            screen.blit(pickerCursor, (mouse_x, mouse_y - 21))
        elif currentBrush == 4:
            if selected:
                if ss_x <= p_x <= se_x and ss_y <= p_y <= se_y:
                    screen.blit(moveCursor, (mouse_x - 10, mouse_y - 10))
                else:
                    screen.blit(selectCursor, (mouse_x - 10, mouse_y - 10))
            else:
                screen.blit(selectCursor, (mouse_x - 10, mouse_y - 10))
    else:
        pg.mouse.set_visible(True)
    pg.display.update(canvasRect)

    clock.tick(126)
    cnt += 1
    if cnt % 100 == 0:
        print(clock.get_fps())
