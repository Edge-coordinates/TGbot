import os
import time
from pagermaid.listener import listener
from pagermaid.enums import Client, Message
from pagermaid.single_utils import safe_remove
from pagermaid.services import bot, sqlite

zip_path = 'dmf_tmp.zip'
start_id = 0
end_id = 0
chat_id = 0
MAX_BOK = 10005
Bot_ID = 2142201306

@listener(command="fft",
          description="批量转发文件 by 边缘坐标")
async def media_downloader(app: Client, message: Message):
    # if not message.reply_to_message:
    #     await message.edit("请回复一条消息以使用")
    #     return
    # 参数预处理
    if message.arguments:
        arguments = message.arguments.lower().strip().split()
    else:
        arguments = ['0']
    # 预赋值
    global chat_id
    global start_id
    global end_id
    reply = message.reply_to_message
    if reply:
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
        sqlite["fft_start_id"] = reply_id
    elif arguments[0] == 'd':
        start_id = sqlite.get("fft_start_id", start_id)
        end_id = reply_id
        if end_id - start_id > MAX_BOK:
            await message.edit("太多啦,请重置开始消息，命令：`,fft r`")
            return
        await do(start_id, end_id, app, message)
    elif arguments[0] == 'da' and len(arguments) == 3 and arguments[1].isdigit() and arguments[2].isdigit():
        start_id = int(arguments[1])
        end_id = int(arguments[2])
        if end_id - start_id > MAX_BOK:
            await message.edit("太多了我会坏掉的")
            return
        await do(start_id, end_id, app, message)
    elif arguments[0] == 'ca' and len(arguments) == 4 and arguments[2].isdigit() and arguments[3].isdigit():
        chat_id = int(arguments[1])
        start_id = int(arguments[2])
        end_id = int(arguments[3])
        if end_id - start_id > MAX_BOK:
            await message.edit("太多了我会坏掉的")
            return
        await do(start_id, end_id, app, message)
    elif arguments[0].isdigit():
        if int(arguments[0]) > MAX_BOK:
            await message.edit("太多了我会坏掉的")
            return
        start_id = reply_id
        end_id = start_id + int(arguments[0])
        await do(start_id, end_id, app, message)
    else:
        await message.reply("参数错误", quote=False)
    await message.safe_delete()



async def do(start_id, end_id, app, message):
    # 通过给定的参数转发文件
    filst = []
    if start_id == 0 or end_id == 0:
        return 0
    meslist = list(range(start_id, end_id+1))
    await message.edit(f"`{chat_id}`")
    a_meslist = arr_size(meslist, 200)
    for mlist in a_meslist:
        # await message.edit(mlist)
        messages = await app.get_messages(chat_id, mlist)
        meslist = []
        for mes in messages:
            try:
                filename = mes.document.file_name
                if is_file_ok(filename):
                    meslist.append(mes.id)
            except Exception as e:
                pass
                # await message.reply(str(e))
        if len(meslist) == 0:
            return            
        await bot.forward_messages(Bot_ID, chat_id, meslist)
        time.sleep(10)

def is_file_ok(filename):
    ok_filend = ['.TXT', '.EPUB', '.PDF', '.MOBI', '.AZW3', '.ZIP']
    filend = os.path.splitext(filename)[-1].upper()
    for i in ok_filend:
        if i == filend:
            return 1
    return 0
    
def arr_size(arr,size):
    s=[]
    for i in range(0,int(len(arr))+1,size):
        c=arr[i:i+size]
        s.append(c)
    newlist = [x for x in s if x]
    return newlist