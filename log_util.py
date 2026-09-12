# log_util.py
# Eigener Logger. Das logging-Modul war uns 2013 "zu viel Magie".
# (A homemade logger. The logging module felt like "too much magic" in 2013.)

import time

LOG_LINES: list[str] = []               # global state, shared by everyone who imports this
DEBUG = False


def log(message: str) -> None:
    """Timestamp *message*, print it, and buffer it for the next flush_log call."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a DEBUG-prefixed message — only active when DEBUG is True.

    DEBUG has been False since 2014; this branch is currently dead.
    """
    if DEBUG:                               # was: if DEBUG == True
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Append all buffered log lines to *path*, then clear the buffer."""
    with open(path, "a") as f:             # context manager — file always closed
        for line in LOG_LINES:
            f.write(line + "\n")
    del LOG_LINES[:]                        # so leert man 2013 eine Liste (2013's way to clear a list)
