import os
from math import floor
import subprocess

from pagermaid.listener import listener
from pagermaid.enums import Message, Client
from pagermaid.utils import pip_install
from pagermaid.single_utils import safe_remove

pip_install("moviepy")
import moviepy.editor as mp

@listener(command="gtss",
          description="将你回复的视频转换为贴纸, 命令 gtss")
async def pic_to_sticker(bot: Client, message: Message):
    reply = message.reply_to_message
    photo = None
    if reply and reply.media.value:
        photo = reply
    elif message.media.value:
        photo = message
    if not photo:
        return await message.edit("请回复一张gif")
    try:
        photopath = await photo.download()
        message: Message = await message.edit("正在转换...\n███████70%")
        clip = mp.VideoFileClip(photopath)
        videosize = clip.size
        target_resolution = []
        if videosize[0] > videosize[1]:
            target_resolution = [None ,512]
        else:
            target_resolution = [512, None]
        ends = min(clip.duration, 3.0)
        clip = mp.VideoFileClip(photopath, target_resolution=target_resolution).subclip(0,ends)
        first_file_path = photopath
        old_path = photopath + os.path.splitext(photopath)[-1]
        clip.write_videofile(old_path, fps=30, audio = False)
        while not os.path.splitext(photopath)[-1] == '':
            photopath = os.path.splitext(photopath)[0]
        photopath += '.webm'
        status_code, log = subprocess.getstatusoutput(
            f"ffmpeg -i '{old_path}' -vcodec libvpx-vp9 -pix_fmt yuva420p '{photopath}'"
        )
        # await message.edit(log)
        if reply:
            await reply.reply_video(photopath, quote=True)
        else:
            await message.reply_video(photopath, quote=True)
        safe_remove(photopath)
        safe_remove(old_path)
        safe_remove(first_file_path)
    except Exception as e:
        return await message.edit(f"转换失败：{e}")
    await message.safe_delete()
