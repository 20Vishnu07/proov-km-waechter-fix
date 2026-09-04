# log_util.py
# A homemade logger from 2013. Updated to remove the permanently-dead debug
# branch and to use a context manager in flush_log so a write failure cannot
# silently discard log lines.

import time

LOG_LINES: list[str] = []   # module-level buffer; flushed by flush_log()


def log(message: str) -> None:
    """Append a timestamped line to the in-memory buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered lines to the log file and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
