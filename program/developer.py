import re
import sys
import subprocess
import traceback

from time import time
from io import StringIO
from inspect import getfullargspec

from config import BOT_USERNAME as bname
from driver.core import bot
from driver.queues import QUEUE
from driver.filters import command
from driver.database.dbchat import remove_served_chat
from driver.decorators import bot_creator, sudo_users_only, errors
from driver.utils import remove_if_exists

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@Client.on_message(command(["eval", f"eval{bname}"]) & ~filters.edited)
@sudo_users_only
async def executor(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="» ɢɪᴠᴇ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ ᴇxᴇᴄᴜᴛᴇ ɪᴛ ᴏɴ ᴛᴇʀᴍɪɴᴀʟ.")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "SUCCESS"
    final_output = f"`ᴏᴜᴛᴩᴜᴛ:`\n\n```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="😴", callback_data=f"ʀᴜɴᴛɪᴍᴇ {t2-t1} sᴇᴄᴏɴᴅs"
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"`ɪɴᴩᴜᴛ:`\n`{cmd[0:980]}`\n\n`ᴏᴜᴛᴩᴜᴛ:`\n`ᴀᴛᴛᴀᴄʜᴇᴅ ᴅᴏᴄᴜᴍᴇɴᴛ`",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        remove_if_exists(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="😴",
                        callback_data=f"ʀᴜɴᴛɪᴍᴇ {round(t2-t1, 3)} sᴇᴄᴏɴᴅs",
                    )
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


@Client.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@Client.on_message(command(["sh", f"sh{bname}"]) & ~filters.edited)
@sudo_users_only
async def shellrunner(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="**ᴜsᴀɢᴇ:**\n\n» /sh echo ʀʏᴛʜᴍx ᴋɪ ᴍᴋʙ")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await edit_or_reply(message, text=f"`ᴇʀʀᴏʀ:`\n\n```{err}```")
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"`ᴇʀʀᴏʀ:`\n\n```{''.join(errors)}```"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await bot.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`ᴏᴜᴛᴩᴜᴛ`",
            )
            return remove_if_exists("output.txt")
        await edit_or_reply(message, text=f"`ᴏᴜᴛᴩᴜᴛ:`\n\n```{output}```")
    else:
        await edit_or_reply(message, text="`ᴏᴜᴛᴩᴜᴛ:`\n\n`no output`")


@Client.on_message(command(["leavebot", f"leavebot{bname}"]) & ~filters.edited)
@bot_creator
async def bot_leave_group(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**ᴜsᴀɢᴇ:**\n\n» /leavebot -1001686672798"
        )
        return
    chat = message.text.split(None, 2)[1]
    if chat in QUEUE:
        await remove_active_chat(chat)
        return
    try:
        await bot.leave_chat(chat)
        await user.leave_chat(chat)
        await remove_served_chat(chat)
    except Exception as e:
        await message.reply_text(f"😩 ғᴀɪʟᴇᴅ\n\nʀᴇᴀsᴏɴ: `{e}`")
        return
    await message.reply_text(f"😎 ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴛʜɪs sʜɪᴛ :\n\n💭 » `{chat}`")
