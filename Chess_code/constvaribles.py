from docutils.nodes import row


class Const:
    def __init__(self):
        # Screen dimensions
        self.width = 600
        self.height = 600
        # Board dimensions
        self.rows = 8
        self.cols = 8
        self.max_fps = 15
        self.size = self.width // self.cols


    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getRow(self):
        return self.rows

    def getCols(self):
        return self.cols

    def getSize(self):
        return self.getWidth() // self.getCols()

    def getMax_fps(self):
        return self.max_fps
