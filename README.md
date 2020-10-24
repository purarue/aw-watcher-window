## window_watcher

This is a fork of [`aw-watcher-window`](https://github.com/ActivityWatch/aw-watcher-window) which doesn't connect to ActivityMonitor.

It uses the core cross platform code, and instead logs the events to a CSV file. (defaults to `${XDG_DATA_DIR:-$HOME/.local/share}/window_events.csv`)

Installs as `window_watcher`, as to not cause possible name conflicts.

```
usage: A cross platform window watcher.
Supported on: Linux (X11), macOS and Windows.
       [-h] [--datafile DATAFILE] [--poll-time POLL_TIME]

optional arguments:
  -h, --help              show this help message and exit
  --datafile DATAFILE     csv file to log events to
  --poll-time POLL_TIME   seconds to wait between polling for window events
```

Similar to `aw-watcher-window`, this logs when the event started, the duration the window was focused, the application name and the window title. An excerpt:

```
1599589324,1,Alacritty,Alacritty
1599589325,6,firefoxdeveloperedition,csv — CSV File Reading and Writing — Python 3.8.5 documentation - Firefox Developer Edition
```

## Install

To install with pip:

```
pip install git+https://github.com/seanbreckenridge/aw-watcher-window
```

Converted from using `poetry` to `setuptools`, I've tested this on Linux (X11) and MacOS (Catalina)

I haven't tested this on windows (particularly the install process, I haven't dealt with peotry before, but [seems there are other dependencies](https://github.com/ActivityWatch/aw-watcher-window/blob/master/pyproject.toml) you may have to install for those systems)

## Note to macOS users

To log current window title the terminal needs access to macOS accessibility API.
This can be enabled in `System Preferences > Security & Privacy > Accessibility`, then add the Terminal to this list. If this is not enabled the watcher can only log current application, and not window title.

