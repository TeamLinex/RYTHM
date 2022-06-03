from driver.core import me_bot, me_user
from driver.queues import QUEUE
from driver.decorators import check_blacklist
from program.utils.inline import menu_markup, stream_markup

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
    SUDO_USERS,
    OWNER_ID,
)


@Client.on_callback_query(filters.regex("home_start"))
@check_blacklist()
async def start_set(_, query: CallbackQuery):
    await query.answer("home start")
    await query.edit_message_text(
        f"""💔 ʜᴇʏ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !\n
   💞 ɪ ᴀᴍ [{me_bot.first_name}](https://t.me/{me_bot.username}) ᴀ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴍᴀᴅᴇ ғᴏʀ ᴩʟᴀʏɪɴɢ ᴀᴜᴅɪᴏs ᴀɴᴅ ᴠɪᴅᴇᴏs ɪɴ ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏᴄʜᴀᴛs.

🥱 ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ʟɪsᴛᴇᴅ ɪɴ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ, ᴄʟɪᴄᴋ ᴏɴ ɪᴛ ᴛᴏ ᴋɴᴏᴡ ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs. 🥱
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🥺 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 🥺", url=f"https://t.me/{me_bot.username}?startgroup=true")
                ],[
                    InlineKeyboardButton("• ʜᴇʟᴩ •", callback_data="command_list"),
                    InlineKeyboardButton("• ᴀʙᴏᴜᴛ •", callback_data="about_me") 
                ],[
                    InlineKeyboardButton("• ᴍᴀɪɴᴛᴀɪɴᴇʀ •", url=f"https://t.me/{OWNER_USERNAME}"),
                    InlineKeyboardButton("• sᴜᴩᴩᴏʀᴛ •", url=f"https://t.me/{GROUP_SUPPORT}")
                ],[
                    InlineKeyboardButton("• sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ •", url="https://telegra.ph/file/3d245c9fa9e2c7851cc8f.jpg")
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("quick_use"))
@check_blacklist()
async def quick_set(_, query: CallbackQuery):
    await query.answer("quick bot usage")
    await query.edit_message_text(
        f"""😅 ᴀ sɪᴍᴩʟᴇ ɢᴜɪᴅᴇ ғᴏʀ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ !

😴 » /play <song name/youtube link> : sᴛᴀʀᴛs ᴩʟᴀʏɪɴɢ ᴛʜᴇ sᴏɴɢ ʀᴇǫᴜᴇsᴛᴇᴅ ᴡɪᴛʜ ɪᴛ.

😴 » /vplay <song name/youtube link> : sᴀᴍᴇ ᴀs ᴩʟᴀʏ ʙᴜᴛ ᴜsᴇ ᴛʜɪs ғᴏʀ ᴩʟᴀʏɪɴɢ ᴠɪᴅᴇᴏs.

😴 » /vstream - sᴀᴍᴇ ᴀs ᴠᴩʟᴀʏ ʙᴜᴛ ᴜsᴇ ᴛʜɪs ғᴏʀ ᴩʟᴀʏɪɴɢ ʟɪᴠᴇ sᴛʀᴇᴀᴍs ᴏʀ ᴍ3ᴜ8 ʟɪɴᴋs.

❓ ɴᴇᴇᴅ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ? ᴀsᴋ ɪᴛ ɪɴ [sᴜᴩᴩᴏʀᴛ ɢʀᴏᴜᴩ](https://t.me/{GROUP_SUPPORT}).""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="user_guide")]]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("user_guide"))
@check_blacklist()
async def guide_set(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""😅 ᴀ sɪᴍᴩʟᴇ ɢᴜɪᴅᴇ ᴛᴏ ᴀᴅᴅɪɴɢ ᴛʜɪs ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴩ ᴀɴᴅ ᴩʟᴀʏɪɴɢ ғᴏʀ ғɪʀsᴛ ᴛɪᴍᴇ !

1.| ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴩ ᴠɪᴀ ᴀᴅᴅ ᴍᴇ ʙᴜᴛᴛᴏɴ.
2.| ᴛʜᴇɴ ᴩʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ ᴀɴᴅ ɢɪᴠᴇ ᴀʟʟ ᴩᴇʀᴍɪssɪᴏɴs ᴇᴄxᴄᴇᴩᴛ ᴛʜᴇ ʟᴀsᴛ ᴏɴᴇ `ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ`.
3.| ᴀғᴛᴇʀ ᴩʀᴏᴍᴏᴛɪɴɢ, ᴛʏᴩᴇ /refresh or /reload or /admincache sᴏ ᴛʜᴀᴛ ʙᴏᴛ ᴄᴀɴ ʀᴇғʀᴇsʜ ᴛʜᴇ ᴀᴅᴍɪɴs ʟɪsᴛ ᴀɴᴅ ᴄᴀɴ sᴛᴀʀᴛ ᴩʟᴀʏɪɴɢ.
3.|  ᴀғᴛᴇʀ ᴛʜᴀᴛᴀᴅᴅ @{me_user.username} ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴩ ᴏʀ ᴛʏᴩᴇ /join ᴛᴏ ɪɴᴠɪᴛᴇ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴏʀ ʟᴇᴀᴠᴇ ɪᴛ ᴀs ɪᴛ ɪs ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴡɪʟʟ ᴊᴏɪɴ ɪᴛsᴇʟғ ᴡʜᴇɴ ʏᴏᴜ ᴩʟᴀʏ sᴏᴍᴇᴛʜɪɴɢ ғᴏʀ ғɪʀsᴛ ᴛɪᴍᴇ.
4.|  ᴍᴀᴋᴇ ᴀᴜʀᴇ ᴛᴏ sᴛᴀʀᴛ ᴠɪᴅᴇᴏᴄʜᴀᴛ ᴏғ ʏᴏᴜʀ ɢʀᴏᴜᴩ ʙᴇғᴏʀᴇ ᴩʟᴀʏɪɴɢ.

`• ᴇᴠᴇʀʏᴛʜɪɴɢ's ɪs ᴅᴏɴᴇ ɴᴏᴡ, ᴇɴᴊᴏʏ •`

💡 ᴀғᴛᴇʀ ᴇxᴩʟᴀɪɴɪɴɢ ᴇᴠᴇʀʏᴛʜɪɴɢ ɪғ ʏᴏᴜ sᴛɪʟʟ ʜᴀᴠᴇ ǫᴜᴇsᴛɪᴏɴs ᴀsᴋ ɪᴛ ɪɴ @{GROUP_SUPPORT} ᴅᴜᴍᴍʏ.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("» ǫᴜɪᴄᴋ ɢᴜɪᴅᴇ «", callback_data="quick_use")
                ],[
                    InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("command_list"))
@check_blacklist()
async def commands_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""💔 **ʜᴇʏ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ʟɪsᴛᴇᴅ ɪɴ ᴛʜᴇsᴇ ᴛʜʀᴇᴇ ʙᴜᴛᴛᴏɴs !

ᴀʟʟ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ (`! / .`)""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("• ᴀᴅᴍɪɴs •", callback_data="admin_command"),
                ],[
                    InlineKeyboardButton("• ᴇᴠᴇʀʏᴏɴᴇ •", callback_data="user_command"),
                ],[
                    InlineKeyboardButton("• sɪᴍᴩʟᴇ ɢᴜɪᴅᴇ •", callback_data="user_guide"),
                ],[
                    InlineKeyboardButton("• sᴜᴅᴏᴇʀs •", callback_data="sudo_command"),
                    InlineKeyboardButton("• ᴅᴇᴠᴇʟᴏᴩᴇʀs •", callback_data="owner_command"),
                ],[
                    InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("user_command"))
@check_blacklist()
async def user_set(_, query: CallbackQuery):
    await query.answer("basic commands")
    await query.edit_message_text(
        f"""😉 ᴄᴏᴍᴍᴀɴᴅs ᴛʜᴀᴛ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ʙʏ ᴇᴠᴇʀʏᴏɴᴇ

» /play (song name/youtube link) - ᴩʟᴀʏ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ ᴀs ᴀᴜᴅɪᴏ.
» /stream (m3u8/youtube live link) - sᴛᴀʀᴛs ᴩʟᴀʏɪɴɢ ʟɪᴠᴇ sᴛʀᴇᴀᴍ ᴀs ᴀᴜᴅɪᴏ.
» /vplay (video name/youtube link) - ᴩʟᴀʏ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ ᴀs ᴠɪᴅᴇᴏ.
» /vstream (m3u8/youtube live link) - sᴛᴀʀᴛs ᴩʟᴀʏɪɴɢ ʟɪᴠᴇ sᴛʀᴇᴀᴍ ᴀs ᴠɪᴅᴇᴏ.
» /playlist - sʜᴏᴡs ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ ᴀɴᴅ ᴡʜᴏʟᴇ ǫᴜᴇᴜᴇᴅ ᴩʟᴀʏʟɪsᴛ.
» /lyric (query) - sᴇᴀʀᴄʜ ғᴏʀ ᴀ sᴏɴɢ ʟʏʀɪᴄs.
» /video (query) - ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴠɪᴅᴇᴏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ.
» /song (query) - ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴀᴜᴅɪᴏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ.
» /search (query) - sᴇᴀʀᴄʜ ᴛʜᴇ ɢɪᴠᴇɴ ǫᴜᴇʀʏ ᴏɴ ʏᴏᴜᴛᴜʙᴇ ᴀɴᴅ sʜᴏᴡs ᴛʜᴇ ʀᴇsᴜʟᴛ ᴡɪᴛʜ ɪᴛ's ʟɪɴᴋs.
» /ping - sʜᴏᴡs ᴛʜᴇ ʙᴏᴛ ᴩɪɴɢ.
» /uptime - sʜᴏᴡs ᴛʜᴇ ᴜᴩᴛɪᴍᴇ sᴛᴀᴛᴜs ᴏғ ᴛʜᴇ ʙᴏᴛ.
» /alive - ᴄʜᴇᴄᴋs ᴛʜᴀᴛ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ.""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("admin_command"))
@check_blacklist()
async def admin_set(_, query: CallbackQuery):
    await query.answer("admin commands")
    await query.edit_message_text(
        f"""🥺 ᴄᴏᴍᴍᴀɴᴅs ᴛʜᴀᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ ᴀᴅᴍɪɴs

» /pause - ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴏɴɢ.
» /resume - ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴏɴɢ.
» /skip - sᴋɪᴩ ᴛᴏ ᴛʜᴇ ɴᴇxᴛ sᴏɴɢ ɪɴ ǫᴜᴇᴜᴇ.
» /end - ᴄʟᴇᴀʀ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ʟᴇᴀᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛ.
» /volume `1-200` - ᴀᴅᴊᴜsᴛ ᴛʜᴇ ᴠᴏʟᴜᴍᴇ ᴏғ ᴀssɪsᴛᴀɴᴛ.
» /reload - ʀᴇғʀᴇsʜ ᴛʜᴇ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ.
» /join - ʀᴇǫᴜᴇsᴛs ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀᴛ.
» /leave - ᴏʀᴅᴇʀ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ ʟᴇᴀᴠᴇ ᴛʜᴇ ᴄʜᴀᴛ.
» /startvc - sᴛᴀʀᴛs ᴠɪᴅᴇᴏᴄʜᴀᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ.
» /stopvc - ᴇɴᴅ ᴛʜᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴩ.""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("sudo_command"))
@check_blacklist()
async def sudo_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in SUDO_USERS:
        await query.answer("🤬 ᴛᴜᴊʜᴇ sᴜᴅᴏ ᴋɪsɴᴇ ʙᴀɴᴀʏᴀ ʙsᴅᴋ, ʙʜᴀᴀɢ ʟᴀᴜᴅᴇ 🤬", show_alert=True)
        return
    await query.answer("sudo commands")
    await query.edit_message_text(
        f"""😜 ᴄᴏᴍᴍᴀɴᴅs ᴛʜᴀᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ sᴜᴅᴏᴇʀs.

» /stats - sʜᴏᴡs ᴛʜᴇ sᴛᴀᴛɪsᴛɪᴄs ᴏғ ᴛʜᴇ ʙᴏᴛ.
» /calls - sʜᴏᴡs ʏᴏᴜ ᴛʜᴇ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛs ᴏɴ ʙᴏᴛ sᴇʀᴠᴇʀ.
» /block (`chat_id`) - ғᴏʀ ʙʟᴀᴄᴋʟɪsᴛɪɴɢ ᴀɴʏ ᴄʜᴀᴛ ғᴏʀ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ.
» /unblock (`chat_id`) - ᴛᴏ ᴀʟʟᴏᴡ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ ᴛᴏ ᴜsᴇ ʏᴏᴜʀ ʙᴏᴛ ᴀɢᴀɪɴ.
» /blocklist - sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs.
» /speedtest - ʀᴜɴs ᴀ sᴩᴇᴇᴅᴛᴇsᴛ.
» /sysinfo - sʜᴏᴡ ᴛʜᴇ sʏsᴛᴇᴍ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.
» /logs - sᴇɴᴅs ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ʟᴏɢs ᴏғ ᴛʜᴇ ʙᴏᴛ.
» /eval - ʀᴜɴs ᴛʜᴇ ᴄᴏᴅᴇ ᴏɴ ᴛʜᴇ ᴛᴇʀᴍɪɴᴀʟ.
» /sh - ᴀᴩᴩʀᴏx sᴀᴍᴇ ᴀs ᴇᴠᴀʟ.""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("owner_command"))
@check_blacklist()
async def owner_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in OWNER_ID:
        await query.answer("🤬 ᴀᴄᴄʜᴀ ᴛᴏʜ ᴛᴜ ᴋʜᴜᴅᴋᴏ ᴏᴡɴᴇʀ sᴀᴍᴀᴊʜᴛᴀ ʜᴀɪ ʙᴇʜᴇɴ ᴋᴇ ʟᴜɴᴅ, ᴛᴇʀɪ ɢᴀɴᴅ ᴍᴀɪɴ ʙᴀᴍʙᴏᴏ ᴅᴀᴀʟᴋᴇ ᴛᴀᴍʙᴏᴏ ʟᴀɢᴀᴜɴɢᴀ 🤬", show_alert=True)
        return
    await query.answer("owner commands")
    await query.edit_message_text(
        f"""😘 ᴄᴏᴍᴍᴀɴᴅs ᴛʜᴀᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ʙʏ ᴍʏ ʙᴀʙʏ

» /gban (`username` or `user_id`) - ғᴏʀ ʙᴀɴɴɪɴɢ ᴜsᴇʀ ɢʟᴏʙᴀʟʟʏ.
» /ungban (`username` or `user_id`) - ғᴏʀ ʀᴇᴍᴏᴠɪɴɢ ɢʟᴏʙᴀʟ ʙᴀɴ ғʀᴏᴍ ᴛʜᴇ ʙᴀɴɴᴇᴅ ᴜsᴇʀ.
» /update - ғᴇᴛᴄʜ ᴛʜᴇ ᴜᴩsᴛʀᴇᴀᴍ ᴀɴᴅ ᴜᴩᴅᴀᴛᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ʟᴀᴛᴇsᴛ ᴠᴇʀsɪᴏɴ.
» /restart - ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴏɴ ᴛʜᴇ sᴇʀᴠᴇʀ.
» /leaveall - ᴏʀᴅᴇʀ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ ʟᴇᴀᴠᴇ ᴀʟʟ ᴄʜᴀᴛs.
» /leavebot (`chat id`) - ᴏʀᴅᴇʀs ᴛʜᴇ ʙᴏᴛ ʟᴇᴀᴠᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴄʜᴀᴛ.
» /broadcast (`message`) - ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ɢɪᴠᴇɴ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴩs ᴛʜᴀᴛ ᴀʀᴇ sᴛᴏʀᴇᴅ ᴏɴ ʙᴏᴛ's sᴇʀᴠᴇʀ.
» /broadcast_pin (`message`) - sᴀᴍᴇ ᴀs ʙʀᴏᴀᴅᴄᴀsᴛ ʙᴜᴛ ᴡɪᴛʜ ᴏɴᴇ ᴇxᴛʀᴀ ᴛʜɪɴɢ ɪs ɪᴛ ᴩɪɴs ᴛʜᴇ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴩs.""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("stream_menu_panel"))
@check_blacklist()
async def at_set_markup_menu(_, query: CallbackQuery):
    user_id = query.from_user.id
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs ! 😂", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.message.from_user.id
    buttons = menu_markup(user_id)
    if chat_id in QUEUE:
        await query.answer("» ᴍᴇɴᴜ ᴏᴩᴇɴᴇᴅ")
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await query.answer("» ɴᴏᴛʜɪɴɢ ɪs ᴩʟᴀʏɪɴɢ.", show_alert=True)


@Client.on_callback_query(filters.regex("stream_home_panel"))
@check_blacklist()
async def is_set_home_menu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs ! 😂", show_alert=True)
    await query.answer("» ᴍᴇɴᴜ ᴄʟᴏsᴇᴅ")
    user_id = query.message.from_user.id
    buttons = stream_markup(user_id)
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex("set_close"))
@check_blacklist()
async def on_close_menu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs ! 😂", show_alert=True)
    await query.message.delete()


@Client.on_callback_query(filters.regex("close_panel"))
@check_blacklist()
async def in_close_panel(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("about_me"))
@check_blacklist()
async def user_set(_, query: CallbackQuery):
    await query.answer("About Elsa")
    await query.edit_message_text(
        f"""😉 ᴀʙᴏᴜᴛ [{me_bot.first_name}](https://t.me/{me_bot.username})


ʜᴇʏ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !,

 ɪ ᴀᴍ [{me_bot.first_name}](https://t.me/{me_bot.username}), ᴀ ᴩᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴍᴀᴅᴇ ғᴏʀ ᴩʟᴀʏɪɴɢ sᴏɴɢs ɪɴ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴩ ᴠᴏɪᴄᴇᴄʜᴀᴛs.
• ɪ ᴄᴀɴ ᴩʟᴀʏ ᴀᴜᴅɪᴏs ᴀɴᴅ ᴠɪᴅᴇᴏs ɪɴ ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏᴄʜᴀᴛs ʙᴀsᴇᴅ ᴏɴ ᴩʏʀᴏɢʀᴀᴍ ᴀɴᴅ ᴩʏ-ᴛɢᴄᴀʟʟs.
• ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ʟɪsᴛᴇᴅ ɪɴ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ, ᴄʟɪᴄᴋ ᴏɴ ɪᴛ ᴛᴏ ᴋɴᴏᴡ ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs. 🥱

» ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴀʙᴏᴜᴛ ᴍᴇ ᴀsᴋ ɪᴛ ɪɴ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](https://t.me/{GROUP_SUPPORT}) ᴀɴᴅ ᴛᴏ ᴋᴇᴇᴩ ʏᴏᴜʀsᴇʟғ ᴜᴩᴅᴀᴛᴇᴅ ᴊᴏɪɴ [BotDuniya](https://t.me/{GROUP_SUPPORT}) «""",
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton("• ᴅᴇᴠᴇʟᴏᴩᴇʀ •", url=f"https://t.me/{OWNER_USERNAME}"),
                ],[
                    InlineKeyboardButton("• sᴜᴩᴩᴏʀᴛ •", url=f"https://t.me/{GROUP_SUPPORT}"),
                ],[
                    InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="home_start"),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )

