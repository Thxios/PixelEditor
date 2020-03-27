from src.lib import *
from src.Section.Section import *


class Interaction:

    canvasSection = None
    brushSection = None
    colorSection = None
    frameSection = None
    layerSection = None
    paletteSection = None

    def Initialize(self, **kwargs):
        if 'canvas' in kwargs:
            self.canvasSection = kwargs['canvas']
        if 'brush' in kwargs:
            self.brushSection = kwargs['brush']
        if 'color' in kwargs:
            self.colorSection = kwargs['color']
        if 'frame' in kwargs:
            self.frameSection = kwargs['frame']
        if 'layer' in kwargs:
            self.layerSection = kwargs['layer']
        if 'palette' in kwargs:
            self.paletteSection = kwargs['palette']


Interaction = Interaction()

