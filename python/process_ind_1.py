import os
import shutil

from zip_utils import zip_and_delete
from image_utils_ind import resize_and_copy
# zip files
sum = 0
zip_sum = 0
counter = 0
json_files = []
for (dirpath, dirnames, filenames) in os.walk("public\\mine_ind"):
    if len(filenames) == 1:
        
        filename = filenames[0]
        path = os.path.join(dirpath, filename)
        # print(path)

        if filename.endswith(".json"):
            size = os.stat(path).st_size
            if size > 100000:
                json_files.append(path)


for path in json_files:
    size = os.stat(path).st_size
    print("json:", counter, path, size)
    counter += 1
    zip_size = zip_and_delete(path)
    sum += size
    zip_sum += zip_size

print("json", sum, zip_sum)

# copy images
sum = 0
new_sum = 0
counter = 0
for (dirpath, dirnames, filenames) in os.walk("public\\mine_ind"):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        if filename.endswith(".png") or filename.endswith(".jpg"):        
            size = os.stat(path).st_size
            print("image:", counter, path, size)
            counter += 1
            ret = resize_and_copy(path)
            sum += size
            new_sum += ret
        else:
            if path.startswith("public\\mine_ind\\files"):
                dst = "public\\mine_ind\\mobilefiles" + path[21:]
                dst_dir = os.path.dirname(dst)
                try:
                    os.makedirs(dst_dir)
                except:
                    pass
                shutil.copyfile(path, dst)
            
print("image", sum, new_sum)

# json
with open('public\\mine_ind\\config.json', 'r', encoding='utf-8') as f:
    txt = f.read()

txt_pc = txt
for path in json_files:
    x = path[16:].replace("\\", "/")
    y = x + ".bin"
    txt_pc = txt_pc.replace(x, y)

with open('public\\mine_ind\\pc.json', 'w', encoding='utf-8') as f:
    f.write(txt_pc)

txt_mobile = txt_pc.replace('files/assets/', 'mobilefiles/assets/')
with open('public\\mine_ind\\mobile.json', 'w', encoding='utf-8') as f:
    f.write(txt_mobile)

# zip_and_delete('public\\mine_ind\\pc.json')
# zip_and_delete('public\\mine_ind\\mobile.json')

os.remove('public\\mine_ind\\__start__.js')
os.remove('public\\mine_ind\\logo.png')
os.remove('public\\mine_ind\\playcanvas-stable.min.js')
os.remove('public\\mine_ind\\index.html')
os.remove('public\\mine_ind\\config.json')

with open('public\\mine_ind\\__settings__.js', 'r', encoding='utf-8') as f:
    txt = f.read()
x = txt.replace('config.json', 'pc.json.bin')
with open('public\\mine_ind\\__pc__.js', 'w', encoding='utf-8') as f:
    f.write(x)

x = txt.replace('config.json', 'mobile.json.bin')
with open('public\\mine_ind\\__mobile__.js', 'w', encoding='utf-8') as f:
    f.write(x)
os.remove('public\\mine_ind\\__settings__.js')



# shutil.copyfile('python\\app.js', 'public\\mine\\app.js')
# shutil.copyfile('python\\pc.html', 'public\\mine\\pc.html')
# shutil.copyfile('python\\mobile.html', 'public\\mine\\mobile.html')


# files/assets/45412903/1/body.json