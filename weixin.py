import win32api
import win32con
import win32gui
import time
import win32clipboard as w


def find_window(chatroom):
    win = win32gui.FindWindow(None, chatroom)
    if win != 0:
        win32gui.ShowWindow(win, win32con.SW_SHOWMINIMIZED)
        win32gui.ShowWindow(win, win32con.SW_SHOWNORMAL)
        win32gui.ShowWindow(win, win32con.SW_SHOW)
        win32gui.SetWindowPos(win, win32con.HWND_TOPMOST, 100, 100, 300, 300, win32con.SWP_SHOWWINDOW)
        win32gui.SetForegroundWindow(win)  # 获取控制
        time.sleep(1)
    else:
        print('请注意：找不到【%s】这个人（或群），请激活窗口！' % chatroom)
        exit()

def close_window(chatroom):
    win = win32gui.FindWindow(None, chatroom)
    time.sleep(3)
    win32gui.ShowWindow(win, win32con.SW_SHOWMINIMIZED)


def set_text(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()


def ctrl_v():
    win32api.keybd_event(17,0,0,0)  #ctrl键位码是17
    win32api.keybd_event(86,0,0,0)  #v键位码是86
    win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
 
def alt_s():
    win32api.keybd_event(18, 0, 0, 0)    #Alt键位码
    win32api.keybd_event(83,0,0,0) #s键位码
    win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
    win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)

def send_text(chatroom,text):
    find_window(chatroom)
    #文字首行留空，防止带表情复制不完全
    set_text(" "+text)
    time.sleep(1)
    ctrl_v()
    time.sleep(1)
    alt_s()
    close_window(chatroom)

# if __name__ == '__main__':

#     text = '123345'
#     send_text('文件传输助手', text)