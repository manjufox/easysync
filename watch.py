import asyncio
from pathlib import Path
import glob

from watchdog.observers import Observer

from EventHandler import EventHandler


class MultiSession():
    def __init__(self, pathlist: list):
        self.pathlist = pathlist

    # defun handlers as many as pathlist
    def multihandler(self, options=None):
        handlerlist = [""] * len(self.pathlist)
        for i in range(len(handlerlist)):
            handlerlist[i] = EventHandler(options)
        return handlerlist

    def multiobserver(self):
        observerlist = [""] * len(self.pathlist)
        for i in range(len(observerlist)):
            observerlist[i] = Observer()
        return observerlist

    def multischeduler(self, multihandler: list, multiobserver: list, recursive=False):
        for i in range(len(self.pathlist)):
            multiobserver[i].schedule(
                multihandler[i], self.pathlist[i], recursive)

    async def _start(self, observer):
        observer.start()
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    async def multistart(self, multiobserver):
        await asyncio.gather(
            *[self._start(multiobserver[i]) for i in range(len(multiobserver))]
        )


if __name__ == "__main__":
    path = r"F:\program\python\git\easysync\test"
    for i in range(5):
        testpath = Path(path)/f"test{i}"
        testpath.mkdir(exist_ok=True)
    pathlist = list(glob.glob(f"{path}/*"))

    session = MultiSession(pathlist=pathlist)
    multihandler = session.multihandler()
    multiobserver = session.multiobserver()
    session.multischeduler(multihandler=multihandler,
                           multiobserver=multiobserver, recursive=True)

    loop = asyncio.get_event_loop()
    # tasks = [asyncio.create_task()
    print("\nsession start\n")
    print(f"{pathlist}")
    asyncio.run(session.main(multiobserver))
