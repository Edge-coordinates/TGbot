import secrets

from os import sep

from pagermaid.listener import listener
from pagermaid.single_utils import Message, safe_remove
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'
}

gushi_apis = ["https://v1.jinrishici.com/all", "https://tuapi.eees.cc/api.php?category={dongman,fengjing}",
            "https://tuapi.eees.cc/api.php?category=fengjing", "https://tuapi.eees.cc/api.php?category=dongman&type=302",
            "https://api.ixiaowai.cn/api/api.php","https://api.ixiaowai.cn/mcapi/mcapi.php", "https://api.ixiaowai.cn/gqapi/gqapi.php", 
            "https://api.mtyqx.cn/tapi/random.php", "https://img.paulzzh.tech/touhou/random"]


@listener(command="gs",
          description="获取随机古诗")
async def gs(message: Message):
    arguments = []
    status = False
    sub = 0
    #初始化完毕
    arguments = message.arguments.upper().strip().split()
    if arguments[0]:
        sub = int(arguments[0])
    for _ in range(3):
        gushi_url = gushi_apis[sub]
        try:
            if gushi_url != " ":
                gushi = requests.get(gushi_url, headers=headers, timeout=10)
            else:
                continue
            if gushi.status_code == 200:
                gjson = json.loads(gushi.text) 
                gorigin = gjson["origin"]
                gauthor = gjson["author"]
                gcontent = gjson["content"]
                gcategory = gjson["category"]
                await message.edit("#每日の诗\n"
                    f"{gorigin} by {gauthor}\n"
                    f"{gcontent}\n"
                    f"{gcategory}")
                status = True
                break  # 成功了就赶紧结束啦！
        except Exception:
            continue
    if not status:
        return await message.edit("出错了呜呜呜 ~ 试了好多好多次都无法访问到服务器 。")
