import asyncio

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from driver.core import me_bot
from driver.filters import command, other_filters
from driver.decorators import bot_creator
from driver.database.dbchat import get_served_chats
from driver.database.dbpunish import add_gban_user, is_gbanned_user, remove_gban_user

from config import OWNER_ID, SUDO_USERS, BOT_USERNAME as bn


@Client.on_message(command(["gban", f"gban@{bn}"]) & other_filters)
@bot_creator
async def global_banned(c: Client, message: Message):
    BOT_NAME = me_bot.first_name
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**ᴜsᴀɢᴇ:**\n\n/gban [username | user_id]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await c.get_users(user)
        from_user = message.from_user
        BOT_ID = me_bot.id
        if user.id == from_user.id:
            await message.reply_text("» ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ʏᴏᴜʀsᴇʟғ ʙᴀʙʏ !")
        elif user.id == BOT_ID:
            await message.reply_text("» ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ɢʙᴀɴ ᴍʏsᴇʟғ, ʙʟᴏᴏᴅʏ ɴᴏᴏʙs !")
        elif user.id in SUDO_USERS:
            await message.reply_text("» ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ᴍʏ ᴇx !")
        elif user.id in OWNER_ID:
            await message.reply_text("» ʏᴏᴜ ʙʟᴏᴏᴅʏ ᴍᴏᴛʜᴇʀғᴜ*ᴋᴇʀ, ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ɢʙᴀɴ ᴍʏ ʙᴀʙʏ, ɪ ᴡɪʟʟ ғᴜ*ᴋ ʏᴏᴜ ʜᴀʀᴅ ᴀɴᴅ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ʙᴇ ᴀʙʟᴇ ᴛᴏ ғᴜ*ᴋ ᴀɴʏᴏɴᴇ ᴀɢᴀɪɴ !")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"😈 **ɢʟᴀᴏʙᴀʟʟʏ ʙᴀɴɴɪɴɢ {user.mention}**\n👿ᴇxᴩᴇᴄᴛᴇᴅ ᴛɪᴍᴇ: `{len(served_chats)}`"
            )
            number_of_chats = 0
            for num in served_chats:
                try:
                    await c.ban_chat_member(num, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
😈 **ɴᴇᴡ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ [{BOT_NAME}](https://t.me/{bn})

**ᴏʀɪɢɪɴ:** {message.chat.title} [`{message.chat.id}`]
**sᴜᴅᴏ:** {from_user.mention}
**ᴜsᴇʀ:** {user.mention}
**ᴜsᴇʀ ɪᴅ:** `{user.id}`
**ᴄʜᴀᴛs:** `{number_of_chats}`"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    BOT_ID = me_bot.id
    if user_id == from_user_id:
        await message.reply_text("» ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ʏᴏᴜʀsᴇʟғ !")
    elif user_id == BOT_ID:
        await message.reply_text("» ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ɢʙᴀɴ ᴍʏsᴇʟғ, ʙʟᴏᴏᴅʏ ɴᴏᴏʙs !")
    elif user_id in SUDO_USERS:
        await message.reply_text("» ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ᴍʏ ᴇx !")
    elif user_id in OWNER_ID:
        await message.reply_text("» ʏᴏᴜ ʙʟᴏᴏᴅʏ ᴍᴏᴛʜᴇʀғᴜ*ᴋᴇʀ, ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ɢʙᴀɴ ᴍʏ ʙᴀʙʏ, ɪ ᴡɪʟʟ ғᴜ*ᴋ ʏᴏᴜ ʜᴀʀᴅ ᴀɴᴅ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ʙᴇ ᴀʙʟᴇ ᴛᴏ ғᴜ*ᴋ ᴀɴʏᴏɴᴇ ᴀɢᴀɪɴ !")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("» ᴛʜɪs ᴍᴏᴛʜᴇʀғᴜ*ᴋᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ !")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"😈 **ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴɪɴɢ {mention}**\n👿 ᴇxᴩᴇᴄᴛᴇᴅ ᴛɪᴍᴇ: `{len(served_chats)}`"
            )
            number_of_chats = 0
            for num in served_chats:
                try:
                    await c.ban_chat_member(num, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
😈 **ɴᴇᴡ ɢʟᴏʙᴀʟ ᴏɴ [{BOT_NAME}](https://t.me/{bn})

**ᴏʀɪɢɪɴ:** {message.chat.title} [`{message.chat.id}`]
**sᴜᴅᴏ:** {from_user_mention}
**ᴜsᴇʀ:** {mention}
**ᴜsᴇʀ ɪᴅ:** `{user_id}`
**ᴄʜᴀᴛs:** `{number_of_chats}`"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@Client.on_message(command(["ungban", f"ungban@{bn}"]) & other_filters)
@bot_creator
async def ungban_global(c: Client, message: Message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**ᴜsᴀɢᴇ:**\n\n/ungban [username | user_id]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await c.get_users(user)
        from_user = message.from_user
        BOT_ID = me_bot.id
        if user.id == from_user.id:
            await message.reply_text("» ɪ ᴀʟʀᴇᴀᴅʏ ᴛᴏʟᴅ ʏᴏᴜ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ʏᴏᴜʀsᴇʟғ sᴏ ʜᴏᴡ ᴛʜᴇ ғᴜ*ᴋ ʏᴏᴜ'ʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴜɴɢʙᴀɴ ʏᴏᴜʀsᴇʟғ !")
        elif user.id == BOT_ID:
            await message.reply_text("» ʏᴏᴜ ʙʟᴏᴏᴅʏ ɴᴏᴏʙ, ɪ ᴀᴍ ᴛᴇʟʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴀɢᴀɪɴ ᴇʟsᴇ ɪ ᴡɪʟʟ ᴛᴇʟʟ ᴍʏ ʙᴀʙʏ ᴛᴏ ғᴜ*ᴋ ʏᴏᴜ ᴜᴩ !")
        elif user.id in SUDO_USERS:
            await message.reply_text("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴛʜᴇ sᴛᴀᴛᴇᴍᴇɴᴛ ᴛʜᴀᴛɪ ᴛᴏʟᴅ ʏᴏᴜ ғᴇᴡ ʏᴇᴀʀs ᴀɢᴏ ɪ ᴡɪʟʟ ɴᴏᴛ ɢʙᴀɴ ᴍʏ ᴇx sᴏ ʜᴏᴡ ɪ ᴄᴀɴ ᴜɴɢʙᴀɴ ʜɪᴍ !")
        elif user.id in OWNER_ID:
            await message.reply_text("» ʀᴇᴀᴅ ᴛʜɪs sᴛᴀᴛᴇᴍᴇɴᴛ ʟᴀsᴛ ᴛɪᴍᴇ, ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴛᴇʟʟ ʏᴏᴜ ᴀɢᴀɪɴ-ɴ-ᴀɢᴀɪɴ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ᴍʏ ʙᴀʙʏ !")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("» ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ɢʙᴀɴɴᴇᴅ !")
            else:
                msg = await message.reply_text("» ᴜɴɢʙᴀɴɴɪɴɢ...")
                await remove_gban_user(user.id)
                served_chats = []
                chats = await get_served_chats()
                for chat in chats:
                    served_chats.append(int(chat["chat_id"]))
                number_of_chats = 0
                for num in served_chats:
                    try:
                        await c.unban_chat_member(num, user.id)
                        number_of_chats += 1
                        await asyncio.sleep(1)
                    except FloodWait as e:
                        await asyncio.sleep(int(e.x))
                    except BaseException:
                        pass
                await msg.edit_text("» ᴜɴɢʙᴀɴɴᴇᴅ.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    BOT_ID = me_bot.id
    if user_id == from_user_id:
        await message.reply_text("» ɪ ᴀʟʀᴇᴀᴅʏ ᴛᴏʟᴅ ʏᴏᴜ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ʏᴏᴜʀsᴇʟғ sᴏ ʜᴏᴡ ᴛʜᴇ ғᴜ*ᴋ ʏᴏᴜ'ʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴜɴɢʙᴀɴ ʏᴏᴜʀsᴇʟғ !")
    elif user_id == BOT_ID:
        await message.reply_text("» ʏᴏᴜ ʙʟᴏᴏᴅʏ ɴᴏᴏʙ, ɪ ᴀᴍ ᴛᴇʟʟɪɴɢ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴀɢᴀɪɴ ᴇʟsᴇ ɪ ᴡɪʟʟ ᴛᴇʟʟ ᴍʏ ʙᴀʙʏ ᴛᴏ ғᴜ*ᴋ ʏᴏᴜ ᴜᴩ !")
    elif user_id in SUDO_USERS:
        await message.reply_text("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴛʜᴇ sᴛᴀᴛᴇᴍᴇɴᴛ ᴛʜᴀᴛɪ ᴛᴏʟᴅ ʏᴏᴜ ғᴇᴡ ʏᴇᴀʀs ᴀɢᴏ ɪ ᴡɪʟʟ ɴᴏᴛ ɢʙᴀɴ ᴍʏ ᴇx sᴏ ʜᴏᴡ ɪ ᴄᴀɴ ᴜɴɢʙᴀɴ ʜɪᴍ !")
    elif user_id in OWNER_ID:
        await message.reply_text("» ʀᴇᴀᴅ ᴛʜɪs sᴛᴀᴛᴇᴍᴇɴᴛ ʟᴀsᴛ ᴛɪᴍᴇ, ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴛᴇʟʟ ʏᴏᴜ ᴀɢᴀɪɴ-ɴ-ᴀɢᴀɪɴ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ᴍʏ ʙᴀʙʏ !")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ɢʙᴀɴɴᴇᴅ !")
        else:
            msg = await message.reply_text("» ᴜɴɢʙᴀɴɴɪɴɢ...")
            await remove_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            number_of_chats = 0
            for num in served_chats:
                try:
                    await c.unban_chat_member(num, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except BaseException:
                    pass
                await msg.edit_text("» ᴜɴɢʙᴀɴɴᴇᴅ.")
