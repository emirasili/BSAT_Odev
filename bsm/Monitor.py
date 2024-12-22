import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"
WATCH_DIRECTORY = "/home/ubuntu/bsm/test"

class ChangeHandler(FileSystemEventHandler):
    def process(self, event):
        log_entry = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "timestamp": datetime.now().isoformat()
        }
        with open(LOG_FILE, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIRECTORY, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()