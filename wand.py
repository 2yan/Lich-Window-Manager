import win32con
import win32gui
import win32api
import pandas as pd

gap = 10
#This func Stolen straight from stackoverflow
def isRealWindow(hWnd):
    '''Return True iff given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def get_windows():
    windows = pd.DataFrame()

    def callback(hwnd, ids):
        if not isRealWindow(hwnd):
            return
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)

        rect = win32gui.GetWindowRect(hwnd)
        windows.loc[hwnd, 'x'] = rect[0]
        windows.loc[hwnd, 'y'] = rect[1]
        windows.loc[hwnd, 'width'] = rect[2] -windows.loc[hwnd, 'x']
        windows.loc[hwnd, 'height'] = rect[3] - windows.loc[hwnd, 'y']
        windows.loc[hwnd, 'title'] = win32gui.GetWindowText(hwnd)
    win32gui.EnumWindows(callback, windows)
    windows.sort_values(['x', 'y'], inplace = True)
    windows = windows[- (windows['title'].str.contains('lich', case = False))]
    return windows

def move_window(hwnd, monitor, percent_x, percent_y, percent_wide, percent_height):
    x = int(percent_x * monitor.width) + monitor.x
    y = int(percent_y * monitor.height)+ monitor.y
    width = int(percent_wide * monitor.width)
    height = int(percent_height * monitor.height)
    print(width)
    print(height)
    _move_window(hwnd, x, y, width, height)

def _move_window(hwnd, x, y, width, height):
    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
    win32gui.MoveWindow(hwnd, x, y, width, height, True)

def fill_monitor(hwnd, monitor):

    x = monitor.x + int(gap/2)
    y = monitor.y + int(gap/2)

    width = monitor.width - (gap )
    height = monitor.height - (gap)
    win32gui.MoveWindow(int(hwnd), x, y , width , height, True)


def get_press(key):
    value = win32api.GetAsyncKeyState(key)
    if value < 0:
        return 1
    return 0


def minimize(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def win_h():
    return get_press(win32con.VK_LWIN) and get_press(ord('h'))

def win_v():
     return get_press(win32con.VK_LWIN) and get_press(ord('v'))

def win_click():
    return get_press(win32con.VK_LWIN) and get_press(win32con.VK_LBUTTON)

def active_window():
    return win32gui.GetForegroundWindow()
