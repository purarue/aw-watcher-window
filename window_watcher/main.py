import sys
import os
import csv
import re
import argparse
import traceback
from time import sleep, time
from typing import Dict, List

from logzero import logger, logfile

from .lib import get_current_window_func

DEFAULT_POLL_TIME = 1.0


def main():

    # setup logging
    logfile("/tmp/window-watcher.log", maxBytes=1e7, backupCount=1)

    # get default data file
    # use XDG dir, else ~/.local/share/
    data_dir: str = os.environ.get(
        "XDG_DATA_HOME", os.path.join(os.environ["HOME"], ".local", "share")
    )
    datafile: str = os.path.join(data_dir, "window_events.csv")

    args = parse_args(DEFAULT_POLL_TIME, datafile)

    if sys.platform.startswith("linux") and (
        "DISPLAY" not in os.environ or not os.environ["DISPLAY"]
    ):
        raise Exception("DISPLAY environment variable not set")

    # note: this just throws a runtime error on mac for me, seems to be related
    # to multiprocessing. I left the note in the README for how to configure this,
    # don't think the popup is necessary
    # https://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing
    # if sys.platform == "darwin":
    # from . import macos
    # macos.background_ensure_permissions()

    logger.info("aw-watcher-window started")

    ignore_strings: List[str] = args.ignore or []
    ignore_regexes: List[re.Pattern] = [re.compile(r) for r in ignore_strings]
    logger.debug("Ignoring regex patterns: {}".format(ignore_regexes))

    run_loop(
        datafile=args.datafile, poll_time=args.poll_time, ignore_regexes=ignore_regexes
    )


def parse_args(default_poll_time: float, default_datafile: str):

    parser = argparse.ArgumentParser(
        "A cross platform window watcher.\nSupported on: Linux (X11), macOS and Windows."
    )
    parser.add_argument(
        "-d",
        "--datafile",
        type=str,
        default=default_datafile,
        help="csv file to log events to",
    )
    parser.add_argument(
        "-p",
        "--poll-time",
        dest="poll_time",
        type=float,
        default=default_poll_time,
        help="seconds to wait between polling for window events",
    )
    parser.add_argument(
        "-i",
        "--ignore-regex",
        dest="ignore",
        action="append",
        default=[],
        help="if the application or window title matches this regex, don't write it to the file. Can be supplied multiple times",
    )
    return parser.parse_args()


def timestamp() -> int:
    return int(time())


def get_window_info() -> Dict[str, str]:
    try:
        return get_current_window_func()()
    except Exception as e:
        logger.error("Exception thrown while trying to get active window: {}".format(e))
        traceback.print_exc()
        return {"appname": "unknown", "title": "unknown"}


def write_to_file(datafile, event_info):
    """
    Write an event to the file
    Better to do this after each event, instead of keeping the file open
    """
    with open(datafile, "a") as dataf:
        data_writer = csv.writer(
            dataf, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        data_writer.writerow(event_info)

def matches_ignore_regex(appname: str, title: str, ignore_regexes: List[re.Pattern]) -> bool:
    for pat in ignore_regexes:
        if bool(re.search(pat, appname)):
            logger.debug(f"{appname} matched {pat}, skipping write to file")
            return True
        if bool(re.search(pat, title)):
            logger.debug(f"{title} matched {pat}, skipping write to file")
            return True
    return False


def run_loop(datafile: str, poll_time: float, ignore_regexes: List[re.Pattern]):
    # if this fails to do so the first time, crash the program
    # otherwise -- this could be failing in the background with no warning
    last_window: dict = get_current_window_func()()
    # when this window was focused
    last_window_started_at: int = timestamp()

    while True:
        current_window: dict = get_window_info()

        # if the window now is the same as before, do nothing
        if (
            current_window["appname"] == last_window["appname"]
            and current_window["title"] == last_window["title"]
        ):
            pass
        else:
            # if its different, write the previous window we were focusing to the file
            now: int = timestamp()
            if not matches_ignore_regex(last_window["appname"], last_window["title"], ignore_regexes):
                # write to file
                window_row = [
                    last_window_started_at,
                    now - last_window_started_at,
                    last_window["appname"],
                    last_window["title"],
                ]
                logger.debug(window_row)
                write_to_file(datafile, window_row)
            # even if we're not writing to the file,
            # we should still update the last_window and when it started, so
            # that when it changes away from this window we have accurate
            # information
            last_window = current_window
            last_window_started_at = now

        sleep(poll_time)
