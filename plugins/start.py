#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex

from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script


@trojanz.on_message(filters.command(["start"]) & filters.private)
async def start(client, message):
    await message.reply_text(
        text=Script.START_MSG.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("💡 𝐁𝐚𝐧𝐭𝐮𝐚𝐧", callback_data="help_data"),
            InlineKeyboardButton("𝐓𝐞𝐧𝐭𝐚𝐧𝐠 🤖", callback_data="about_data"),
        ]]),
        reply_to_message_id=message.id)


@trojanz.on_message(filters.command(["help"]) & filters.private)
async def help(client, message):
    await message.reply_text(
        text=Script.HELP_MSG,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("≪ 𝕂𝕖𝕞𝕓𝕒𝕝𝕚", callback_data="start_data"),
            InlineKeyboardButton("𝐓𝐞𝐧𝐭𝐚𝐧𝐠 🤖", callback_data="about_data"),
        ]]),
        reply_to_message_id=message.id)


@trojanz.on_message(filters.command(["about"]) & filters.private)
async def about(client, message):
    await message.reply_text(
        text=Script.ABOUT_MSG,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("≪ 𝕂𝕖𝕞𝕓𝕒𝕝𝕚", callback_data="help_data"),
            InlineKeyboardButton("𝕊𝕥𝕒𝕣𝕥", callback_data="start_data"),
        ]]),
        reply_to_message_id=message.id)
