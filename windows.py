import ctypes, sys



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def windowsStartup():
    if not is_admin():
        import win32con, win32api
        # Re-run the program with admin rights
        win32api.ShellExecute(0, "runas", sys.executable, " ".join(sys.argv), None, 1)
        exit(0)
