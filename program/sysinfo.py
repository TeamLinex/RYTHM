import os
import re
import uuid
import socket
import psutil
import platform

from config import BOT_USERNAME

from program import LOGS
from driver.core import me_bot
from driver.filters import command
from driver.utils import remove_if_exists
from driver.decorators import sudo_users_only, humanbytes

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(command(["sysinfo", "sysstats", f"sysinfo@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def fetch_system_information(client, message):
    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    ram = humanbytes(round(psutil.virtual_memory().total))
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    du = psutil.disk_usage(client.workdir)
    psutil.disk_io_counters()
    disk = f"{humanbytes(du.used)} / {humanbytes(du.total)} " f"({du.percent}%)"
    cpu_len = len(psutil.Process().cpu_affinity())
    somsg = f"""🖥 **sʏsᴛᴇᴍ ɪɴғᴏʀᴍᴀᴛɪᴏɴ**
    
**ᴩʟᴀᴛғᴏʀᴍ :** `{splatform}`
**ʀᴇʟᴇᴀsᴇ :** `{platform_release}`
**ᴠᴇʀsɪᴏɴ :** `{platform_version}`
**ᴀʀᴄʜɪᴛᴇᴄᴛᴜʀᴇ :** `{architecture}`
**ʜᴏsᴛɴᴀᴍᴇ :** `{hostname}`
**ɪᴩ :** `{ip_address}`
**ᴍᴀᴄ :** `{mac_address}`
**ᴩʀᴏᴄᴇssᴏʀ :** `{processor}`
**ʀᴀᴍ : ** `{ram}`
**ᴄᴩᴜ :** `{cpu_len}`
**ғʀǫᴜᴇɴᴄʏ :** `{cpu_freq}`
**ᴅɪsᴋ :** `{disk}`

ʏᴏᴜ ᴀʀᴇ ᴛʜɪɴᴋɪɴɢ ʜᴏᴡ ᴛʜᴇ ᴄᴩᴜ ᴜsᴀɢᴇ ɪs sᴏ ʜɪɢʜ ɴᴀ 😂, ɪ ᴀᴍ ᴡᴀᴛᴄʜɪɴɢ 4ᴋ ᴩᴏ*ɴ ᴀɴᴅ ʏᴏᴜ ᴀʀᴇ ᴛᴇɴsᴇᴅ.😂
    """
    
    await message.reply(somsg)


@Client.on_message(command(["logs", "log", f"logs@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_bot_logs(c: Client, m: Message):
    bot_log_path = f'streambot-logs-{me_bot.id}.txt'
    if os.path.exists(bot_log_path):
        try:
            await m.reply_document(
                bot_log_path,
                quote=True,
                caption='» ʟᴏɢs ᴏғ ʏᴏᴜʀ ʙᴏᴛ',
            )
        except Exception as e:
            remove_if_exists(bot_log_path)
            print(f'[ERROR]: {e}')
    else:
        if not os.path.exists(bot_log_path):
            await m.reply_text('» ʟᴏɢs ɴᴏᴛ ғᴏᴜɴᴅ !')
