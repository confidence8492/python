import ctypes
from ctypes import wintypes

# 判斷系統是 64-bit 或 32-bit，定義 LRESULT
if ctypes.sizeof(ctypes.c_void_p) == 8:
    LRESULT = ctypes.c_longlong
else:
    LRESULT = ctypes.c_long

# DLL 載入
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# 常數
WS_OVERLAPPEDWINDOW = 0x00CF0000
CW_USEDEFAULT = 0x80000000
CW_USEDEFAULT_SIGNED = -2147483648  # 對 ctypes.c_int 的 signed 轉換
WM_DESTROY = 0x0002




# WinAPI HANDLE 類型別名
HCURSOR = wintypes.HANDLE
HICON = wintypes.HANDLE
HBRUSH = wintypes.HANDLE

# WNDPROC 函式原型
WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

# RECT 結構
class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long),
    ]

# MSG 結構
class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", wintypes.POINT)
    ]

# WNDCLASS 結構
class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]

# 設定 DefWindowProcW 參數和回傳型態
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = LRESULT

# 視窗處理函式
@WNDPROC
def WindowProc(hwnd, msg, wParam, lParam):
    if msg == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0
    return user32.DefWindowProcW(hwnd, msg, wParam, lParam)

def main(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE):
    hInstance = kernel32.GetModuleHandleW(None)
    className = "MyPythonWindowClass"

    # 註冊視窗類別
    wndclass = WNDCLASS()
    wndclass.lpfnWndProc = WindowProc
    wndclass.hInstance = hInstance
    wndclass.lpszClassName = className
    wndclass.hCursor = user32.LoadCursorW(None, 32512)  # IDC_ARROW
    wndclass.style = 0
    wndclass.cbClsExtra = 0
    wndclass.cbWndExtra = 0
    wndclass.hIcon = None
    wndclass.hbrBackground = 6  # COLOR_WINDOW + 1
    wndclass.lpszMenuName = None

    if not user32.RegisterClassW(ctypes.byref(wndclass)):
        raise ctypes.WinError(ctypes.get_last_error())

    # 調整視窗大小 (考慮邊框)
    rect = RECT(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    if not user32.AdjustWindowRect(ctypes.byref(rect), WS_OVERLAPPEDWINDOW, False):
        raise ctypes.WinError(ctypes.get_last_error())

    width = rect.right - rect.left
    height = rect.bottom - rect.top

    # 指定 CreateWindowExW 參數與回傳型態
    user32.CreateWindowExW.argtypes = [
        wintypes.DWORD,     # dwExStyle
        wintypes.LPCWSTR,   # lpClassName
        wintypes.LPCWSTR,   # lpWindowName
        wintypes.DWORD,     # dwStyle
        ctypes.c_int,       # X
        ctypes.c_int,       # Y
        ctypes.c_int,       # nWidth
        ctypes.c_int,       # nHeight
        wintypes.HWND,      # hWndParent
        wintypes.HMENU,     # hMenu
        wintypes.HINSTANCE, # hInstance
        wintypes.LPVOID     # lpParam
    ]
    user32.CreateWindowExW.restype = wintypes.HWND

    # 建立視窗
    hwnd = user32.CreateWindowExW(
        0,
        className,
        WINDOW_TITLE,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT_SIGNED,
        CW_USEDEFAULT_SIGNED,
        width,
        height,
        None,
        None,
        hInstance,
        None
    )

    if not hwnd:
        raise ctypes.WinError(ctypes.get_last_error())

    user32.ShowWindow(hwnd, 1)  # SW_SHOWNORMAL
    user32.UpdateWindow(hwnd)

    # 訊息迴圈
    msg = MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))



