from config import BOT_USERNAME
from driver.decorators import check_blacklist
from driver.filters import command
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch


@Client.on_message(command(["search", f"search@{BOT_USERNAME}"]) & ~filters.edited)
@check_blacklist()
async def youtube_search(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("/search **ɴᴇᴇᴅs sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ sᴇᴀʀᴄʜ ɪᴛ ᴏɴ ʏᴏᴜᴛᴜʙᴇ !**")
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("» **sᴇᴀʀᴄʜɪɴɢ...**")
    results = YoutubeSearch(query, max_results=5).to_dict()
    text = ""
    for i in range(5):
        try:
            text += f"• **ɴᴀᴍᴇ:** __{results[i]['title']}__\n"
            text += f"• **ᴅᴜʀᴀᴛɪᴏɴ:** `{results[i]['duration']}`\n"
            text += f"• **ᴠɪᴇᴡs:** `{results[i]['views']}`\n"
            text += f"• **ᴄʜᴀɴɴᴇʟ:** {results[i]['channel']}\n"
            text += f"• **ʟɪɴᴋ:** https://www.youtube.com{results[i]['url_suffix']}\n\n"
        except IndexError:
            break
    await m.edit_text(
        text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close_panel")]]
        ),
    )
