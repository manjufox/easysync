import time
import asyncio
from pathlib import Path
import glob

#import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):
    # def __init__(self,patterns=None,ignore_patterns=None, ignore_directories=False, case_sensitive=False):
    #     super(EventHandler,self).__init__(patterns=patterns,ignore_patterns=ignore_patterns,
    #                                         ignore_directories=ignore_directories, case_sensitive=case_sensitive)

    def on_created(self,event):
        print(f"CREATED : {event.src_path}")

    def on_modified(self, event):
        print(f"MODIFIED : {event.src_path}")

    def on_deleted(self, event):
        print(f"DELETED : {event.src_path}")

    def on_moved(self, event):
        print(f"MOVED : {event.src_path}")

class MultiSession():
    def __init__(self,pathlist:list,options:dict=None):
        self.pathlist = pathlist
        self.options = options
        # self.patterns=self.options["patterns"]
        # self.igignore_patterns=self.options["ignore_patterns"]
        # self.ignore_directories=self.options["ignore_directories"]
        # self.case_sensitive=self.options["case_sensitive"]
        
    #defun handlers as many as pathlist 
    def multihandler(self):
        handlerlist = [""] * len(self.pathlist)
        for i in range(len(handlerlist)):
            handlerlist[i] = EventHandler()
        return handlerlist

    def multiobserver(self):
        observerlist = [""] * len(self.pathlist)
        for i in range(len(observerlist)):
            observerlist[i] = Observer()
        return observerlist

    def multischeduler(self,multihandler:list,multiobserver:list,recursive=False):
        for i in range(len(self.pathlist)):
            multiobserver[i].schedule(multihandler[i],self.pathlist[i],recursive)
        

    async def _start(self,observer):
        observer.start()
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    
    async def main(self,multiobserver):
        await asyncio.gather(
            self._start(multiobserver[0]),
            self._start(multiobserver[1])
            
    )
    
    # async def sessionstart(self,multiobserver:list):
    #     await asyncio.wait([self._start(observer) for observer in multiobserver])


if __name__ == "__main__":
    path = r"F:\program\python\git\easysync\test"
    for i in range(2):
        testpath = Path(path)/f"test{i}"
        testpath.mkdir(exist_ok=True)
    pathlist = list(glob.glob(f"{path}/*"))

    session = MultiSession(pathlist=pathlist)
    multihandler = session.multihandler()
    multiobserver = session.multiobserver()
    session.multischeduler(multihandler=multihandler,multiobserver=multiobserver,recursive=True)

    loop = asyncio.get_event_loop()
    #tasks = [asyncio.create_task()
    print("\nsession start\n")
    print(f"{pathlist}")
    asyncio.run(session.main(multiobserver))
    #loop.run_until_complete(tasks)