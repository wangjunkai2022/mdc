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

conf = config.getInstance()

pikpak_go = PikPak(conf.pikpak_user(), conf.pikpak_pd())
# default fetch order list, from the beginning to the end
suffix_videos = conf.media_type().lower().split(",")
suffix_photo = conf.photo_type().lower().split(",")


def main(path):
    exclude = ["extrafanart"]
    for number in range(369, 500):  # 150+没整理
        exclude.append(f"max_folder_50G_{number}")
    # get_file_list(path, run_have_callback, exclude=exclude)
    # get_folds_video(path, find_av_notnfo_or_badimg, exclude=exclude)
    # get_folds_video(path, run_num2video_callback, exclude=exclude)
    # get_folds_video(path, change_video_and_only_cd1, exclude=exclude)
    get_folds_video(path, superfluous_file, exclude=exclude)


def superfluous_file(video_file):
    parent_dir = os.path.dirname(video_file)
    superfluous = []
    not_superfluous = []
    for path, _, files in os.walk(parent_dir):
        for file in files:
            if re.search(r"\(\d\).", file):
                superfluous.append(os.path.join(path, file))
            else:
                not_superfluous.append(os.path.join(path, file))

    if len(superfluous) > 0:
        path = parent_dir[parent_dir.find(conf.organize_pikpak_path()):]
        print(superfluous)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(pikpak_go.superfluous_file(path))
        loop.run_until_complete(future)


def change_video_and_only_cd1(video_file):
    parent_dir = os.path.dirname(video_file)
    videos = []
    nfos = []
    name_have_hack = False
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        suffix = os.path.splitext(temp_dir)[-1].lower()
        name = os.path.splitext(f)[0].lower()
        if suffix in suffix_videos:
            videos.append(temp_dir)
            if 'cd1' in name.lower():
                name_have_hack = True
        elif 'nfo' in suffix:
            nfos.append(temp_dir)

    if name_have_hack and len(videos) == 1:
        path = parent_dir[parent_dir.find(conf.organize_pikpak_path()):]
        print(f'整理文件{path}')
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(pikpak_go.change_1video_cd(path))
        loop.run_until_complete(future)
    if len(nfos) < 1:
        path = parent_dir[parent_dir.find(conf.organize_pikpak_path()):]
        print(f"没有nfo文件{path}")
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(pikpak_go.run_have_change(path))
        loop.run_until_complete(future)


def find_av_notnfo_or_badimg(video_file):
    parent_dir = os.path.dirname(video_file)
    imgs = []
    videos = []
    nfo_files = []
    # 是否操作
    dity = False

    print(f"当前扫描到的文件{parent_dir}")
    for root, base_name, files in os.walk(parent_dir):
        # print(root, base_name, file)
        for file in files:
            temp_dir = os.path.join(root, file)
            new_dir = os.path.join(root, file.lower())
            suffix = os.path.splitext(temp_dir)[-1].lower()
            if suffix in suffix_videos:
                if file.lower() != file:
                    os.rename(temp_dir, new_dir)
                videos.append(new_dir)
                pass
            elif suffix == ".nfo":
                if file.lower() != file:
                    os.rename(temp_dir, new_dir)
                nfo_files.append(new_dir)
            elif suffix in suffix_photo:
                imgs.append(temp_dir)

    if len(nfo_files) < 1:
        print(f"{parent_dir} nfo 文件有问题{nfo_files}")
        dity = True
    # elif len(nfo_files) > 1:

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
        nfo_files.sort(key=len)
        nfo_new_path = os.path.join(parent_dir, os.path.basename(parent_dir).lower() + ".nfo")
        nfo_old_path = os.path.join(parent_dir, nfo_files[0])
        if nfo_old_path.lower() != nfo_new_path.lower() and not os.path.exists(nfo_new_path):
            os.rename(nfo_old_path, nfo_new_path)
        num = os.path.basename(parent_dir).lower()
        for video in videos:
            if num in video.lower():
                pass
            else:
                print(f"{parent_dir}中 视频文件和文件夹不对 需要查看")
    if dity:
        # print(f'nfo 文件和视频文件不匹配——{parent_dir}')
        run_remdc_callback(parent_dir)


# def nfo_in_video(video_file):
def run_num2video_callback(video_file):
    parent_dir = os.path.dirname(video_file)
    videos = []
    name_have_hack = False
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        suffix = os.path.splitext(temp_dir)[-1].lower()
        name = os.path.splitext(f)[0].lower()
        if suffix in suffix_videos:
            videos.append(temp_dir)
            if 'hack' in name.lower():
                name_have_hack = True
            # video_file = temp_dir
            # path = parent_dir.replace("/Volumes/dav/色花堂无码无破解", "")
            # print(path)
            # loop = asyncio.get_event_loop()
            # future = asyncio.ensure_future(pikpak_go.run_have_change(path))
            # loop.run_until_complete(future)
            # return
    if len(videos) >= 1 and name_have_hack:
        # path = parent_dir.replace("/Volumes/dav/色花堂无码无破解", "")
        path = parent_dir[parent_dir.find(conf.organize_pikpak_path()):]
        print(path)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(pikpak_go.run_have_change(path))
        loop.run_until_complete(future)


# 文件夹中带有Have的字段则进入直接在pikpak的地方进行重新下载并删除原视频文件。
def run_have_callback(video_file):
    parent_dir = os.path.dirname(video_file)
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        suffix = os.path.splitext(temp_dir)[-1].lower()
        if suffix in suffix_videos and "Have" in temp_dir:
            # video_file = temp_dir
            # path = parent_dir.replace("/Volumes/dav/色花堂无码无破解", "")
            path = parent_dir[parent_dir.find(conf.organize_pikpak_path()):]
            print(path)
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(pikpak_go.run_have_change(path))
            loop.run_until_complete(future)
            return


def run_remdc_callback(parent_dir):
    # for root, path, file in os.walk(path):
    #     print(root, path, file)
    video_file = []
    for f in listdir(parent_dir):
        temp_dir = join(parent_dir, f)
        suffix = os.path.splitext(temp_dir)[-1].lower()
        if suffix in suffix_videos:
            video_file.append(temp_dir)
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
    select_video = ''
    num = os.path.basename(os.path.dirname(video_file[0]))
    # if re.search(r"n\d\d\d\d", num) and len(num) == 5:
    #     num = "TokyoHot-" + num
    if len(video_file) > 1:
        print(f"{parent_dir}视频文件不止一个")
        select_video = os.path.join(parent_dir, num + ".mp4")
    else:
        select_video = video_file[0]
    import Movie_Data_Capture
    # from number_parser import get_number
    # num = get_number(False, num)
    args = tuple([
        select_video,
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
    # main("/Volumes/dav/色花堂无码无破解/JAV_output")
    main(conf.organize_path())

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
