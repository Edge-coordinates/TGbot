import secrets

from os import sep

from pagermaid.listener import listener
from pagermaid.single_utils import Message, safe_remove
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'
}

img_apis = ["https://pic.re/images", "https://tuapi.eees.cc/api.php?category={dongman,fengjing}",
            "https://tuapi.eees.cc/api.php?category=fengjing", "https://tuapi.eees.cc/api.php?category=dongman&type=302",
            "https://api.mtyqx.cn/tapi/random.php", "https://img.paulzzh.tech/touhou/random"]


@listener(command="e1",
          description="获取二次元图+一言")
async def e1(message: Message):
    arguments = message.arguments.upper().strip().split()
    status = False
    hitokoto_json = (requests.get(
        "https://v1.hitokoto.cn/?charset=utf-8", headers=headers, timeout=10)).json()
    copy_right = "“种族不代表荣耀，我见过最高尚的兽人，也见过最卑劣的人类。”"
    if hitokoto_json['hitokoto']:
        copy_right = "“" + hitokoto_json['hitokoto'] + "”"
    await message.edit("一言装填完毕。")
    # 图片部分开始
    sub = 0
    if arguments[0]:
        sub = int(arguments[0])
    filename = f"data{sep}wallpaper.jpg"
    for _ in range(3):
        image_url = img_apis[sub]
        try:
            if image_url != " ":
                img = requests.get(image_url, headers=headers, timeout=10)
            else:
                continue
            if img.status_code == 200:
                await message.edit("已进入二次元 . . .")
                with open(filename, "wb") as f:
                    f.write(img.content)
                await message.reply_photo(
                    filename,
                    caption=("#每日の图\n"
                             f"{str(copy_right)}\n"
                             "@edge_wasteland"),
                    quote=False,
                    reply_to_message_id=message.reply_to_top_message_id,
                )
                status = True
                break  # 成功了就赶紧结束啦！
        except Exception:
            continue
    safe_remove(filename)
    if not status:
        return await message.edit("出错了呜呜呜 ~ 试了好多好多次都无法访问到服务器 。")
    await message.safe_delete()
