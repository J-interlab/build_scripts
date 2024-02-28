import cv2
import os
def resize_and_copy(path):
    if not path.startswith("public\\mine_ind\\files"):
        return 0
    new_path = "public\\mine_ind\\mobilefiles" + path[21:]
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    w = img.shape[1] // 2
    h = img.shape[0] // 2
    resized = cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA)
    dir_name = os.path.dirname(new_path)
    try:
        os.makedirs(dir_name)
        cv2.imwrite(new_path, resized)
    except:
        pass
    return os.stat(new_path).st_size

path = "public\\mine_ind\\files\\assets\\45032131\\1\\AO.jpg"