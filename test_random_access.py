import random
from pathlib import Path
import shutil
import asyncio
import os
import time

base_path = Path(r"F:\program\python\git\easysync\test")
paths = list(base_path.glob("*"))
paths_num = len(paths)
files_num = len(list(base_path.glob("**/*")))


def select_access_path():
    return random.choice(paths)


def create_file():
    path = select_access_path()
    filename = f"test_{random.randrange(0,files_num+100)}.txt"
    file_path = path/filename
    file_path.touch(exist_ok=True)
    print(f"CREATE : {file_path}")


def move_file():
    files = [i for i in list(base_path.glob("**/*")) if i.is_file()]
    file_path = random.choice(files)
    filename = file_path.stem
    rename = filename + str(random.randrange(0, files_num+100))
    renamed = file_path.rename(file_path/str(rename+file_path.suffix))
    print(f"MOVED : {renamed}")


def delete_file():
    files = [i for i in list(base_path.glob("**/*")) if i.is_file()]
    file_path = random.choice(files)
    os.remove(str(file_path))
    print(f"DELETED : {file_path}")


def callback(func):
    func()


num = 1000

for i in range(num):
    funcs = [create_file, move_file, delete_file]
    rand_func = random.choice(funcs)
    try:
        callback(rand_func)
        time.sleep(1)
    except :
        pass