from pagermaid.listener import listener
from pagermaid.single_utils import Message

@listener(command="lss",
          description="列出所有可用的贴纸包")
async def ta(message: Message):
    tlist = ("边缘坐标：`Edgesticker01`、`edge_dynamic_01`、`EDGE000`"
        )
    await message.edit(''.join(tlist))
    # arguments = []
    # try:
        # arguments = message.arguments.upper().strip().split()
    #     await message.edit(arguments)    
    # except Exception:
    #     arguments = []
    #     await message.edit(arguments)
    
    # await message.edit(arguments)
    # await message.edit("**aa**")
    