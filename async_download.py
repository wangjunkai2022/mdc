import os

import aiohttp
import asyncio
from aiohttp import FormData
import config

headers = {"User-Agent": ua or G_USER_AGENT}  # noqa


async def sync_download(url, filename, path, filepath, json_headers=None, cookies=None):
    file_save_path = os.path.join(path, filename)
    print(f"资源异步下载部分\turl:{url}\nname:{filename} \npath:{path} \nfilepath:{filepath}")

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print(f"异步创建文件错误\n'{path}'")
            return
    if json_headers is not None:
        headers.update(json_headers)
    verify = config.getInstance().cacert_file()
    config_proxy = config.getInstance().proxy()
    if config_proxy.enable:
        proxies = config_proxy.proxies()
    else:
        proxies = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=config_proxy.timeout, proxies=proxies,
                               verify=verify,
                               cookies=cookies, stream=True) as resp:
            with open(file_save_path, 'wb') as fd:
                async for chunk in resp.content.iter_chunked(1024):
                    fd.write(chunk)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sync_download())
