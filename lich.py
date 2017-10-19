import wand
import screeninfo
import time

class Node():

    left = None
    right = None
    parent = None
    id  = None
    x = None
    y = None
    height = None
    width = None
    window = None


    def get(self, id , what = 'id',):

        if str(self.__dict__[what]) == str(id):
            return self

        if self.left != None:
            left = self.left.get(id, what)
            if left != None:
                return left

            return self.right.get(id, what)
        return None


    def __init__(self, id,x, y, width, height, parent):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.id = str(id)
        self.parent = parent

    def add_window(self, window, how ):
        if self.window == None:
            self.window = window
            wand.fill_monitor(window, self)
            return

        if self.right != None:
            self.right.add_window(window, how)

        if self.right == None:
            self._split(how)
            self.left.add_window(self.window, how)
            self.right.add_window(window, how)
            self.window = [self.window, window]

    def remove(self):
        wand.minimize(self.window)
        if self.parent != None:

            if self.parent.right == self:
                self.parent.right = None
            if self.parent.left == self:
                self.parent.left = None
            self.parent.balance()

    def balance(self):
        if self.left == None:
            self.add_window(self.right.window)
            self.right = None
            return

        if self.right == None:
            self.add_window(self.left.window)
            self.left = None
            return

    def _split(self, how):
        width = self.width
        height = self.height
        x = self.x
        y = self.y
        if how == 'v':
            a = (x, y, width * 0.5, height, 0)
            b = (x + (width * 0.5), y, width * 0.5, height, 0)
        if how == 'h':
            a = (x, y, width , height * 0.5, 0)
            b = (x, y + (height * 0.5), width , height * 0.5, 0)

        id1 = self.id + '.1'
        id2 = self.id + '.2'

        self.left = Node(id1,a[0], a[1], a[2], a[3],self)
        self.right = Node(id2,b[0],b[1], b[2], b[3] ,self)
        return

    def _combine(self, window = None):
        self.left = None
        self.right = None
        if window != None:
            wand.move_window(window, self)


    def __str__(self):
        if self.id == None:
            return ''
        final = str(self.id)
        if self.left != None:
            final = final +'[' +str(self.left) + ','
        if self.right != None:
            final = final + str(self.right) + ']'

        return final

def initalize():

    screens = []
    windows = wand.get_windows()

    screen_raw = screeninfo.get_monitors()
    for screen in screen_raw:
        position = len(screens)
        screens.append( Node(position, screen.x, screen.y, screen.width, screen.height, None) )
    del screen_raw

    i = 0
    how = 'v'
    for window in windows.index:
        screens[i].add_window(window, how )
        i = i + 1
        if i >= len(screens):
            i = 0

    return screens

def get_node(id, what):
    result = None
    for screen in screens:
        result = screen.get(id, what)
        if result != None:
            return result


screens = initalize()
moving = False



class manager():
    screens = None
    moving = False
    how = 'v'
    move_window = None

    def __init__(self):

        wand.win_h()
        wand.win_v()
        wand.win_click()

    def start(self):
        while True:
            if wand.win_h():
                self.how = 'h'
                print(self.how)
            if wand.win_v():
                self.how = 'v'
                print(self.how)

            if wand.win_click() != 0:
                if self.moving == False:
                    time.sleep(2)
                    self.move_window = wand.active_window()
                    node = get_node(self.move_window, 'window')
                    node.remove()
                    self.moving = True

                elif self.moving == True:
                    time.sleep(2)
                    to_window = wand.active_window()
                    node = get_node(to_window, 'window')
                    node.add_window(self.move_window)
                    self.moving = False



