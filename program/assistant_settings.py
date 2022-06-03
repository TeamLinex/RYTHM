import asyncio

from config import BOT_USERNAME, SUDO_USERS

from program import LOGS
from program.utils.function import get_calls

from driver.queues import QUEUE
from driver.core import user, me_bot
from driver.filters import command, other_filters
from driver.database.dbchat import remove_served_chat
from driver.database.dbqueue import remove_active_chat
from driver.decorators import authorized_users_only, bot_creator, check_blacklist

from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.raw.types import InputPeerChannel
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant, ChatAdminRequired


@Client.on_message(
    command(["userbotjoin", "join", " assistant", f"userbotjoin@{BOT_USERNAME}"]) & other_filters
)
@check_blacklist()
@authorized_users_only
async def join_chat(c: Client, m: Message):
    chat_id = m.chat.id
    try:
        invitelink = (await c.get_chat(chat_id)).invite_link
        if not invitelink:
            await c.export_chat_invite_link(chat_id)
            invitelink = (await c.get_chat(chat_id)).invite_link
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        await user.join_chat(invitelink)
        await remove_active_chat(chat_id)
        return await user.send_message(chat_id, "🙂 ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ.")
    except UserAlreadyParticipant:
        return await user.send_message(chat_id, "🙂 ɪ ᴀᴍ ᴀʟʀᴇᴀᴅʏ ʜᴇʀᴇ.")


@Client.on_message(
    command(["userbotleave", f"userbotleave@{BOT_USERNAME}"]) & other_filters
)
@check_blacklist()
@authorized_users_only
async def leave_chat(c :Client, m: Message):
    chat_id = m.chat.id
    try:
        if chat_id in QUEUE:
            await remove_active_chat(chat_id)
            await user.leave_chat(chat_id)
            return await c.send_message(chat_id, "» ᴀssɪsᴛᴀɴᴛ ʟᴇғᴛ ᴛʜᴇ ᴄʜᴀᴛ.")
        else:
            await user.leave_chat(chat_id)
            return await c.send_message(chat_id, "» ᴀssɪsᴛᴀɴᴛ ʟᴇғᴛ ᴛʜᴇ ᴄʜᴀᴛ.")
    except UserNotParticipant:
        return await c.send_message(chat_id, "» ᴀssɪsᴛᴀɴᴛ ʟᴇғᴛ ᴛʜᴇ ᴄʜᴀᴛ ғᴇᴡ ʏᴇᴀʀs ᴀɢᴏ.")


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]) & ~filters.edited)
@bot_creator
async def leave_all(c: Client, message: Message):
    if message.from_user.id not in SUDO_USERS:
        return
    run_1 = 0
    run_2 = 0
    msg = await message.reply("» ᴀssɪsᴛᴀɴᴛ ɪs ᴛʀʏɪɴɢ ᴛᴏ ʟᴇᴀᴠᴇ ᴀʟʟ ᴄʜᴀᴛs.")
    async for dialog in user.iter_dialogs():
        try:
            await user.leave_chat(dialog.chat.id)
            await remove_active_chat(dialog.chat.id)
            run_1 += 1
            await msg.edit(
                f"ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠɪɴɢ ᴄʜᴀᴛs...\n\nsᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ: {run_1} ᴄʜᴀᴛs.\nғᴀɪʟᴇᴅ ᴛᴏ ʟᴇᴀᴠᴇ ɪɴ: {run_2} ᴄʜᴀᴛs."
            )
        except Exception:
            run_2 += 1
            await msg.edit(
                f"ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠɪɴɢ ᴄʜᴀᴛs...\n\nsᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ: {run_1} ᴄʜᴀᴛs.\nғᴀɪʟᴇᴅ ᴛᴏ ʟᴇᴀᴠᴇ ɪɴ: {run_2} ᴄʜᴀᴛs."
            )
        await asyncio.sleep(0.5)
    await msg.delete()
    await client.send_message(
        message.chat.id, f"» sᴜᴄᴄᴇssғᴜʟʏ ʟᴇғᴛ: {run_2} ᴄʜᴀᴛs.\n😫 ғᴀɪʟᴇᴅ ᴛᴏ ʟᴇᴀᴠᴇ: {run_2} ᴄʜᴀᴛs."
    )


@Client.on_message(command(["startvc", f"startvc@{BOT_USERNAME}"]) & other_filters)
@check_blacklist()
@authorized_users_only
async def start_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    msg = await c.send_message(chat_id, "`ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ ᴠᴏɪᴄᴇᴄʜᴀᴛ ʙᴀʙʏ...`")
    try:
        peer = await user.resolve_peer(chat_id)
        await user.send(
            CreateGroupCall(
                peer=InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash,
                ),
                random_id=user.rnd_id() // 9000000000,
            )
        )
        await msg.edit_text("» ᴠᴏɪᴄᴇᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ ʙᴀʙʏ !")
    except ChatAdminRequired:
        await msg.edit_text(
            "ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ɪs ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ᴄʜᴀᴛ ᴡɪᴛʜ:\n\n» ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs ᴩᴇʀᴍɪssɪᴏɴ"
        )


@Client.on_message(filters.left_chat_member)
async def bot_kicked(c: Client, m: Message):
    bot_id = me_bot.id
    chat_id = m.chat.id
    left_member = m.left_chat_member
    if left_member.id == bot_id:
        if chat_id in QUEUE:
            await remove_active_chat(chat_id)
            return
        try:
            await user.leave_chat(chat_id)
            await remove_served_chat(chat_id)
        except Exception as e:
            LOGS.info(e)
