import datetime
from pathlib import Path
import hashlib
import sys
import os
import json

def force_decode(b: bytes):
    try:
        return b.decode(json.detect_encoding(b))
    except UnicodeDecodeError:
        return b.decode(errors= "backslashreplace")

def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path,"rb") as f:
        for byte_block in iter(lambda: f.read(16777216),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

def current_time(seconds_also=False):
    return datetime.datetime.now().strftime('%d.%m.%Y_%H.%M' if not seconds_also else '%d.%m.%Y_%H.%M.%S')

def tree(dir_path: Path, level: int=-1, limit_to_directories: bool=False, length_limit: int=sys.maxsize):
    global tree_files, tree_directories
    space =  '    '
    branch = '│   '
    tee =    '├── '
    last =   '└── '
    dir_path = Path(dir_path)
    level = int(-1)
    limit_to_directories = False
    def inner(dir_path: Path, prefix: str='', level=-1):
        global tree_files, tree_directories
        try:
            contents = list(dir_path.iterdir())
            pointers = [tee] * (len(contents) - 1) + [last]
            for pointer, path in zip(pointers, contents):
                if path.is_dir():
                    yield prefix + pointer + path.name
                    extension = branch if pointer == tee else space 
                    yield from inner(path, prefix=prefix+extension, level=level-1)
                elif not limit_to_directories:
                    yield prefix + pointer + path.name
        except Exception as err:
            print(err)
    return inner(dir_path, level=level)

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def secure_delete_file(path, passes=1):
    length = os.path.getsize(path)
    with open(path, "br+", buffering=-1) as f:
        for i in range(passes):
            f.seek(0)
            f.write(os.urandom(length))
        f.close()
    os.remove(path)
