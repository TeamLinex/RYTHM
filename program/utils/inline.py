""" inline section button """

from config import GROUP_SUPPORT

from pyrogram.types import (
  InlineKeyboardButton,
  InlineKeyboardMarkup,
)


def stream_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="▷", callback_data=f'set_resume | {user_id}'),
      InlineKeyboardButton(text="II", callback_data=f'set_pause | {user_id}'),
      InlineKeyboardButton(text="‣‣I", callback_data=f'set_skip | {user_id}'),
      InlineKeyboardButton(text="▢", callback_data=f'set_stop | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="• sᴜᴩᴩᴏʀᴛ •", url=f"https://t.me/{GROUP_SUPPORT}"),
      InlineKeyboardButton(text="• ᴄʟᴏsᴇ •", callback_data=f'set_close'),
    ],
  ]
  return buttons


def menu_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="▢", callback_data=f'set_stop | {user_id}'),
      InlineKeyboardButton(text="II", callback_data=f'set_pause | {user_id}'),
      InlineKeyboardButton(text="▷", callback_data=f'set_resume | {user_id}'),
      InlineKeyboardButton(text="‣‣I", callback_data=f'set_skip | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data='stream_home_panel'),
    ]
  ]
  return buttons


close_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "🗑", callback_data="set_close"
      )
    ]
  ]
)


back_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "• ʙᴀᴄᴋ •", callback_data="stream_menu_panel"
      )
    ]
  ]
)
