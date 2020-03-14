import tkinter as tk
import pygame as pg


class PopupWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

    def ColorPopup(self):
        colorWindow = tk.Toplevel(self)
        self.mainloop()


root = PopupWindow()
print(pg.K_SPACE)
print(type(pg.K_SPACE))
# popup = tk.Toplevel(root)

