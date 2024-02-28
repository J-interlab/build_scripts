from ast import excepthandler
import re
import json
import os 
import shutil
import utils
import zip_utils
FOLDER_PATH = "public\\car_mea"
# asset_scenes_json = 45032171

# __pc__.js
SCRIPTS = [ 74887947, 73835434, 73835435, 73835436, 73835441, 73835444, 73835445, 73835446, 73835483, 73835484, 74786036, 74798387, 74798826, 74798827, 74799147, 74819506, 74895174]


assets = []
CAR_INDEX = 9
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
for car_index in [11]:
    txt = utils.get_file_contents(FOLDER_PATH + '\\pc.json')
    pc_obj = json.loads(txt)
    txt = utils.get_file_contents(FOLDER_PATH + '\\mobile.json')
    mobile_obj = json.loads(txt)
    
    assets = [] + SCRIPTS
    scenes = []
    for obj in pc_obj['scenes']:
        if obj['name'] == 'start' or obj['name'].startswith(f'interior{car_index}') or obj['name'].startswith(f'exterior{car_index}'):
            scenes.append(int(obj['url'][:7]))
    print('scenes:', scenes)


    for scene in scenes:
        with open(f'{FOLDER_PATH}\\{scene}.json', 'r', encoding='utf-8') as f:
            txt = f.read()
        founds = re.findall("\d{8,9}", txt)

        for asset in founds:
            asset = int(asset)
            if not asset in assets:
                assets.append(asset)
    
    for asset in assets:
        if asset == 53267968:
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

    with open(f'{FOLDER_PATH}\\pc{car_index}.json', 'w', encoding='utf-8') as f:
        json.dump(pc_obj, f)
    with open(f'{FOLDER_PATH}\\mobile{car_index}.json', 'w', encoding='utf-8') as f:
        json.dump(mobile_obj, f)

    zip_utils.zip_and_delete(f'{FOLDER_PATH}\\pc{car_index}.json')
    zip_utils.zip_and_delete(f'{FOLDER_PATH}\\mobile{car_index}.json')

    # copy resources

    src = f'{FOLDER_PATH}/files'
    try:
        dst = f'{FOLDER_PATH}/files{car_index}'
        os.mkdir(dst)
        os.mkdir(dst + '/assets')

        dst = f'{FOLDER_PATH}/mobilefiles{car_index}'
        os.mkdir(dst)
        os.mkdir(dst + '/assets')
    except:
        pass
    for asset in assets:
        src = f'{FOLDER_PATH}/files/assets/{asset}'
        dst = f'{FOLDER_PATH}/files{car_index}/assets/{asset}'
        src_mobile = f'{FOLDER_PATH}/mobilefiles/assets/{asset}'
        dst_mobile = f'{FOLDER_PATH}/mobilefiles{car_index}/assets/{asset}'
        try:
            utils.copytree(src, dst)
            utils.copytree(src_mobile, dst_mobile)
        except Exception as e:
            print(e)


def copy_files():
    root_folder = 'public/' + utils.get_timestamp()
    os.makedirs(root_folder)
    dst_root = root_folder + "/car2/files/assets"
    os.makedirs(dst_root)

    for asset in assets:
        src = f"public/mine_ind/files/assets/{asset}"
        dst = f"{dst_root}/{asset}"
        if os.path.exists(src):
            utils.copytree(src, dst)
        print(asset, pc_obj['assets'][str(asset)]['name'])

# copy_files()



