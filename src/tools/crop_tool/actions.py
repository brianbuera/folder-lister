from .window import CropToolWindow

def realizar_recortes(parent, video):
    win = CropToolWindow(parent, video)

    if not win.winfo_exists():
        return False

    parent.wait_window(win)
    return win.confirmed