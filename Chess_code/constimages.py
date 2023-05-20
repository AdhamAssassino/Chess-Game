import pygame as py
from constvaribles import *


class Images:
    def __init__(self):
        self.vars = Const()
        self.images = {}
        self.pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'wQ', 'wK', 'wB', 'wN', 'wR', 'bP', 'wP']

    def imagesSetter(self):
        for i in self.pieces:
            self.images[i] = py.transform.scale(py.image.load('images/' + i + '.png'), (self.vars.getSize(), self.vars.getSize()))
        return self.images
