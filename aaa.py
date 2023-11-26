from io import BytesIO

import os
from math import floor

from pagermaid.listener import listener
from pagermaid.enums import Message, Client
from pagermaid.utils import pip_install
from pagermaid.single_utils import safe_remove

pip_install("moviepy")
import moviepy.editor as mp

@listener(command="gtss",
          description="将你回复的视频转换为贴纸")
async def pic_to_sticker(bot: Client, message: Message):
    reply = message.reply_to_message
    photo = None
    if reply:
        photo = reply
    elif message:
        photo = message
    if not photo:
        return await message.edit("请回复一张gif")
    try:
        photopath = await bot.download_media(photo)
        message: Message = await message.edit("正在转换...\n███████70%")
        clip = mp.VideoFileClip(photopath)
        safe_remove(photopath)
        while not os.path.splitext(photopath)[-1] == '':
            photopath = os.path.splitext(photopath)[0]
        photopath += '.WEBM'
        clip.write_videofile(photopath)
        if reply:
            await reply.reply_sticker(photopath, quote=True)
        else:
            await message.reply_sticker(photopath, quote=True)
        safe_remove(photopath)
    except Exception as e:
        return await message.edit(f"转换失败：{e}")
    await message.safe_delete()
