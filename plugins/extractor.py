#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex

from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script


@trojanz.on_message(filters.private & (filters.document | filters.video))
async def confirm_dwnld(client, message):
    media = message
    filetype = media.document or media.video

    if filetype.mime_type.startswith("video/"):
        await message.reply_text(
            "**𝘼𝙥𝙖𝙠𝙖𝙝 𝙖𝙙𝙖 𝙮𝙖𝙣𝙜 𝙗𝙞𝙨𝙖 𝙨𝙖𝙮𝙖 𝙗𝙖𝙣𝙩𝙪?**",
            quote=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="𝐔𝐧𝐝𝐮𝐡 𝐝𝐚𝐧 𝐏𝐫𝐨𝐬𝐞𝐬",
                                     callback_data="download_file")
            ], [InlineKeyboardButton(text="𝔹𝕒𝕥𝕒𝕝", callback_data="close")]]))
    else:
        await message.reply_text("Invalid Media", quote=True)


@trojanz.on_message(filters.private & filters.incoming & filters.text &
                    (filters.regex('^(ht|f)tp*')))
async def link_dwnld(client, message):
    if not message.media:
        #link = message.text
        await message.reply_text(
            "**𝘼𝙥𝙖𝙠𝙖𝙝 𝙖𝙙𝙖 𝙮𝙖𝙣𝙜 𝙗𝙞𝙨𝙖 𝙨𝙖𝙮𝙖 𝙗𝙖𝙣𝙩𝙪?**",
            quote=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="𝐔𝐧𝐝𝐮𝐡 𝐝𝐚𝐫𝐢 𝐓𝐚𝐮𝐭𝐚𝐧",
                                     callback_data="download_url")
            ], [InlineKeyboardButton(text="𝔹𝕒𝕥𝕒𝕝", callback_data="close")]]))
