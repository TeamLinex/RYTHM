import wget
import yt_dlp
import traceback
import requests
import lyricsgenius

from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from config import BOT_USERNAME as bn
from driver.decorators import check_blacklist
from driver.filters import command
from driver.utils import remove_if_exists


@Client.on_message(command(["song", f"song@{bn}"]) & ~filters.edited)
@check_blacklist()
async def song_downloader(_, message):
    await message.delete()
    query = " ".join(message.command[1:])
    m = await message.reply("🔎")
    ydl_ops = {
        'format': 'bestaudio[ext=m4a]',
        'geo-bypass': True,
        'noprogress': True,
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
        'extractor-args': 'youtube:player_client=all',
        'nocheckcertificate': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quite': True,
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        await m.edit("😴 sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ ᴏɴ ʏᴏᴜᴛᴜʙᴇ.\n\n» ᴍᴀʏʙᴇ ᴛᴜɴᴇ ɢᴀʟᴛɪ ʟɪᴋʜᴀ ʜᴏ, ᴩᴀᴅʜᴀɪ - ʟɪᴋʜᴀɪ ᴛᴏʜ ᴋᴀʀᴛᴀ ɴᴀʜɪ ᴛᴜ !")
        print(str(e))
        return
    await m.edit("» ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"» ᴜᴩʟᴏᴀᴅᴇᴅ ʙʏ @{bn}"
        host = str(info_dict["uploader"])
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("» ᴜᴩʟᴏᴀᴅɪɴɢ...")
        await message.reply_audio(
            audio_file,
            caption=rep,
            performer=host,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        await m.delete()

    except Exception as e:
        await m.edit("» ᴇʀʀᴏʀ ᴋɪ ᴍᴋʙ, ᴏᴡɴᴇʀ ᴋᴏ ʙᴏʟ ɢᴀ*ᴅ ɴᴀ ᴍᴀʀᴀᴀʏᴇ ᴀᴜʀ ɪsᴋᴏ ғɪx ᴋᴀʀᴇ.")
        print(e)
    try:
        remove_if_exists(audio_file)
        remove_if_exists(thumb_name)
    except Exception as e:
        print(e)


@Client.on_message(
    command(["vsong", f"vsong@{bn}", "video", f"video@{bn}"]) & ~filters.edited
)
@check_blacklist()
async def video_downloader(_, message):
    await message.delete()
    ydl_opts = {
        "format": "best",
        "geo-bypass": True,
        "noprogress": True,
        "user-agent": "Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "extractor-args": "youtube:player_client=all",
        "nocheckcertificate": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("» ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        traceback.print_exc()
        return await msg.edit(f"» ᴇʀʀᴏʀ: `{e}`")
    preview = wget.download(thumbnail)
    await msg.edit("» ᴜᴩʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        remove_if_exists(file_name)
        await msg.delete()
    except Exception as e:
        print(e)


@Client.on_message(command(["lyric", f"lyric@{bn}", "lyrics"]))
@check_blacklist()
async def get_lyric_genius(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n\n/lyrics ʙʜᴀᴀɢ ᴍᴀᴅʜᴀʀᴄʜᴏᴅ sᴏɴɢ")
    m = await message.reply_text("» sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ʟʏʀɪᴄs...")
    query = message.text.split(None, 1)[1]
    api = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    data = lyricsgenius.Genius(api)
    data.verbose = False
    result = data.search_song(query, get_full_info=False)
    if result is None:
        return await m.edit("» `404` ʟʏʀɪᴄs ɴᴏᴛ ғᴏᴜɴᴅ, ɢᴀʟᴀᴛ ʟɪᴋʜᴀ ʜᴏɢᴀ ᴛᴜɴᴇ ᴍᴀɪɴ ᴄᴏɴғɪʀᴍ ʜᴜ ᴋʏᴜɴᴋɪ ᴛᴜ ᴩᴀᴅʜᴛᴀ - ʟɪᴋʜᴛᴀ ᴛᴏʜ ʜᴀɪ ɴᴀʜɪ")
    xxx = f"""
**ᴛɪᴛʟᴇ:** {query}
**ᴀʀᴛɪsᴛ:** {result.artist}
**ʟʏʀɪᴄs:**

{result.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**ᴏᴜᴛᴩᴜᴛ:**\n\n`ᴀᴛᴛᴀᴄʜᴇᴅ ʟʏʀɪᴄs`",
            quote=False,
        )
        remove_if_exists(filename)
    else:
        await m.edit(xxx)
