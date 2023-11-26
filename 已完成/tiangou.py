import secrets

from os import sep

from pagermaid.listener import listener
from pagermaid.single_utils import Message, safe_remove
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'
}

tg_api = "http://fuyhi.top/api/tgrj/api.php"


@listener(command="tiangou",
          description="随机舔狗日记 by Edgecoordinates")
async def gs(message: Message):
    # arguments = []
    status = False
    sub = 0
    #初始化完毕
    # arguments = message.arguments.upper().strip().split()
    # if arguments[0]:
        # sub = int(arguments[0])
    for _ in range(3):
        gushi_url = tg_api
        try:
            if gushi_url != " ":
                gushi = requests.get(gushi_url, headers=headers, timeout=10)
            else:
                continue
            if gushi.status_code == 200:
                gjson = json.loads(gushi.text) 
                await message.edit("#舔狗日记\n"
                    f"{gjson.get('text')}")
                status = True
                break  # 成功了就赶紧结束啦！
        except Exception:
            continue
    if not status:
        return await message.edit("出错了呜呜呜 ~ 试了好多好多次都无法访问到服务器 。")
