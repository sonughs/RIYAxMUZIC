import os
import re
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from AnonXMusic import app
from config import OWNER_ID

# ⚠️ SECURITY: eval/sh commands have been DISABLED for security reasons.
# These commands allowed arbitrary code/shell execution which is a critical vulnerability.
# If you need these features, implement proper sandboxing and audit logging first.

async def aexec(code, client, message):
    """Disabled for security reasons."""
    pass


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


# DISABLED: Arbitrary code execution vulnerability
# @app.on_edited_message(...)
# @app.on_message(...)
# async def executor(...): ...

@app.on_message(
    filters.command("eval")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor_disabled(client, message: Message):
    """Eval command disabled for security."""
    await edit_or_reply(
        message, 
        text="<b>⚠️ /eval command has been DISABLED for security reasons.</b>\n\n"
             "This command allowed arbitrary Python code execution which is a critical vulnerability."
    )


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "» ɪᴛ'ʟʟ ʙᴇ ʙᴇᴛᴛᴇʀ ɪғ ʏᴏᴜ sᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛs ʙᴀʙʏ.", show_alert=True
            )
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


# DISABLED: Shell command injection vulnerability
# @app.on_edited_message(...)
# @app.on_message(...)
# async def shellrunner(...): ...

@app.on_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def shellrunner_disabled(_, message: Message):
    """Shell command disabled for security."""
    await edit_or_reply(
        message,
        text="<b>⚠️ /sh command has been DISABLED for security reasons.</b>\n\n"
             "This command allowed arbitrary shell execution which is a critical vulnerability."
    )
