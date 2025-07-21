import ctypes
def window(window):
    user32 = ctypes.windll.user32
    hwnd = user32.FindWindowW(None, window)
    if hwnd:
        print("f{hwnd}")
    else:
        print("not find")