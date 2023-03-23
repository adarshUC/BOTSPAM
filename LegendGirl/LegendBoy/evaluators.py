import asyncio
import os
import sys
from io import StringIO

from pyrogram import Client, filters
from pyrogram.types import Message

from LegendGirl.Config import *

from .. import sudos


@Client.on_message(filters.user(sudos) & filters.command(["eval"], prefixes=HANDLER))
async def eval(Legend: Client, message: Message):
    global code
    if message.reply_to_message:
        code = message.reply_to_message.text.markdown
    else:
        try:
            code = message.text.split(" ", maxsplit=1)[1]
            if not code:
                message.reply_text("Gib me code!")
                return
        except IndexError:
            try:
                code = message.text.split(" \n", maxsplit=1)[1]
                if not code:
                    message.reply_text("Gib me code!")
                    return
            except IndexError:
                pass
    result = sys.stdout = StringIO()
    lol = exec(message, code)
    try:
        await message.reply_text(
            f"<b>Code:</b>\n"
            f"<code>{code}</code>\n\n"
            f"<b>Result</b>:\n"
            f"<code>{lol}</code>"
        )
    except:
        await message.reply_text(
            f"<b>Code:</b>\n"
            f"<code>{code}</code>\n\n"
            f"<b>Result</b>:\n"
            f"<code>{lol}</code>"
        )


@Client.on_message(filters.user(sudos) & filters.command(["exec"], prefixes=HANDLER))
async def exec(Legend: Client, message: Message):
    global code
    if message.reply_to_message:
        cmd = message.reply_to_message.text.markdown
    else:
        try:
            cmd = message.text.split(" ", maxsplit=1)[1]
            if not cmd:
                message.reply_text("Gib me code!")
                return
        except IndexError:
            try:
                cmd = message.text.split(" \n", maxsplit=1)[1]
                if not cmd:
                    message.reply_text("Gib me code!")
                    return
            except IndexError:
                pass
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    uid = os.geteuid()
    if uid == 0:
        await message.reply_text(
            f"<b>Code:</b>\n"
            f"<code>{cmd}</code>\n\n"
            f"<b>Result</b>:\n"
            f"<code>{result}</code>"
        )
    else:
        await message.reply_text(
            f"<b>Code:</b>\n"
            f"<code>{cmd}</code>\n\n"
            f"<b>Result</b>:\n"
            f"<code>{result}</code>"
        )
