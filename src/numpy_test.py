import numpy as np
import pygame as pg
from time import time


t = 0
def Start():
    global t
    t = time()
def End():
    print(time() - t)


class Boo:
    def DoSomething(self):
        return


class TestClass:
    member: [Boo]

    def __init__(self):
        self.member = []


a = TestClass()
print(a.member)
