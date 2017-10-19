import screeninfo
import pandas as pd
import win32gui
from binary_tree import Node
how  = 'v'







class Hades():
    monitors = None
    trees = []
    def __init__(self):
        monitors = pd.DataFrame( columns = ['x','y','width', 'height', 'full'])

        screens = screeninfo.get_monitors()
        for screen in screens:
            position = len(monitors)
            monitors.loc[str(position)]=(screen.x, screen.y, screen.width, screen.height, 0)
            self.trees.append(Node(position))

        self.monitors = monitors

    def split(self, index):
        index = str(index)
        current = self.monitors.loc[index]
        x = current.x
        y = current.y
        width = current.width
        height = current.height
        if how == 'v':
            a = (x, y, width * 0.5, height, 0)
            b = (x + (width * 0.5), y, width * 0.5, height, 0)

        if how == 'h':
            a = (x, y, width , height * 0.5, 0)
            b = (x, y + (height * 0.5), width , height * 0.5, 0)


        a_index = index + '.1'
        b_index = index + '.2'

        self.monitors.loc[a_index] = a
        self.monitors.loc[b_index] = b






x = Hades()
x.split(1)
print(x.monitors)


