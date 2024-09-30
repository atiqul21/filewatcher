import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file

    def log_change(self, event):
        event_type = 'Created' if event.event_type == 'created' else 'Deleted' if event.event_type == 'deleted' else 'Modified'
        message = f"{event_type}: {event.src_path}"
        logging.info(message)

        with open(self.log_file, 'a') as f:
            f.write(message + '\n')

    def on_created(self, event):
        self.log_change(event)

    def on_deleted(self, event):
        self.log_change(event)

    def on_modified(self, event):
        self.log_change(event)

def main(directory, log_file):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(directory):
        print(f"'{directory}' is not a directory.")
        sys.exit(1)

    event_handler = ChangeHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=False)

    try:
        observer.start()
        print(f"Watching directory: {directory} for changes. Logging to: {log_file}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filewatcher.py <directory_to_watch> <log_file>")
        sys.exit(1)

    directory_to_watch = sys.argv[1]
    log_file = sys.argv[2]

    main(directory_to_watch, log_file)
