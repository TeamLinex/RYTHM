import asyncio
import traceback

from pyrogram.types import Message
from pyrogram import Client, filters, __version__ as pyrover
from pytgcalls import (__version__ as pytgver)

from program import __version__ as ver
from program.start import __python_version__ as pyver

from driver.core import me_bot
from driver.filters import command
from driver.decorators import bot_creator, sudo_users_only
from driver.database.dbchat import get_served_chats
from driver.database.dbusers import get_served_users
from driver.database.dbpunish import get_gbans_count
from driver.database.dbqueue import get_active_chats

from config import BOT_USERNAME as uname


@Client.on_message(command(["broadcast", f"broadcast@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_nopin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.1)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"» ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ɪɴ {sent} ɢʀᴏᴜᴩ...")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**ᴜsᴀɢᴇ**:\n\n/broadcast (`message`) ᴏʀ (`reply to message`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.1)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"» sᴜᴄᴄᴇssғᴜʟʟʏ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ɪɴ {sent} ɢʀᴏᴜᴩs.")


@Client.on_message(command(["broadcast_pin", f"broadcast_pin@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_pin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.1)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"» ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ɪɴ {sent} ɢʀᴏᴜᴩs.\n» ᴩɪɴɴᴇᴅ ɪɴ {pin} ɢʀᴏᴜᴩs."
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**ᴜsᴀɢᴇ**:\n\n/broadcast_pin (`message`) ᴏʀ (`reply to message`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.1)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"» ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ɪɴ {sent} ɢʀᴏᴜᴩs.\n» ᴩɪɴɴᴇᴅ ɪɴ {pin} ɢʀᴏᴜᴩs."
    )


@Client.on_message(command(["stats", f"stats@{uname}"]) & ~filters.edited)
@sudo_users_only
async def bot_statistic(c: Client, message: Message):
    name = me_bot.first_name
    chat_id = message.chat.id
    msg = await c.send_message(
        chat_id, "» ᴄᴏʟʟᴇᴄᴛɪɴɢ sᴛᴀᴛs..."
    )
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gbans_usertl = await get_gbans_count()
    tgm = f"""
😴 sᴛᴀᴛɪsᴛɪᴄs ᴏғ [{name}](https://t.me/{uname})`:`

» **ɢʀᴏᴜᴩs** : `{served_chats}`
» **ᴜsᴇʀs** : `{served_users}`
» **ɢʙᴀɴɴᴇᴅ** : `{gbans_usertl}`

» **ᴩʏᴛʜᴏɴ** : `{pyver}`
» **ᴩʏ∆ᴛɢ-ᴄᴀʟʟs** : `{pytgver.__version__}`
» **ᴩʏʀᴏɢʀᴀᴍ** : `{pyrover}`

😎 ʙᴏᴛ ᴠᴇʀsɪᴏɴ: `{ver}` 😎"""
    await msg.edit(tgm, disable_web_page_preview=True)


@Client.on_message(command(["calls", "activevc", f"calls@{uname}"]) & ~filters.edited)
@sudo_users_only
async def active_group_calls(c: Client, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"» ᴇʀʀᴏʀ: `{e}`")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await c.get_chat(x)).title
        except BaseException:
            title = "Private Group"
        if (await c.get_chat(x)).username:
            data = (await c.get_chat(x)).username
            text += (
                f"**{j + 1}.** [{title}](https://t.me/{data}) [`{x}`]\n"
            )
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛs ғᴏᴜɴᴅ ᴏɴ ʙᴏᴛ's sᴇʀᴠᴇʀ")
    else:
        await message.reply_text(
            f"» **ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛs:**\n\n{text}\n» ᴛʜɪs ɪs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛs ᴏɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ.",
            disable_web_page_preview=True,
        )
