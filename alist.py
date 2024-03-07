import asyncio
import httpx
import json
import config

conf = config.getInstance()

user = conf.organize_alist_user()
password = conf.organize_alist_pd()
token = ''
proxy = None

domain = conf.organize_alist_domain()


async def update_all(path):
    global token
    if not token:
        # headers = {
        #     # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        #     'Content-Type': 'application/json'
        # }
        body = {
            "username": user,
            "password": password,
        }
        async with httpx.AsyncClient(proxies=proxy) as client:
            response = await client.post(domain + "/api/auth/login", json=body)
            re_json = json.loads(response.text)
            token = re_json["data"]["token"]

    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.post(domain + "/api/fs/list", headers={
            "Authorization": token,

        }, json={
            "path": path,
            "refresh": True,
        })
        re_json = json.loads(response.text)
        print("刷新alist的文件结果{}".format(re_json))
        return re_json["code"] == 200 and re_json["message"] == "success", re_json


if __name__ == '__main__':
    import re

    parent_path = "/data/videos/media/alist/PikPak2/整理/中文字幕无码破解/希島あいり/IPZ-299"
    # pikpakPath = parent_path.replace("/data/videos/media/alist/PikPak2/", "")
    alist_re = re.search(r"alist/", parent_path)
    alist_path = parent_path[alist_re.end():]
    print(alist_path)

    # path = "/PikPak2/整理/中文字幕无码破解/希島あいり/IPZ-299"
    loop = asyncio.get_event_loop()
    get_future = asyncio.ensure_future(update_all(alist_path))  # 相当于开启一个future
    loop.run_until_complete(get_future)  # 事件循环
    magnets = get_future.result()
    print(magnets)  # 获取结果
