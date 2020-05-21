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
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class sync():
    def __init__(self, paths: list, options=None, recursive=False):
        self.multiobserver = multiobserver(pathlist)
        self.handlers = self.multiobserver.handler(options)
        self.observers = self.multiobserver.observer()
        self.multiobserver.scheduler(
            self.handlers, self.observers, recursive=recursive)

    async def _print(self, words):
        print(words)

    async def gather(self):
        tasks = [self.multiobserver.start(
            self.observers[i]) for i in range(len(self.observers))]
        return await asyncio.gather(*tasks, self._print("SESSION START"))

    def run(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
            asyncio.run(self.gather())
        else:
            future = asyncio.run_coroutine_threadsafe(self.gather(), loop)
        print(f"session start")
        return future


async def coro():
    i = 0
    while True:
        i = i + 1
        await asyncio.sleep(1)
        print(f"time : {i+1}")


if __name__ == "__main__":
    path = r"F:\program\python\git\easysync\test"
    for i in range(5):
        testpath = Path(path)/f"test{i}"
        testpath.mkdir(exist_ok=True)
    pathlist = list(glob.glob(f"{path}/*"))

    sync = sync(pathlist, recursive=True)
    sync.run()

    # session = multiobserver(pathlist=pathlist)
    # handler = session.handler()
    # observer = session.observer()
    # session.scheduler(handler=handler,
    #                        observer=observer, recursive=True)

    # loop = asyncio.get_event_loop()
    # # tasks = [asyncio.create_task()
    # print("\nsession start\n")
    # print(f"{pathlist}")
    # asyncio.run(session.multistart(observer))
