import subprocess
from subprocess import PIPE
import os

cmd = ["osascript", os.path.join(os.path.dirname(__file__), "printAppTitle.scpt")]

def getInfo() -> str:
    p = subprocess.run(cmd, stdout=PIPE)
    return str(p.stdout, "utf8").strip()


def getApp(info: str) -> str:
    return info.split('","')[0][1:]


def getTitle(info: str) -> str:
    return info.split('","')[1][:-1]

