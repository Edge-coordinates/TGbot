'''
食用帮助
Json API 这么定义
'list_path':[] ,定义为一个数组，数组中每个元素为json中图片列表的路径
'''
import secrets

from os import sep
import os

from pagermaid.listener import listener
from pagermaid.single_utils import Message, safe_remove
from pagermaid.utils import pip_install
pip_install("requests")
pip_install("ddict")

from ddict import DotAccessDict
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'
}

img_apis = {
    "0": {'url': "https://pic.re/images",
          "des": "A free public Anime picture provider api."},
    "1": {"url": "https://tuapi.eees.cc/api.php",
          "parameter": ["category={dongman,fengjing}&type=302", "category=fengjing&type=302", "category=dongman&type=302", "category=dongman&px=m&type=302"],
          "des": "动漫，风景混合API,参数有三种，分别是动漫风景混合，纯风景，纯动漫"},
    "2": {'url':'https://px2.rainchan.win/random', 'des':'随机Pixiv图片'},
    "4": {"url": "https://img.paulzzh.tech/touhou/random",
          "des": "东方图片API"},
    "5": {"des": "文档地址：https://www.eee.dog/tech/rand-pic-api.html"},
    "r0": {'url': 'https://anime-api.hisoka17.repl.co/img/nsfw/hentai', 'des': "hentaiNSFWAPI,可能返回图片或GIF", 'isjson': 1,
           'item_path':['url']},
    "r1": {'url': 'https://anime-api.hisoka17.repl.co/img/nsfw/lesbian', 'des': "lesbianNSFWAPI,可能返回图片或GIF", 'isjson': 1,
           'item_path':['url']},
    "r2": {'url': 'https://anime-api.hisoka17.repl.co/img/nsfw/boobs', 'des': "boobsNSFWAPI,可能返回图片或GIF", 'isjson': 1,
           'item_path':['url']},
}

helptext = ("Random Image Plugin V0.2 by Edge-coordinates\n"
            "命令帮助\n"
            "本插件命令为`,rp`有如下模式\n"
            "普通模式：默认模式就是普通模式，将会根据用户的输入参数返回随机图片\n"
            "图床API分为普通API和JsonAPI,对于普通API，有的图床提供了选择参数，您在输入命令时候将可以输入两个参数用来配置图床的选择参数，这是一个例子`,rp abc 1`，其中，**abc**代表图床的名称，**1**代表你选择的参数。参数的选择是数组，从0开始，如果你输入的数字不合法，将使用0作为代替\n",
            "对于JsonAPI，目前不提供任何配置。"
            "命令模式：通过第一个参数是否为s鉴别，命令列表如下：\n"
            "`,ri s list`该命令将会输出所有的随机图床信息")


@ listener(command="ri",
           description=''.join(helptext),
           usage=helptext)
async def Random_Image(message: Message):
    # 参数预处理
    if message.arguments:
        arguments = message.arguments.lower().strip().split()
    else:
        for key in img_apis:
            arguments = [key]
            break
    # 预赋值
    imgurl = 0
    a_word = A_word()
    # 进入命令选择
    if arguments[0] == 's':
        if len(arguments) == 1:
            await message.edit(''.join(helptext))
            return
        elif arguments[1] == 'list':
            api_lists = list(img_apis)
            await message.edit(api_lists)
            return
        elif arguments[1] == 'help':
            await message.edit(''.join(helptext))
            return
    if arguments[0] == 'c':
        if len(arguments) == 1:
            await message.edit(''.join(helptext))
            return
        else:
            imgurl = arguments[1]
            # 自定义爬取，想想咋写》

    
    # await message.edit(imgurl)
    # 图片部分开始
    if imgurl == 0:
        imgurl = await img_url_geter(message, arguments)
    if imgurl == 0:
        return
    filenamelist = await img_downloader(message, arguments, imgurl)
    if filenamelist == 0:
        return await message.edit("出错了呜呜呜 ~ 试了好多好多次都无法访问到服务器 。")
    if not await message_sender(message, filenamelist, a_word):
        message.edit("出错了，可能群组不让发布媒体。")
    await file_cleaner(message, filenamelist)

    await message.safe_delete()


async def img_url_geter(message, arguments):
    api_item = img_apis.get(arguments[0], 0)
    if api_item == 0:
        await message.edit("出错了呜呜呜 ~ 请使用`,ri s list`来检查可用的API")
        return 0
    img_url = api_item.get('url', False)
    if not img_url:
        await message.edit("出错了呜呜呜 ~ 该API未启用")
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
    if api_item.get('isjson', 0):
        jsonc = requests.get(img_url, headers=headers, timeout=10).json()
        jsonc = DotAccessDict(jsonc)
        img_url = []
        if api_item.get('item_path', 0):
            for i in api_item.get('item_path'):
                tmp = jsonc.get(i, 0)
                if tmp == 0:
                    return 0
                if isinstance(tmp, str):
                    img_url.append(tmp)
        if api_item.get('list_path', 0):
            for i in api_item.get('list_path'):
                tmp = jsonc.get(i, 0)
                if tmp == 0:
                    return 0
                if type(tmp) == type([]):
                    img_url = img_url + tmp
    return img_url


async def img_downloader(message, arguments, imgurl):
    status = 0
    if type(imgurl) == type([]) and len(imgurl) == 1:
        imgurl = imgurl[0]
    if isinstance(imgurl, str):
        for _ in range(3):
            try:
                img = requests.get(imgurl, headers=headers, timeout=10)
                if img.status_code == 200:
                    filename = f"data{sep}{img.url.split('/')[-1]}"
                    # await message.edit(imgurl)
                    await message.edit("图片Get！")
                    with open(filename, "wb") as f:
                        f.write(img.content)
                        return filename
            except Exception:
                return 0
        return 0
    elif type(imgurl) == type([]):
        await message.edit('???')
        pass


async def message_sender(message, filenamelist, a_word):
    if isinstance(filenamelist, str):
        try:
            fileend = os.path.splitext(filenamelist)[-1].lower()
            if fileend == '.mp4' or fileend == '.gif':
                await message.reply_video(
                    filenamelist,
                    caption=("#每日の视频\n"
                            f"{str(a_word)}\n"
                            "@edge_wasteland"),
                    quote=False,
                    reply_to_message_id=message.reply_to_top_message_id,
                )
                return 1
            else:
                await message.reply_photo(
                    filenamelist,
                    caption=("#每日の图\n"
                            f"{str(a_word)}\n"
                            "@edge_wasteland"),
                    quote=False,
                    reply_to_message_id=message.reply_to_top_message_id,
                )
                return 1
        except Exception:
            return 0
    else:
        # 处理返回图片列表的情况
        pass


async def file_cleaner(message, filenamelist):
    if isinstance(filenamelist, str):
        safe_remove(filenamelist)
    pass


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
