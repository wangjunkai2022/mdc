import os
import re
import subprocess
from pikpakapi import PikPakApi, DownloadStatus
import asyncio


class PikPak():
    client = None
    user = ""
    password = ""

    def __init__(self, user, password):
        self.user = user
        self.password = password

    async def content(self):
        self.client = PikPakApi(self.user, self.password)
        await self.client.login()

    async def change(self):
        if not self.client:
            await self.content()

    # 这里的path是pikpak中的路径 不是本地映射的路径
    async def run_have_change(self, path):
        await self.change()
        pikpak_paths = await self.client.path_to_id(path)
        pikpak_parent_path = pikpak_paths[len(pikpak_paths) - 2]
        pikpak_file_path = pikpak_paths[len(pikpak_paths) - 1]
        for pikpak_ in pikpak_paths[::-1]:
            if pikpak_ and pikpak_.get("file_type") == "folder":
                pikpak_parent_path = pikpak_
                break
            pass

        all_parent_files = await self.client.file_list(parent_id=pikpak_parent_path.get("id"))
        nfo_file = None
        old_videos = []
        for file in all_parent_files.get("files"):
            if "nfo" in file.get("name"):
                nfo_file = file
            elif "mp4" in file.get("name"):
                old_videos.append(file)
                if pikpak_file_path.get("file_type") == "folder":
                    pikpak_file_path = file
        if not nfo_file:
            # p = subprocess.Popen(cmd, shell=True,env=)
            # return_code = p.wait()
            import Movie_Data_Capture
            path_new = re.sub(r"_Have\d", "", path)
            num = pikpak_parent_path.get('name')
            args = tuple([
                f"/Volumes/dav/色花堂无码无破解{path_new}",
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
            await asyncio.sleep(10)
            await self.run_have_change(path)
            return
        nfo_name = nfo_file.get("name").replace(".nfo", "")
        # file_info = await self.client.file_rename(pikpak_file.get("id"), "__" + pikpak_file.get("name"))
        file_info = await self.client.get_download_url(pikpak_file_path.get("id"))
        magnet_url = file_info.get("params").get("url")
        offline_down = await self.client.offline_download(magnet_url, pikpak_parent_path.get("id"))
        task_id = offline_down.get("task").get('id')
        file_id = offline_down.get("task").get('file_id')
        # 等待离线下载完成。。。。。。
        count = 10
        while True:
            if file_id == "":
                await asyncio.sleep(10)
                temp_path = os.path.join(os.path.dirname(path), offline_down.get("task").get('name'), )
                file_paths = await self.client.path_to_id(temp_path)
                file_id = file_paths[len(file_paths) - 1].get("id")
                break
            result = await self.client.get_task_status(task_id, file_id)
            print(f"等待离线下载完成{result}")
            if DownloadStatus.done == result or DownloadStatus.not_found == result:
                break
            await asyncio.sleep(2)
            count -= 1
            if count < 0:
                # await self.run_have_change(path)
                # return
                print("下载太久 不知道有没有完成 这里打印一下")
                break
        new_down_file = await self.client.get_download_url(file_id)
        if "folder" in new_down_file.get("kind"):
            # 下载的是文件夹
            file_list = await self.client.file_list(parent_id=file_id)
            videos = []
            for file in file_list.get("files"):
                name = file.get("name")
                size = int(file.get("size"))
                if re.search(r"社(\s*)區(\s*)最(\s*)新(\s*)情(\s*)報(\s*)", name, re.I) or \
                        re.search(r'x(\s*)u(\s*)u(.*)c(\s*)o(\s*)m*', name, re.I) or \
                        re.search(r'u(\s*)u(.*)c(\s*)o(\s*)m*', name, re.I) or \
                        re.search(r'u(\s*)u(\s*)r*', name, re.I) or \
                        re.search(r"有(\s*)趣(\s*)的(\s*)臺(\s*)灣(\s*)妹(\s*)妹(\s*)直(\s*)播*", name, re.I):
                    print(f'这个文件不对 不加入{name}')
                elif "mp4" in name:
                    videos.append(file)
            videos.sort(key=lambda element: element['name'])
            if len(old_videos) == len(videos):
                count = 1
                for video in videos:
                    await self.client.file_rename(video.get("id"), f"{nfo_name}-cd{count}.mp4")
                    count += 1
                for video in old_videos:
                    if nfo_name in video.get("name"):
                        await self.client.delete_forever(ids=[video.get("id")])
                for video in videos:
                    await self.client.file_batch_move(ids=[video.get("id")], to_parent_id=pikpak_parent_path.get("id"))
            else:
                print(f"新下载的文件和以前的文件数量不一样{path}")
                raise EOFError()
            await self.client.delete_forever(ids=[file_id])

            # 删除下载的文件夹
            # delete = await self.client.delete_forever([
            #     file_id,
            # ])
            # print(delete)
