import asyncio
from pathlib import Path
import glob
import time

from watchdog.observers import Observer

from eventhandler import EventHandler


class multiobserver():
    def __init__(self, pathlist: list):
        self.pathlist = pathlist

    # defun handlers as many as pathlist
    def handler(self, options=None):
        handlerlist = [""] * len(self.pathlist)
        for i in range(len(handlerlist)):
            handlerlist[i] = EventHandler(options)
        return handlerlist

    def observer(self):
        observerlist = [""] * len(self.pathlist)
        for i in range(len(observerlist)):
            observerlist[i] = Observer()
        return observerlist

    def scheduler(self, handler: list, observer: list, recursive=False):
        for i in range(len(self.pathlist)):
            observer[i].schedule(
                handler[i], self.pathlist[i], recursive)

    async def start(self, observer):
        observer.start()
        while True:
            await asyncio.sleep(1)


class sync():
    def __init__(self, paths: list, options=None, recursive=False):
        self.multiobserver = multiobserver(pathlist)
        self.handlers = self.multiobserver.handler(options)
        self.observers = self.multiobserver.observer()
        self.multiobserver.scheduler(
            self.handlers, self.observers, recursive=recursive)

    async def _print(self, words):
        print(words)

    async def tasks(self):
        while True:
            await asyncio.sleep(1)
            print(asyncio.all_tasks())

    async def gather(self):
        tasks = [self.multiobserver.start(
            self.observers[i]) for i in range(len(self.observers))]
        return await asyncio.gather(*tasks)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.gather())


if __name__ == "__main__":
    path = r"F:\program\python\git\easysync\test"
    for i in range(5):
        testpath = Path(path)/f"test{i}"
        testpath.mkdir(exist_ok=True)
    pathlist = list(glob.glob(f"{path}/*"))
    sync = sync(pathlist, recursive=True)
    sync.run()
    print("done")
