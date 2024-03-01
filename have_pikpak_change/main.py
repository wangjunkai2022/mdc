import os
import shutil
from os import listdir
from os.path import join, isfile, isdir
import asyncio

import re

import time
from PIL import Image

from pikpak import PikPak

pikpak_go = PikPak("lopipi9801@giratex.com", "098poi")


def main(path):
    exclude = []
    # for number in range(86, 440):
    #     exclude.append(f"max_folder_50G_{number}")
    # get_file_list(path, run_have_callback, exclude=exclude)
    get_file_list(path, run_remdc_callback, exclude=exclude)


def run_have_callback(path):
    path = path.replace("/Volumes/dav/色花堂无码无破解", "")
    print(path)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(pikpak_go.run_have_change(path))
    loop.run_until_complete(future)


def run_remdc_callback(parent_dir):
    # for root, path, file in os.walk(path):
    #     print(root, path, file)
    video_file = None
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        if not temp_dir.endswith(".mp4"):
            # if os.path.exists(temp_dir):
            #     if isdir(temp_dir):
            #         shutil.rmtree(temp_dir)
            #     else:
            #         os.remove(temp_dir)
            pass
        else:
            video_file = temp_dir
    time.sleep(5)
    import Movie_Data_Capture
    num = os.path.basename(os.path.dirname(video_file))
    if re.search(r"n\d\d\d\d", num) and len(num) == 5:
        num = "TokyoHot-" + num
    # from number_parser import get_number
    # num = get_number(False, num)
    args = tuple([
        video_file,
        f"{num}",
        'log',
        '',
        False,
        False,
        "",
        "",
        "",
    ])
    Movie_Data_Capture.main(args)
    time.sleep(10)
    return


def get_file_list(parent_dir, callback=print, exclude=[]):
    """
    :param parent_dir: 想要获取文件列表的一级目录
    :param file_list: 将获取到的文件列表存储到该列表中
    :return: 返回获取到的文件列表
    """
    # 列举出当前文件路径下的所有文件名，也可能是文件夹名
    for exc in exclude:
        if exc in parent_dir:
            return

    nfo_file = None
    video_file = None
    imgs = []
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        if isfile(temp_dir):
            if temp_dir.endswith(".mp4"):
                video_file = temp_dir
                break
        elif "extrafanart" in temp_dir:
            pass
        else:
            get_file_list(temp_dir, callback, exclude)
    if video_file:
        for root, base_name, files in os.walk(parent_dir):
            # print(root, base_name, file)
            for file in files:
                path_all = os.path.join(root, file)
                if path_all.endswith(".nfo"):
                    nfo_file = file
                elif path_all.endswith(".mp4"):
                    pass
                else:
                    imgs.append(path_all)
        是否整理 = False

        if not nfo_file:
            print(f"{parent_dir} 没有 nfo 文件")
            是否整理 = True

        for img in imgs:
            try:
                img = Image.open(img)
            except Exception as e:
                print(f"{img} 图片有问题")
                print(e)
                是否整理 = True
                break

        if video_file and 是否整理:
            callback(parent_dir)


if __name__ == "__main__":
    print("main")
    # main("/Volumes/dav/色花堂无码无破解/JAV_output/max_folder_50G_298")
    main("/Volumes/dav/色花堂无码无破解/JAV_output/")

    # name = "x u u 9 2 .c o m.mp4"
    # name = 'u u r 9 3.c om'
    # name = 'uur76.mp4'
    # name = '有 趣 的 臺 灣 妹 妹 直 播 .mp4'
    # if re.search(r"社(\s*)區(\s*)最(\s*)新(\s*)情(\s*)報(\s*)", name, re.I) or \
    #         re.search(r'x(\s*)u(\s*)u(.*)c(\s*)o(\s*)m*', name, re.I) or \
    #         re.search(r'u(\s*)u(.*)c(\s*)o(\s*)m*', name, re.I) or \
    #         re.search(r'u(\s*)u(\s*)r*', name, re.I) or \
    #         re.search(r"有(\s*)趣(\s*)的(\s*)臺(\s*)灣(\s*)妹(\s*)妹(\s*)直(\s*)播*", name, re.I):
    #     print(f'这个文件不对 不加入{name}')
