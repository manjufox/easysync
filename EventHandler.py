from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class EventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=["*"],ignore_patterns=None,ignore_directories=False,case_sensitive=False):
        super(EventHandler, self).__init__(patterns=patterns, ignore_patterns=ignore_patterns,
                                            ignore_directories=ignore_directories, case_sensitive=case_sensitive)

    def on_created(self, event):
        print(f"CREATED : {event.src_path}")
        

    def on_modified(self, event):
        print(f"MODIFIED : {event.src_path}")

    def on_deleted(self, event):
        print(f"DELETED : {event.src_path}")

    def on_moved(self, event):
        print(f"MOVED : {event.src_path}")