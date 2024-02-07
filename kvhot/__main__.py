import argparse
import importlib.metadata
import os
import subprocess
import sys
from typing import Union

from watchfiles import DefaultFilter, watch
from watchfiles.main import FileChange

try:
    __version__ = importlib.metadata.version("kvhot")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


def check_target_dir(path: str) -> str:
    """
    Checks if the target_dir is exists and there is main.py inside it.
    """
    path = os.path.abspath(path)

    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"No directory '{path}' exists")
    elif not os.path.isfile(os.path.join(path, "main.py")):
        raise argparse.ArgumentTypeError(
            f"No 'main.py' file exists in '{path}'"
        )

    return path


parser = argparse.ArgumentParser(
    prog="kvhot",
    description="Automatically restarts the Kivy application "
    "whenever files within the project directory change.",
)
parser.add_argument(
    "target_dir",
    type=check_target_dir,
    help="directory of the entry-point (main.py) of the kivy application",
)
parser.add_argument(
    "--width", type=int, default=350, help="width of the window."
)
parser.add_argument(
    "--height", type=int, default=650, help="height of the window."
)
parser.add_argument(
    "--top", type=int, default=0, help="top position of the window."
)
parser.add_argument(
    "--left", type=int, default=0, help="left position of the window."
)
parser.add_argument(
    "-b",
    "--blacklist",
    nargs="+",
    help="exclude specific files/dirs from being monitored.",
)
parser.add_argument(
    "-V", "--version", action="version", version="%(prog)s " + __version__
)


def log(s: str):
    """
    Simple log system.
    """
    BLUE = "\033[34m"
    BOLD = "\033[01m"
    RESET = "\033[0m"
    msg = (
        f"[{BLUE}{BOLD}KVHOT{RESET}]: {s}"
        if sys.platform != "win32"
        else f"[KVHOT]: {s}"
    )
    print(msg)


def filter_blacklist_paths(
    blacklisted_paths: Union[list[str], None]
) -> list[str]:

    if not blacklisted_paths:
        return []

    paths: list[str] = []

    for path in blacklisted_paths:
        abs_path: str = os.path.abspath(path)

        if os.path.exists(abs_path):
            paths.append(abs_path)

    return paths


class Watcher:
    """
    Class implementing the logic.
    """

    _process: "subprocess.Popen[bytes]"
    target_dir: str
    main_py: str
    blacklist_filter: DefaultFilter

    def __init__(
        self,
        target_dir: str,
        width: int,
        height: int,
        top: int,
        left: int,
        blacklist: Union[list[str], None],
    ):
        self.target_dir = target_dir
        self.main_py = os.path.join(self.target_dir, "main.py")
        self.blacklist_filter = DefaultFilter(
            ignore_paths=filter_blacklist_paths(blacklist)
        )

        os.environ["KCFG_GRAPHICS_WIDTH"] = str(width)
        os.environ["KCFG_GRAPHICS_HEIGHT"] = str(height)
        os.environ["KCFG_GRAPHICS_POSITION"] = "custom"
        os.environ["KCFG_GRAPHICS_TOP"] = str(top)
        os.environ["KCFG_GRAPHICS_LEFT"] = str(left)

    def _start_app(self, changes: Union[FileChange, None] = None):

        if not changes:
            log("Starting app...")
            log(f"Running {self.main_py}")
            log("Press CTRL+C to stop.")
        else:
            change_type = changes[0].raw_str().title()
            file_path = os.path.abspath(changes[1])

            log(f"{change_type} {file_path}, restarting app...")
            self._process.kill()

        self._process = subprocess.Popen([sys.executable, self.main_py])

    def _stop_app(self):
        if self._process:
            self._process.kill()

    def start(self):
        """
        Starts the app (runs main.py) and watches the target_dir
        """

        self._start_app()

        try:
            for changes in watch(
                self.target_dir, watch_filter=self.blacklist_filter
            ):
                self._start_app(changes.pop())
        except KeyboardInterrupt:
            self._stop_app()
            log("Stopping")


def main():
    args = vars(parser.parse_args())
    w = Watcher(**args)
    w.start()


if __name__ == "__main__":
    main()
