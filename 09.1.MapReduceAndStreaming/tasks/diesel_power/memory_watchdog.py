from os import environ, getpid
from sys import stderr
from threading import Thread, Event
from time import sleep

from psutil import Process

VERBOSE = int(environ.get("VERBOSE", "0"))
SLEEP_PERIOD = float(environ.get("WATCHDOG_PERIOD", "100")) / 1000.0  # in msec
WIDTH = int(environ.get("PLOT_WIDTH", "100")) // 5 * 5
SELF_PROCESS = Process(getpid())


class MemoryWatchdog(Thread):
    """
    This class implements thread watching for current process memory consumption.
    Watchdog may be configured using the environment variables above.
    """

    def __init__(self, limit: int, is_baseline: bool = False) -> None:
        self._stop_event = Event()
        self.maximum_memory_usage = 0
        self.limit = limit
        self.limit_in_kib = limit // 1024
        self._is_baseline = is_baseline

        if VERBOSE:
            # To not interfere with pytest output.
            print("", file=stderr)
            header = ""
            for i in range(0, WIDTH - 10, 10):
                marking_in_kib = (i * self.limit // WIDTH) // 1024
                header += str(marking_in_kib).ljust(10)
            header = header.ljust(WIDTH)
            header += str(self.limit_in_kib)
            header = " " * 10 + header
            print(header, file=stderr)

        super().__init__()

    def run(self) -> None:
        while True:
            if self._stop_event.is_set():
                break
            usage = SELF_PROCESS.memory_info().rss
            usage_in_kib = usage // 1024
            self.maximum_memory_usage = max(self.maximum_memory_usage, usage)

            if VERBOSE:
                line = str(usage_in_kib).ljust(9) + "|" + "=" * min(WIDTH, usage * WIDTH // self.limit)
                if usage > self.limit:
                    line += min(10, (usage - self.limit) * WIDTH // self.limit) * "X"
                print(line, file=stderr)

            sleep(SLEEP_PERIOD)

        if not self._is_baseline:
            print("Maximum memory usage / limit (in KiB):",
                  self.maximum_memory_usage // 1024, "/", self.limit // 1024, file=stderr)

    def stop(self) -> None:
        self._stop_event.set()
