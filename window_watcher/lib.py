import sys
from typing import Callable
from functools import lru_cache


def get_current_window_linux() -> dict:
    from . import xlib
    window = xlib.get_current_window()

    if window is None:
        cls = "unknown"
        name = "unknown"
    else:
        cls = xlib.get_window_class(window)
        name = xlib.get_window_name(window)

    return {"appname": cls, "title": name}


def get_current_window_macos() -> dict:
    from . import macos
    info = macos.getInfo()
    app = macos.getApp(info)
    title = macos.getTitle(info)

    return {"title": title, "appname": app}


def get_current_window_windows() -> dict:
    from . import windows
    window_handle = windows.get_active_window_handle()
    app = windows.get_app_name(window_handle)
    title = windows.get_window_title(window_handle)

    if app is None:
        app = "unknown"
    if title is None:
        title = "unknown"

    return {"appname": app, "title": title}


@lru_cache(1)
def get_current_window_func() -> Callable:
    if sys.platform.startswith("linux"):
        return get_current_window_linux
    elif sys.platform == "darwin":
        return get_current_window_macos
    elif sys.platform in ["win32", "cygwin"]:
        return get_current_window_windows
    else:
        raise Exception("Unknown platform: {}".format(sys.platform))
