import wget
import speedtest

from PIL import Image
from config import BOT_USERNAME as bname

from driver.filters import command
from driver.decorators import sudo_users_only
from driver.core import bot as app
from driver.utils import remove_if_exists

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(command(["speedtest", f"speedtest@{bname}"]) & ~filters.edited)
@sudo_users_only
async def run_speedtest(_, message: Message):
    m = await message.reply_text("🥴 sᴛᴀʀᴛɪɴɢ sᴩᴇᴇᴅᴛᴇsᴛ...")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("🥴 ᴛᴇsᴛɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ sᴩᴇᴇᴅᴛᴇsᴛ...")
        test.download()
        m = await m.edit("🥴 ᴛᴇsᴛɪɴɢ ᴜᴩʟᴏᴀᴅ sᴩᴇᴇᴅᴛᴇsᴛ...")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await m.edit(e)
        return
    m = await m.edit("🥱 ᴡᴀɪᴛ ғᴏʀ ᴀ sᴇᴄ ʟᴇᴛ ᴍᴇ ᴇᴅɪᴛ ᴀɴᴅ ɪɴᴄʀᴇᴀsᴇ ᴛʜᴇ sᴩᴇᴇᴅ ɪɴ ᴛʜᴀᴛ ᴩɪᴄ 😜")
    path = wget.download(result["share"])
    try:
        img = Image.open(path)
        c = img.crop((17, 11, 727, 389))
        c.save(path)
    except BaseException:
        pass

    output = f"""😴 **ғᴀᴋᴇ sᴩᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs**
    
<u>**ᴄʟɪᴇɴᴛ:**</u>
**ɪsᴩ:** {result['client']['isp']}
**ᴄᴏᴜɴᴛʀʏ:** {result['client']['country']}
  
<u>**sᴇʀᴠᴇʀ:**</u>
**ɴᴀᴍᴇ:** {result['server']['name']}
**ᴄᴏᴜɴᴛʀʏ:** {result['server']['country']}, {result['server']['cc']}
**sᴩᴏɴsᴏʀ:** {result['server']['sponsor']}
**ʟᴀᴛᴇɴᴄʏ:** {result['server']['latency']}

😲 **ᴩɪɴɢ:** {result['ping']}

**ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ ʙᴀʙʏ ɪ sᴇɴᴅ ᴛʜᴇ ᴇᴅɪᴛᴇᴅ ᴩɪᴄ ʜᴇʀᴇ, ᴄʜᴇᴄᴋ ʏᴏᴜ ᴅᴍ ɪ sᴇɴᴛ ʏᴏᴜ ᴛʜᴇ ʀᴇᴀʟ ᴩɪᴄ ᴛʜᴇʀᴇ,🥵 ɪ ᴀᴍ ғᴀsᴛ ᴀғ 🥵"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    remove_if_exists(path)
    await m.delete()
