import os
import sys

from git import Repo
from os import system, execle, environ
from git.exc import InvalidGitRepositoryError

from pyrogram.types import Message
from pyrogram import Client, filters

from program import LOGS
from config import UPSTREAM_REPO, BOT_USERNAME

from driver.filters import command
from driver.decorators import bot_creator


def gen_chlog(repo, diff):
    upstream_repo_url = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = ""
    tldr_log = ""
    ch = f"<b>updates for <a href={upstream_repo_url}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b>"
            f"<a href={upstream_repo_url.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        )
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if "upstream" in repo.remotes:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", UPSTREAM_REPO)
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


@Client.on_message(command(["update", f"update@{BOT_USERNAME}"]) & ~filters.edited)
@bot_creator
async def update_bot(_, message: Message):
    chat_id = message.chat.id
    msg = await message.reply("» sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴜᴩᴅᴀᴛᴇs, ɪғ ғᴏᴜɴᴅ ɪ ᴡɪʟʟ ᴜᴩᴅᴀᴛᴇ ᴍʏsᴇʟғ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ...")
    update_avail = updater()
    if update_avail:
        await msg.edit("» ʙᴏᴛ ɪs ɴᴏᴡ ᴜᴩᴅᴀᴛᴇᴅ ᴡɪᴛʜ ᴛʜᴇ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏsɪᴛᴏʀʏ !\n\n• ɴᴏᴡ ʟᴇᴛ ᴍᴇ ʀᴇsᴛᴀʀᴛ sᴏ ᴛʜᴀᴛ ɪ ᴄᴀɴ sᴇᴛᴜᴩ ᴀʟʟ ᴛʜᴇ ᴄʜᴀɴɢᴇs.")
        system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
        execle(sys.executable, sys.executable, "main.py", environ)
        return
    await msg.edit(f"» ʙᴏᴛ ɪs **ᴜᴩ-ᴛᴏ-ᴅᴀᴛᴇ** ᴡɪᴛʜ [ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ]({UPSTREAM_REPO}/tree/main) ɴᴏ ᴍᴏʀᴇ ɴᴇᴡ ᴄᴏᴍᴍɪᴛs ғᴏᴜɴᴅ.", disable_web_page_preview=True)


@Client.on_message(command(["restart", "reboot", f"restart@{BOT_USERNAME}"]) & ~filters.edited)
@bot_creator
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply_text("» ʀᴇsᴛᴀʀᴛɪɴɢ...")
        LOGS.info("[INFO]: BOT RESTARTED !")
    except BaseException as err:
        LOGS.info(f"[ERROR]: {err}")
        return
    await msg.edit_text("✅ ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴀᴛʀᴛᴇᴅ !\n\n» ᴡɪʟʟ sᴛᴀʀᴛ ᴡᴏʀᴋɪɴɢ ᴀɢᴀɪɴ ɪɴ ғᴇᴡ sᴇᴄᴏɴᴅs.")
    os.system(f"kill -9 {os.getpid()} && python3 main.py")
