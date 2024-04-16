import threading
import time
# Singleton class to create a single thread of the class
class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.thread = None

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Singleton, cls).__new__(cls)
                cls._instance.thread = None
                cls._instance.lock = threading.Lock()
                cls._instance.stop_requested = False
        return cls._instance

    def start_thread(self, target, **kwargs):
        with self.lock:
            if self.thread is None or not self.thread.is_alive():
                self.stop_requested = False
                self.thread = threading.Thread(target=self.run_task, args=(target,), kwargs=kwargs)
                self.thread.start()
            return self.thread

    def run_task(self, task, **kwargs):
        while not self.stop_requested:
            result = task(**kwargs)
            if result is not True:
                break  # Exit the loop if the task fails or completes with a specific condition
            time.sleep(2)  # Adjust the sleep time as necessary

    def stop_thread(self):
        with self.lock:
            self.stop_requested = True
            if self.thread is not None:
                self.thread.join()
        return True

    def should_stop(self):
        return self.stop_requested