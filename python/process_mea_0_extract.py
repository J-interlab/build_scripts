import os
import sys
import shutil
import zipfile
import re


FOLDER_PATH = "public\\car_mea"

downloads = 'C:\\Users\\SKYDEV\\Downloads'
pattern = 'car_mea( \(\d+\))?\.zip'
destination = os.path.relpath(os.path.join(FOLDER_PATH, os.pardir))

try:
    shutil.rmtree(FOLDER_PATH)
except Exception as e:
    pass

files = os.listdir(downloads)
max_time = -1
for filename in files:
    if re.match(pattern, filename) is not None:
        full_path = os.path.join(downloads, filename)
        status = os.stat(full_path)
        if status.st_ctime > max_time:
            max_time = status.st_ctime
            filename_found = filename
if max_time < 0:
    print('build not found, end script')
    exit(0)

print('The most recent build is', filename_found)


# copy and unzip file

src = os.path.join(downloads, filename_found)

products_dir = os.path.join(FOLDER_PATH)
# if os.path.isdir(products_dir):
#     print('products folder found')
#     temp = str(round(datetime.datetime.now().timestamp()))
#     temp_dir = os.path.join('temp', temp)
#     shutil.move(products_dir, temp_dir)
#     print('products folder renamed as temp')

## extract zip file
with zipfile.ZipFile(src, 'r') as zip_ref:
    zip_ref.extractall(products_dir)

print('build extracted')




# src = f'{FOLDER_PATH}\\files'
# dst = f'{FOLDER_PATH}\\filesBackup'
# os.mkdir('public\\car_mea\\aaa')
# try:
#     os.rename(src, dst)
#     os.mkdir(src)
#     os.mkdir(src + '/assets')
# except NameError as e:
#    print(e)
# except PermissionError as e:
#     print(e)



