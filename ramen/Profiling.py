import functools
import os
import threading
import time

import psutil

_process = psutil.Process(os.getpid())


def profile_stage(name=None, sample_interval=0.01):
    """
    Decorator for profiling runtime and peak RSS memory.

    Stores results in:
        self.profile[stage_name] = {
            "runtime_seconds": float,
            "peak_memory_mb": float
        }
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):

            if not hasattr(self, "profile"):
                self.profile = {}

            peak_rss = [_process.memory_info().rss]
            stop_event = threading.Event()

            def monitor():
                while not stop_event.is_set():
                    rss = _process.memory_info().rss
                    if rss > peak_rss[0]:
                        peak_rss[0] = rss
                    time.sleep(sample_interval)

            monitor_thread = threading.Thread(
                target=monitor,
                daemon=True
            )

            start = time.perf_counter()

            monitor_thread.start()

            try:
                result = func(self, *args, **kwargs)
            finally:
                stop_event.set()
                monitor_thread.join()

            runtime = time.perf_counter() - start

            self.profile[name or func.__name__] = {
                "runtime_seconds": runtime,
                "peak_memory_mb": peak_rss[0] / (1024 ** 2),
            }

            return result

        return wrapper

    return decorator