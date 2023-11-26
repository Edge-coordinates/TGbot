import secrets

from os import sep

from pagermaid.listener import listener
from pagermaid.single_utils import Message, safe_remove
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'
}

img_apis = {
    "0": {'url': "https://pic.re/images",
          "des": "A free public Anime picture provider api."},
    "1": {"url": "https://tuapi.eees.cc/api.php",
          "parameter": ["category={dongman,fengjing}&type=302", "category=fengjing&type=302", "category=dongman&type=302"],
          "des": "动漫，风景混合API,参数有三种，分别是动漫风景混合，纯风景，纯动漫"},
    "4": {"url": "https://img.paulzzh.tech/touhou/random",
          "des": "东方图片API"},
    "5": {"des": "文档地址：https://www.eee.dog/tech/rand-pic-api.html"}
}

helptext = ("Random Image Plugin V0.1 by Edge-coordinates\n"
            "命令帮助\n"
            "本插件命令为`,rp`有如下模式\n"
            "普通模式：默认模式就是普通模式，将会根据用户的输入参数返回随机图片\n"
            "图床API分为普通API和JsonAPI,对于普通API，有的图床提供了选择参数，您在输入命令时候将可以输入两个参数用来配置图床的选择参数，这是一个例子`,rp abc 1`，其中，**abc**代表图床的名称，**1**代表你选择的参数。参数的选择是数组，从0开始，如果你输入的数字不合法，将使用0作为代替\n",
            "对于JsonAPI，目前不提供任何配置。"
            "命令模式：通过第一个参数是否为s鉴别，命令列表如下：\n"
            "`,ri s list`该命令将会输出所有的随机图床信息")


@ listener(command="ri",
           description="获取二次元图+一言",
           usage=helptext)
async def Random_Image(message: Message):
    # 参数预处理
    if message.arguments:
        arguments = message.arguments.lower().strip().split()
    else:
        for key in img_apis:
            arguments = [key]
            break
    # 预赋值完毕
    status = False

    # 进入命令选择
    if arguments[0] == 's':
        if len(arguments) == 1:
            await message.edit(helptext)
            return
        elif arguments[1] == 'list':
            api_lists = list(img_apis)
            await message.edit(api_lists)
            return
    else:
        a_word = A_word()
        # await message.edit("一言装填完毕。")
        # 图片部分开始
        for _ in range(3):
            file = await image_grabber(arguments, message)
            if file == 0:
                break
            if isinstance(file, str):
                try:
                    await message.reply_photo(
                        file,
                        caption=("#每日の图\n"
                                    f"{str(a_word)}\n"
                                    "@edge_wasteland"),
                        quote=False,
                        reply_to_message_id=message.reply_to_top_message_id,
                    )
                    status = True
                    safe_remove(file)
                    break  # 成功了就赶紧结束啦！
                except Exception:
                    pass
            else:
                #处理返回图片列表的情况
                pass
        
        if not status:
            return await message.edit("出错了呜呜呜 ~ 试了好多好多次都无法访问到服务器 。")
        await message.safe_delete()


async def image_grabber(arguments, message):
    api_item = img_apis.get(arguments[0], 0)
    if api_item == 0:
        return await message.edit("出错了呜呜呜 ~ arguments初始化错误")
    if api_item != 0:
        img_url = api_item.get('url', False)
        if not img_url:
            return 0
        parameter = api_item.get('parameter', 0)
        if len(arguments) > 1:
            if parameter == 0:
                parameter = arguments[1]
            else:
                if arguments[1].isdigit():
                    parindex = int(arguments[1])
                    if parindex >= len(parameter):
                        parindex = len(parameter) - 1
                    parameter = parameter[parindex]
                else:
                    parameter = arguments[1]
            img_url = str(img_url + "?" + parameter)
        elif not parameter == 0:
            parameter = parameter[0]
            img_url = str(img_url + "?" + parameter)
        await message.edit(img_url)
        img = requests.get(img_url, headers=headers, timeout=10)
    else:
        pass
    try:
        filename = f"data{sep}wallpaper.jpg"
        if img.status_code == 200:
            await message.edit("图片Get！")
            with open(filename, "wb") as f:
                f.write(img.content)
                return filename
                # 成功就结束啦
    except Exception:
        return 0



def A_word():
    hitokoto_json = (requests.get(
        "https://v1.hitokoto.cn/?charset=utf-8", headers=headers, timeout=10)).json()
    a_word = hitokoto_json.get('hitokoto', "“种族不代表荣耀，我见过最高尚的兽人，也见过最卑劣的人类。”")
    return a_word


def list(dict):
    hlist = ""
    for key in dict:
        zdict = dict.get(key)
        hlist += f'''**Key：{key}**\n介绍：{zdict.get('des', "没有介绍")}\nURL：{zdict.get('url','这个API未启用')}\n参数值：{zdict.get('parameter','该API没有参数')}\n\n'''
    return hlist
