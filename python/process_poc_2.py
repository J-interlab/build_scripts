import re
import json
import os 
import shutil
import utils
import zip_utils

folder_path = "public\\car_POC"
# asset_scenes_json = 45032171

# __pc__.js
SCRIPTS = [ 104470444, 106180258, 106180306, 106180307, 106180316, 106249649, 106251799 ]


assets = []
def visit(obj):
    if isinstance(obj, dict):
        for key in obj:
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
for car_index in [0]:
    txt = utils.get_file_contents(folder_path + '\\pc.json')
    pc_obj = json.loads(txt)
    txt = utils.get_file_contents(folder_path + '\\mobile.json')
    mobile_obj = json.loads(txt)
    
    assets = [] + SCRIPTS
    scenes = []
    for obj in pc_obj['scenes']:
        if obj['name'] == 'start' or obj['name'].startswith(f'interior{car_index}_') or obj['name'] == f'exterior{car_index}':
            scenes.append(int(obj['url'][:7]))
    print('scenes:', scenes)

    for scene in scenes:
        with open(f'{folder_path}\\{scene}.json', 'r', encoding='utf-8') as f:
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

    with open(f'{folder_path}\\pc{car_index}.json', 'w', encoding='utf-8') as f:
        json.dump(pc_obj, f)
    with open(f'{folder_path}\\mobile{car_index}.json', 'w', encoding='utf-8') as f:
        json.dump(mobile_obj, f)

    zip_utils.zip_and_delete(f'{folder_path}\\pc{car_index}.json')
    zip_utils.zip_and_delete(f'{folder_path}\\mobile{car_index}.json')




