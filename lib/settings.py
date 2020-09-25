"""
Global variables

By design, import no any other local module inside this file.
Vice verse, it'd produce circular dependent imports.
"""

from sys import platform
from os import environ as environmental_variables
from os.path import join as join_path
import os


WORKSPACE = {
    "name": "InstaBot",
    "path": os.getcwd() + "/data/",
}
OS_ENV = (
    "windows" if platform == "win32" else "osx" if platform == "darwin" else "linux"
)


def localize_path(*args):
    """ Join given locations as an OS path """

    if WORKSPACE["path"]:
        path = join_path(WORKSPACE["path"], *args)
        return path
    else:
        return None


class Settings:
    """ Globally accessible settings throughout whole project """

    # locations
    log_location = localize_path("logs")
    database_location = localize_path("db", "instabot.db")

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    )


