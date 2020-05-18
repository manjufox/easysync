import os
import time
import sys
import shutil

#import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#import dirsync
import dirsync


class EventHandler(FileSystemEventHandler):
    def __init__(self):
        pass

    def on_created(self,event):
        print(f"CREATED : {event.src_path}")

    def on_modified(self, event):
        print(f"MODIFIED : {event.src_path}")

    def on_deleted(self, event):
        print(f"DELETED : {event.src_path}")

    def on_moved(self, event):
        print(f"MOVED : {event.src_path}")

# class SuperHandler():
#     def __init__(self,source_A:str,source_B:str,options:list):
#         self.source_A = source_A
#         self.source_B = source_B
#         Handler_A = EventHandler(source_A)
#         Handler_B = EventHandler(source_B)

if __name__ == "__main__":
    path = r"F:\program\python\git\easysync\test"
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler,path,recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
