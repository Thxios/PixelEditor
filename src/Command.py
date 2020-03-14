from src.lib import *


class Command:
    key: list

    def GetInput(self):
        self.key = pg.key.get_pressed()

    def GetKey(self, key):
        return self.key[key]


Command = Command()
