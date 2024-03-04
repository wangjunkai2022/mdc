import os
import shutil
from os import listdir
from os.path import join, isfile, isdir
import asyncio

import re

import time
from PIL import Image

import config
from pikpak import PikPak

pikpak_go = PikPak("lopipi9801@giratex.com", "098poi")
conf = config.getInstance()
# default fetch order list, from the beginning to the end
suffix_videos = conf.media_type().lower().split(",")
suffix_phone = conf.phone_type().lower().split(",")


def main(path):
    exclude = ["extrafanart"]
    # for number in range(400, 500):
    #     exclude.append(f"max_folder_50G_{number}")
    # get_file_list(path, run_have_callback, exclude=exclude)
    get_folds_video(path, find_av_notnfo_or_badimg, exclude=exclude)


def find_av_notnfo_or_badimg(video_file):
    parent_dir = os.path.dirname(video_file)
    imgs = []
    video = []
    nfo_file = None
    # 是否操作
    dity = False

    print(f"当前扫描到的文件{parent_dir}")
    for root, base_name, files in os.walk(parent_dir):
        # print(root, base_name, file)
        for file in files:
            temp_dir = os.path.join(root, file)
            suffix = os.path.splitext(temp_dir)[-1].lower()
            if suffix in suffix_videos:
                video.append(temp_dir)
                pass
            elif suffix == ".nfo":
                if nfo_file:
                    dity = True
                else:
                    nfo_file = file
            elif suffix in suffix_phone:
                imgs.append(temp_dir)

    if not nfo_file:
        print(f"{parent_dir} 没有 nfo 文件")
        dity = True

    count = 0
    for img in imgs:
        try:
            img = Image.open(img)
        except Exception as e:
            print(f"{img} 图片有问题")
            print(e)
            count += 1
            os.remove(img)

    if count >= len(imgs) or len(imgs) == 0:
        dity = True

    if not dity:
        nfo_name = os.path.splitext(nfo_file)[0]
        for file in video:
            if nfo_name in file:
                pass
            else:
                dity = True

    if video_file and dity:
        run_remdc_callback(parent_dir)


# def nfo_in_video(video_file):


# 文件夹中带有Have的字段则进入直接在pikpak的地方进行重新下载并删除原视频文件。
def run_have_callback(video_file):
    parent_dir = os.path.dirname(video_file)
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        suffix = os.path.splitext(temp_dir)[-1].lower()
        if suffix in suffix_videos and "Have" in temp_dir:
            # video_file = temp_dir
            path = parent_dir.replace("/Volumes/dav/色花堂无码无破解", "")
            print(path)
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(pikpak_go.run_have_change(path))
            loop.run_until_complete(future)
            return


def run_remdc_callback(parent_dir):
    # for root, path, file in os.walk(path):
    #     print(root, path, file)
    video_file = None
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        suffix = os.path.splitext(temp_dir)[-1].lower()
        if suffix in suffix_videos:
            video_file = temp_dir
        elif suffix == ".bif":
            pass
        else:
            if os.path.exists(temp_dir):
                if isdir(temp_dir):
                    shutil.rmtree(temp_dir)
                else:
                    os.remove(temp_dir)
            pass
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


# 循环遍历视频文件
def get_folds_video(parent_dir, callback=print, exclude=[]):
    """
    :param parent_dir: 想要获取文件列表的一级目录
    :param callback: 获取到视频文件回调
    :param exclude:排除的文件
    """

    # 列举出当前文件路径下的所有文件名，也可能是文件夹名
    for exc in exclude:
        if exc in parent_dir:
            return

    video_file = None
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        if isfile(temp_dir):
            suffix = os.path.splitext(temp_dir)[-1].lower()
            if suffix in suffix_videos:
                video_file = temp_dir
                break
        # elif "extrafanart" in temp_dir:
        #     pass
        else:
            get_folds_video(temp_dir, callback, exclude)

    if video_file:
        callback(video_file)


if __name__ == "__main__":
    print("main")
    # main("/Volumes/dav/色花堂无码无破解/JAV_output/max_folder_50G_298")
    main("/Volumes/dav/色花堂无码无破解/JAV_output")

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
