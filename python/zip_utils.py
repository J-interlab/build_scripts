import os
import zipfile

def zip_and_delete(path):
    root_path = os.path.abspath(os.path.curdir)
    os.chdir(os.path.dirname(path))
    basename = os.path.basename(path)    
    zipfile.ZipFile(basename + ".bin", mode='w').write(basename, compress_type = zipfile.ZIP_DEFLATED)
    filesize = os.stat(basename + ".bin").st_size
    os.remove(basename)
    os.chdir(root_path)
    return filesize
