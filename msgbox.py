import ctypes

def msgbox(null, msgbox, title, mb, mb1):
    ctypes.windll.user32.MessageBoxW(null, msgbox, title, mb | mb1)