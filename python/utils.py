
import time
import os, shutil

def get_timestamp():
    return str(int(time.time() * 1000))


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def get_file_contents(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        txt = f.read()
        return txt