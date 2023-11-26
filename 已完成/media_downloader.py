import shutil
import os
from os import sep
from pagermaid.listener import listener
from pagermaid.enums import Client, Message
from pagermaid.single_utils import safe_remove
from pagermaid.utils import pip_install
from pagermaid.services import sqlite
import zipfile

zip_path = 'dmf_tmp.zip'
start_id = 0
end_id = 0
chat_id = 0

@listener(command="dmf",
          description="批量下载媒体文件 by 边缘坐标")
async def media_downloader(app: Client, message: Message):
    if not message.reply_to_message:
        await message.edit("请回复一条消息以使用")
        return
    # 参数预处理
    if message.arguments:
        arguments = message.arguments.lower().strip().split()
    else:
        arguments = ['d']
    # 预赋值
    global chat_id
    global start_id
    global end_id
    reply = message.reply_to_message
    reply_id = reply.id #int
    start_id = reply_id
    chat_id = message.chat.id
    flist = []
    # 进入命令选择
    if arguments[0] == 's':
        pass
        # if len(arguments) == 1:
        #     await message.edit(''.join(helptext))
        #     return
        # elif arguments[1] == 'list':
        #     api_lists = list(img_apis)
        #     await message.edit(api_lists)
        #     return
        # elif arguments[1] == 'help':
        #     await message.edit(''.join(helptext))
        #     return
    elif arguments[0] == 'r':
        sqlite["dmf_start_id"] = reply_id
    elif arguments[0] == 'd':
        start_id = sqlite.get("dmf_start_id", start_id)
        end_id = reply_id
        if end_id - start_id > 200:
            await message.edit("太多啦,请重置开始消息，命令：`,dmf r`")
            return
        flist = await ddownloader(start_id, end_id, app, message)
        # await message.edit(flist)
        if flist == 0 or len(flist) == 0:
            await message.edit("懒得写提示，自己看源码怎么用1")
            return
        status = await zipper(flist)
        if not status:
            await message.edit("懒得写提示，自己看源码怎么用2")
            return
        await message.reply_document(zip_path, caption = "打包媒体", quote=False)
    elif arguments[0].isnumeric():
        if int(arguments[0] > 200):
            await message.edit("太多了我会坏掉的")
            return
        start_id = reply_id
        end_id = start_id + int(arguments[0])
        flist = ddownloader(start_id, end_id, app, message)
        # await message.edit(flist)
        if flist == 0 or len(flist) == 0:
            await message.edit("懒得写提示，自己看源码怎么用3")
            return
        status = await zipper(flist)
        if not status:
            await message.edit("懒得写提示，自己看源码怎么用4")
            return
        await message.reply_document(zip_path, caption = "打包媒体", quote=False)

    safe_remove(zip_path)
    for filee in flist:
        safe_remove(filee)
    await message.safe_delete()

async def ddownloader(start_id, end_id, app, message):
    filst = []
    if start_id == 0 or end_id == 0:
        return 0
    meslist = list(range(start_id, end_id+1))
    await message.edit(meslist)
    messages = await app.get_messages(chat_id, meslist)
    for mes in messages:
        try:
            fpath = await app.download_media(mes)
            filst.append(fpath)
        except Exception as e:
            pass
    return filst

async def zipper(flist):
    zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    for filea in flist:
        filename = os.path.split(filea)[-1]
        zip_file.write(filea, filename)
    zip_file.close() 
    return 1