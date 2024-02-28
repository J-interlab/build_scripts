import re
import json
import os 
import shutil
import utils
import zip_utils

# asset_scenes_json = 45032171

# __pc__.js
# Mexico
SCRIPTS = [ 53360318, 53364187, 53361581, 53377893, 53393814, 53426882, 53459772, 53460526, 53465206, 53363951, 53492716, 53494610, 53549502 ]

# Europe project demo
# SCRIPTS = [ 156795639, 156795640, 156797159, 156797166, 156807412, 156807630, 156807632, 156807766, 156812040, 156853155 ]

assets = []
def visit(obj):
    if isinstance(obj, dict):
        for key in obj:
            if key == 'size':
                continue
            visit(obj[key])
    elif isinstance(obj, list):
        for child in obj:
            visit(child)
    elif isinstance(obj, int):
        if 10000000 <= obj <= 999999999:
            if not obj in assets and str(obj) in pc_obj['assets'].keys():
                assets.append(obj)
                visit(pc_obj['assets'][str(obj)])
    elif isinstance(obj, str):
        # print('str', child)
        pass

# car_index = 2
# for car_index in [0, 1, 2, 3, 4, 5, 8, 10, 11, 12]:
for car_index in [14]:
    txt = utils.get_file_contents('public\\mine\\pc.json')
    pc_obj = json.loads(txt)
    txt = utils.get_file_contents('public\\mine\\mobile.json')
    mobile_obj = json.loads(txt)
    
    assets = [] + SCRIPTS
    scenes = []
    for obj in pc_obj['scenes']:
        if obj['name'] == 'start' or obj['name'].startswith(f'interior{car_index}_') or obj['name'] == f'exterior{car_index}':
            scenes.append(int(obj['url'][:7]))
    print('scenes:', scenes)


    for scene in scenes:
        with open(f'public\\mine\\{scene}.json', 'r', encoding='utf-8') as f:
            txt = f.read()
        founds = re.findall("\d{8,9}", txt)

        for asset in founds:
            asset = int(asset)
            if not asset in assets:
                assets.append(asset)

    for asset in assets:
        try:
            visit(pc_obj['assets'][str(asset)])
        except Exception as e:
            print(e)
            pass

    print('total assets:', len(pc_obj['assets']))
    print(assets)
    keys = list(pc_obj['assets'].keys())
    for asset in keys:
        if not int(asset) in assets:
            pc_obj['assets'].pop(asset)
            mobile_obj['assets'].pop(asset)

    print(len(pc_obj['assets']), 'assets remained for car', car_index)

    with open(f'public\\mine\\pc{car_index}.json', 'w', encoding='utf-8') as f:
        json.dump(pc_obj, f)
    with open(f'public\\mine\\mobile{car_index}.json', 'w', encoding='utf-8') as f:
        json.dump(mobile_obj, f)

    zip_utils.zip_and_delete(f'public\\mine\\pc{car_index}.json')
    zip_utils.zip_and_delete(f'public\\mine\\mobile{car_index}.json')

def copy_files():
    root_folder = 'public/' + utils.get_timestamp()
    os.makedirs(root_folder)
    dst_root = root_folder + "/car2/files/assets"
    os.makedirs(dst_root)

    for asset in assets:
        src = f"public/mine1/files/assets/{asset}"
        dst = f"{dst_root}/{asset}"
        if os.path.exists(src):
            utils.copytree(src, dst)
        print(asset, pc_obj['assets'][str(asset)]['name'])

# copy_files()



