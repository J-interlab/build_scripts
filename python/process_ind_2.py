import re
import json
import os 
import shutil
import utils
import zip_utils

# asset_scenes_json = 45032171

# __pc__.js
SCRIPTS = [ 54507063, 54507064, 54507065, 54507066, 54507067, 54507068, 54507069, 54507070, 54507071, 54507072, 54507073, 54507074, 54507075, 54507076, 54803874, 136987119, 136987394, 136987649, 137084157, 137084506, 137084546, 137112790, 137112896, 137112898, 137159939, 137159957, 146946562, 161386310 ]


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
            if not obj in assets:
                assets.append(obj)
                visit(pc_obj['assets'][str(obj)])
    elif isinstance(obj, str):
        # print('str', child)
        pass

# car_index = 2
for car_index in [2]:
    txt = utils.get_file_contents('public\\mine_ind\\pc.json')
    pc_obj = json.loads(txt)
    txt = utils.get_file_contents('public\\mine_ind\\mobile.json')
    mobile_obj = json.loads(txt)
    
    assets = [] + SCRIPTS
    scenes = []
    for obj in pc_obj['scenes']:
        if obj['name'] == 'start' or obj['name'].startswith(f'interior{car_index}') or obj['name'] == f'exterior{car_index}':
            scenes.append(int(obj['url'][:7]))
    print('scenes:', scenes)


    for scene in scenes:
        with open(f'public\\mine_ind\\{scene}.json', 'r', encoding='utf-8') as f:
            txt = f.read()
        founds = re.findall("\d{8,9}", txt)

        for asset in founds:
            asset = int(asset)
            if not asset in assets:
                assets.append(asset)
    
    for asset in assets:
        if asset == 137117865:
            err = 1
        try:
            visit(pc_obj['assets'][str(asset)])
        except Exception as e:
            print(e)
            pass

    print(assets)

    print('total assets:', len(pc_obj['assets']))
    keys = list(pc_obj['assets'].keys())
    for asset in keys:
        if not int(asset) in assets:
            pc_obj['assets'].pop(asset)
            mobile_obj['assets'].pop(asset)

    print(len(pc_obj['assets']), 'assets remained for car', car_index)

    with open(f'public\\mine_ind\\pc{car_index}.json', 'w', encoding='utf-8') as f:
        json.dump(pc_obj, f)
    with open(f'public\\mine_ind\\mobile{car_index}.json', 'w', encoding='utf-8') as f:
        json.dump(mobile_obj, f)

    zip_utils.zip_and_delete(f'public\\mine_ind\\pc{car_index}.json')
    zip_utils.zip_and_delete(f'public\\mine_ind\\mobile{car_index}.json')





