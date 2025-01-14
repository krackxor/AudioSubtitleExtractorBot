#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex

import time
import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helpers.download_from_url import get_size
from helpers.tools import clean_up
from helpers.progress import progress_func

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def upload_audio(client, message, file_loc):

    msg = await message.edit_text(text="**Mengunggah aliran yang diekstrak...**",
                                  reply_markup=InlineKeyboardMarkup([[
                                      InlineKeyboardButton(
                                          text="Progres",
                                          callback_data="progress_msg")
                                  ]]))

    title = None
    artist = None
    thumb = None
    duration = 0

    metadata = extractMetadata(createParser(file_loc))
    if metadata and metadata.has("title"):
        title = metadata.get("title")
    if metadata and metadata.has("artist"):
        artist = metadata.get("artist")
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds

    fn = os.path.basename(file_loc)
    ex = os.path.splitext(fn)[1]
    fn = os.path.splitext(fn)[0]
    fn = os.path.splitext(fn)[0]
    if ex == ".aac" or ex == ".mp3":
        fn = fn + ex
    else:
        fn = fn + ".mka"
    size = os.path.getsize(file_loc)
    size = get_size(size)

    c_time = time.time()
    try:
        await client.send_audio(
            chat_id=message.chat.id,
            audio=file_loc,
            file_name=str(fn),
            thumb=thumb,
            caption=f"`{fn}` [{size}]\n\n<b>Creative by </b>TelMovID",
            title=title,
            performer=artist,
            duration=duration,
            progress=progress_func,
            progress_args=("**Mengunggah aliran yang diekstrak...**", msg, c_time))
    except Exception as e:
        print(e)
        await msg.edit_text("**Terjadi Kesalahan. Lihat Log untuk Informasi Lebih Lanjut.**")
        return

    await msg.delete()
    await clean_up(file_loc)


async def upload_subtitle(client, message, file_loc):

    msg = await message.edit_text(text="**Mengunggah subtitle...**",
                                  reply_markup=InlineKeyboardMarkup([[
                                      InlineKeyboardButton(
                                          text="Progres",
                                          callback_data="progress_msg")
                                  ]]))

    c_time = time.time()

    try:
        await client.send_document(
            chat_id=message.chat.id,
            document=file_loc,
            caption="<b>Creative by </b>TelMovID",
            progress=progress_func,
            progress_args=("**Mengunggah teks subtitle yang diekstrak...**", msg, c_time))
    except Exception as e:
        print(e)
        await msg.edit_text("**Terjadi Kesalahan. Lihat Log untuk Informasi Lebih Lanjut.**")
        return

    await msg.delete()
    await clean_up(file_loc)
