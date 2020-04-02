from src.lib import *
from src.Sprite import Sprite
import tkinter as tk
from tkinter import filedialog


class FileIO:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

    @staticmethod
    def Open():
        try:
            _image = pg.image.load(FileIO.FileOpenWindow())
        except pg.error:
            print('cannot open file')
            return
        Sprite.FromSurface(_image, in_place=True)

    @staticmethod
    def Save():
        FileIO.SaveImage(Sprite.GetSurface(), FileIO.FileSaveWindow())

    @staticmethod
    def SaveImage(surface: pg.Surface, path):
        try:
            pg.image.save(surface, path)
        except pg.error:
            print('cannot save file')
            return

    @staticmethod
    def FileSaveWindow():
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

    @staticmethod
    def FileOpenWindow():
        path = filedialog.askopenfilename(
            title='open project from',
            filetypes=[
                ('image files', '*.png'),
                ('image files', '*.jpg'),
                ('all files', '*.*'),
            ]
        )
        print(path)
        return path


FileIO = FileIO()
