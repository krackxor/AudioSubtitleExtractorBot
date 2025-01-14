#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex

import time
import json
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.progress import progress_func
from helpers.tools import execute, clean_up
from helpers.download_from_url import download_link

DATA = {}


async def download_file(client, message):
    media = message.reply_to_message
    if media.empty:
        await message.reply_text('𝑴𝒆𝒏𝒈𝒂𝒑𝒂 𝒌𝒂𝒎𝒖 𝒎𝒆𝒏𝒈𝒉𝒂𝒑𝒖𝒔 𝒊𝒕𝒖?', True)
        return

    msg = await client.send_message(
        chat_id=message.chat.id,
        text="**Mengunduh berkas Anda ke server....**",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="Periksa Progres",
                                 callback_data="progress_msg")
        ]]),
        reply_to_message_id=media.id)
    filetype = media.document or media.video

    c_time = time.time()

    download_location = await client.download_media(
        message=media,
        progress=progress_func,
        progress_args=("**Mengunduh berkas Anda ke server...**", msg, c_time))

    await msg.edit_text("Sedang memproses berkas Anda...")

    output = await execute(
        f"ffprobe -hide_banner -show_streams -print_format json '{download_location}'"
    )

    if not output:
        await clean_up(download_location)
        await msg.edit_text("Terjadi kesalahan saat mengambil detail....")
        return

    details = json.loads(output[0])
    buttons = []
    DATA[f"{message.chat.id}-{msg.id}"] = {}
    for stream in details["streams"]:
        mapping = stream["index"]
        stream_name = stream["codec_name"]
        stream_type = stream["codec_type"]
        codec_long_name = stream['codec_long_name']
        if stream_type in ("audio", "subtitle"):
            pass
        else:
            continue
        try:
            lang = stream["tags"]["language"]
        except:
            lang = mapping

        DATA[f"{message.chat.id}-{msg.id}"][int(mapping)] = {
            "map": mapping,
            "name": stream_name,
            "type": stream_type,
            "lang": lang,
            "location": download_location
        }
        buttons.append([
            InlineKeyboardButton(
                f"{stream_type.upper()} - {str(lang).upper()} [{codec_long_name}]",
                f"{stream_type}_{mapping}_{message.chat.id}-{msg.id}")
        ])

    buttons.append([
        InlineKeyboardButton("𝔹𝕒𝕥𝕒𝕝",
                             f"cancel_{mapping}_{message.chat.id}-{msg.id}")
    ])

    await msg.edit_text("**Pilih aliran yang akan diekstrak...**",
                        reply_markup=InlineKeyboardMarkup(buttons))


async def download_url_link(client, message):

    m = message.reply_to_message
    link = m.text

    if '|' in link:
        link, filename = link.split('|')
        link = link.strip()
        filename = filename.strip()
        dl_path = os.path.join(f'./{filename}')
    else:
        link = link.strip()
        filename = os.path.basename(link)
        dl_path = os.path.join("./", os.path.basename(link))

    msg = await client.send_message(
        chat_id=m.chat.id,
        text="**Mengunduh tautan Anda ke Server...**",
        reply_to_message_id=m.id)

    start = time.time()
    try:
        download_location = await download_link(link, dl_path, msg, start,
                                                client)
    except Exception as e:
        print(e)
        await msg.edit(f"**Pengunduhan Gagal** :\n\n{e}")
        await clean_up(download_location)
        return

    output = await execute(
        f"ffprobe -hide_banner -show_streams -print_format json '{download_location}'"
    )

    if not output:
        await clean_up(download_location)
        await msg.edit_text("Terjadi Kesalahan saat Mengambil Detail...")
        return

    details = json.loads(output[0])
    buttons = []
    DATA[f"{m.chat.id}-{msg.id}"] = {}
    for stream in details["streams"]:
        mapping = stream["index"]
        stream_name = stream["codec_name"]
        stream_type = stream["codec_type"]
        codec_long_name = stream['codec_long_name']
        if stream_type in ("audio", "subtitle"):
            pass
        else:
            continue
        try:
            lang = stream["tags"]["language"]
        except:
            lang = mapping

        DATA[f"{m.chat.id}-{msg.id}"][int(mapping)] = {
            "map": mapping,
            "name": stream_name,
            "type": stream_type,
            "lang": lang,
            "location": download_location
        }
        buttons.append([
            InlineKeyboardButton(
                f"{stream_type.upper()} - {str(lang).upper()} [{codec_long_name}]",
                f"{stream_type}_{mapping}_{m.chat.id}-{msg.id}")
        ])

    buttons.append([
        InlineKeyboardButton("𝔹𝕒𝕥𝕒𝕝",
                             f"cancel_{mapping}_{m.chat.id}-{msg.id}")
    ])

    await msg.edit_text("**Pilih Aliran yang Akan Diekstrak...**",
                        reply_markup=InlineKeyboardMarkup(buttons))
