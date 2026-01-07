import asyncio
import os
from datetime import datetime, timedelta
from typing import Union
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls import filters as pytgfilters
from pytgcalls import types as pytypes
from pytgcalls.exceptions import NoActiveGroupCall
from ntgcalls import ConnectionNotFound, TelegramServerError

import config
from AnonXMusic import LOGGER, YouTube, app
from AnonXMusic.misc import db
from AnonXMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from AnonXMusic.utils.exceptions import AssistantErr
from AnonXMusic.utils.formatters import check_duration, seconds_to_min, speed_converter
from AnonXMusic.utils.inline.play import stream_markup
from AnonXMusic.utils.stream.autoclear import auto_clean
from AnonXMusic.utils.thumbnails import get_thumb
from strings import get_string

autoend = {}
counter = {}


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="AnonXAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        ) if config.STRING1 else None
        self.one = PyTgCalls(
            self.userbot1,
            cache_duration=100,
        ) if self.userbot1 else None
        
        self.userbot2 = Client(
            name="AnonXAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        ) if config.STRING2 else None
        self.two = PyTgCalls(
            self.userbot2,
            cache_duration=100,
        ) if self.userbot2 else None
        
        self.userbot3 = Client(
            name="AnonXAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        ) if config.STRING3 else None
        self.three = PyTgCalls(
            self.userbot3,
            cache_duration=100,
        ) if self.userbot3 else None
        
        self.userbot4 = Client(
            name="AnonXAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        ) if config.STRING4 else None
        self.four = PyTgCalls(
            self.userbot4,
            cache_duration=100,
        ) if self.userbot4 else None
        
        self.userbot5 = Client(
            name="AnonXAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        ) if config.STRING5 else None
        self.five = PyTgCalls(
            self.userbot5,
            cache_duration=100,
        ) if self.userbot5 else None

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_call(chat_id)
        except:
            pass

    async def stop_stream_force(self, chat_id: int):
        try:
            if config.STRING1:
                await self.one.leave_call(chat_id)
        except:
            pass
        try:
            if config.STRING2:
                await self.two.leave_call(chat_id)
        except:
            pass
        try:
            if config.STRING3:
                await self.three.leave_call(chat_id)
        except:
            pass
        try:
            if config.STRING4:
                await self.four.leave_call(chat_id)
        except:
            pass
        try:
            if config.STRING5:
                await self.five.leave_call(chat_id)
        except:
            pass
        try:
            await _clear_(chat_id)
        except:
            pass

    async def speedup_stream(self, chat_id: int, file_path, speed, playing):
        assistant = await group_assistant(self, chat_id)
        if str(speed) != str("1.0"):
            base = os.path.basename(file_path)
            chatdir = os.path.join(os.getcwd(), "playback", str(speed))
            if not os.path.isdir(chatdir):
                os.makedirs(chatdir)
            out = os.path.join(chatdir, base)
            if not os.path.isfile(out):
                if str(speed) == str("0.5"):
                    vs = 2.0
                if str(speed) == str("0.75"):
                    vs = 1.35
                if str(speed) == str("1.5"):
                    vs = 0.68
                if str(speed) == str("2.0"):
                    vs = 0.5
                proc = await asyncio.create_subprocess_shell(
                    cmd=(
                        "ffmpeg "
                        "-i "
                        f"{file_path} "
                        "-filter:v "
                        f"setpts={vs}*PTS "
                        "-filter:a "
                        f"atempo={speed} "
                        f"{out}"
                    ),
                    stdin=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await proc.communicate()
            else:
                pass
        else:
            out = file_path
        dur = await asyncio.get_event_loop().run_in_executor(None, check_duration, out)
        dur = int(dur)
        played, con_seconds = speed_converter(playing[0]["played"], speed)
        duration = seconds_to_min(dur)
        stream = (
            pytypes.MediaStream(
                out,
                audio_parameters=pytypes.AudioQuality.HIGH,
                video_parameters=pytypes.VideoQuality.HD_720p,
                ffmpeg_parameters=f"-ss {played} -to {duration}",
            )
            if playing[0]["streamtype"] == "video"
            else pytypes.MediaStream(
                out,
                audio_parameters=pytypes.AudioQuality.HIGH,
                video_flags=pytypes.MediaStream.Flags.IGNORE,
                ffmpeg_parameters=f"-ss {played} -to {duration}",
            )
        )
        if str(db[chat_id][0]["file"]) == str(file_path):
            await assistant.play(chat_id, stream)
        else:
            raise AssistantErr("Umm")
        if str(db[chat_id][0]["file"]) == str(file_path):
            exis = (playing[0]).get("old_dur")
            if not exis:
                db[chat_id][0]["old_dur"] = db[chat_id][0]["dur"]
                db[chat_id][0]["old_second"] = db[chat_id][0]["seconds"]
            db[chat_id][0]["played"] = con_seconds
            db[chat_id][0]["dur"] = duration
            db[chat_id][0]["seconds"] = dur
            db[chat_id][0]["speed_path"] = out
            db[chat_id][0]["speed"] = speed

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_call(chat_id)
        except:
            pass

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        if video:
            stream = pytypes.MediaStream(
                link,
                audio_parameters=pytypes.AudioQuality.HIGH,
                video_parameters=pytypes.VideoQuality.HD_720p,
            )
        else:
            stream = pytypes.MediaStream(
                link,
                audio_parameters=pytypes.AudioQuality.HIGH,
                video_flags=pytypes.MediaStream.Flags.IGNORE,
            )
        await assistant.play(
            chat_id,
            stream,
        )

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        stream = (
            pytypes.MediaStream(
                file_path,
                audio_parameters=pytypes.AudioQuality.HIGH,
                video_parameters=pytypes.VideoQuality.HD_720p,
                ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
            if mode == "video"
            else pytypes.MediaStream(
                file_path,
                audio_parameters=pytypes.AudioQuality.HIGH,
                video_flags=pytypes.MediaStream.Flags.IGNORE,
                ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
        )
        await assistant.play(chat_id, stream)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOGGER_ID)
        await assistant.play(
            config.LOGGER_ID,
            pytypes.MediaStream(link),
        )
        await asyncio.sleep(0.2)
        await assistant.leave_call(config.LOGGER_ID)

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)
        if video:
            stream = pytypes.MediaStream(
                link,
                audio_parameters=pytypes.AudioQuality.HIGH,
                video_parameters=pytypes.VideoQuality.HD_720p,
            )
        else:
            stream = (
                pytypes.MediaStream(
                    link,
                    audio_parameters=pytypes.AudioQuality.HIGH,
                    video_parameters=pytypes.VideoQuality.HD_720p,
                )
                if video
                else pytypes.MediaStream(
                    link,
                    audio_parameters=pytypes.AudioQuality.HIGH,
                    video_flags=pytypes.MediaStream.Flags.IGNORE,
                )
            )
        try:
            await assistant.play(
                chat_id,
                stream,
            )
        except NoActiveGroupCall:
            raise AssistantErr(_["call_8"])
        except ConnectionNotFound:
            raise AssistantErr(_["call_9"])
        except Exception as e:
            raise AssistantErr(f"Error: {str(e)}")
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.calls)
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            await auto_clean(popped)
            if not check:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
        except:
            try:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
            except:
                return
        else:
            queued = check[0]["file"]
            language = await get_lang(chat_id)
            _ = get_string(language)
            title = (check[0]["title"]).title()
            user = check[0]["by"]
            original_chat_id = check[0]["chat_id"]
            streamtype = check[0]["streamtype"]
            videoid = check[0]["vidid"]
            db[chat_id][0]["played"] = 0
            exis = (check[0]).get("old_dur")
            if exis:
                db[chat_id][0]["dur"] = exis
                db[chat_id][0]["seconds"] = check[0]["old_second"]
                db[chat_id][0]["speed_path"] = None
                db[chat_id][0]["speed"] = 1.0
            video = True if str(streamtype) == "video" else False
            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)
                if n == 0:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                if video:
                    stream = pytypes.MediaStream(
                        link,
                        audio_parameters=pytypes.AudioQuality.HIGH,
                        video_parameters=pytypes.VideoQuality.HD_720p,
                    )
                else:
                    stream = pytypes.MediaStream(
                        link,
                        audio_parameters=pytypes.AudioQuality.HIGH,
                        video_flags=pytypes.MediaStream.Flags.IGNORE,
                    )
                try:
                    await client.play(chat_id, stream)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                img = await get_thumb(videoid)
                button = stream_markup(_, chat_id)
                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif "vid_" in queued:
                mystic = await app.send_message(original_chat_id, _["call_7"])
                try:
                    file_path, direct = await YouTube.download(
                        videoid,
                        mystic,
                        videoid=True,
                        video=True if str(streamtype) == "video" else False,
                    )
                except:
                    return await mystic.edit_text(
                        _["call_6"], disable_web_page_preview=True
                    )
                if video:
                    stream = pytypes.MediaStream(
                        file_path,
                        audio_parameters=pytypes.AudioQuality.HIGH,
                        video_parameters=pytypes.VideoQuality.HD_720p,
                    )
                else:
                    stream = pytypes.MediaStream(
                        file_path,
                        audio_parameters=pytypes.AudioQuality.HIGH,
                        video_flags=pytypes.MediaStream.Flags.IGNORE,
                    )
                try:
                    await client.play(chat_id, stream)
                except:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                img = await get_thumb(videoid)
                button = stream_markup(_, chat_id)
                await mystic.delete()
                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            elif "index_" in queued:
                stream = (
                    pytypes.MediaStream(
                        videoid,
                        audio_parameters=pytypes.AudioQuality.HIGH,
                        video_parameters=pytypes.VideoQuality.HD_720p,
                    )
                    if str(streamtype) == "video"
                    else pytypes.MediaStream(
                        videoid,
                        audio_parameters=pytypes.AudioQuality.HIGH,
                        video_flags=pytypes.MediaStream.Flags.IGNORE,
                    )
                )
                try:
                    await client.play(chat_id, stream)
                except:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                button = stream_markup(_, chat_id)
                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=config.STREAM_IMG_URL,
                    caption=_["stream_2"].format(user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                if video:
                    stream = pytypes.MediaStream(
                        queued,
                        audio_parameters=pytypes.AudioQuality.HIGH,
                        video_parameters=pytypes.VideoQuality.HD_720p,
                    )
                else:
                    stream = pytypes.MediaStream(
                        queued,
                        audio_parameters=pytypes.AudioQuality.HIGH,
                        video_flags=pytypes.MediaStream.Flags.IGNORE,
                    )
                try:
                    await client.play(chat_id, stream)
                except:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                if videoid == "telegram":
                    button = stream_markup(_, chat_id)
                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=config.TELEGRAM_AUDIO_URL
                        if str(streamtype) == "audio"
                        else config.TELEGRAM_VIDEO_URL,
                        caption=_["stream_1"].format(
                            config.SUPPORT_CHAT, title[:23], check[0]["dur"], user
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                elif videoid == "soundcloud":
                    button = stream_markup(_, chat_id)
                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=config.SOUNCLOUD_IMG_URL,
                        caption=_["stream_1"].format(
                            config.SUPPORT_CHAT, title[:23], check[0]["dur"], user
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                else:
                    img = await get_thumb(videoid)
                    button = stream_markup(_, chat_id)
                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=img,
                        caption=_["stream_1"].format(
                            f"https://t.me/{app.username}?start=info_{videoid}",
                            title[:23],
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        pings = []
        if self.one:
            pings.append(self.one.ping)
        if self.two:
            pings.append(self.two.ping)
        if self.three:
            pings.append(self.three.ping)
        if self.four:
            pings.append(self.four.ping)
        if self.five:
            pings.append(self.five.ping)
        return str(round(sum(pings) / len(pings), 3)) if pings else "0"

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client...\n")
        from AnonXMusic.core.userbot import assistants, assistantids
        
        if self.one:
            await self.one.start()
            assistants.append(1)
            self.userbot1.id = self.userbot1.me.id
            self.userbot1.name = self.userbot1.me.mention
            self.userbot1.username = self.userbot1.me.username
            assistantids.append(self.userbot1.id)
            LOGGER(__name__).info(f"Assistant 1 Started as {self.userbot1.name}")
            try:
                await self.userbot1.join_chat("Exampurrs")
            except:
                pass
        
        if self.two:
            await self.two.start()
            assistants.append(2)
            self.userbot2.id = self.userbot2.me.id
            self.userbot2.name = self.userbot2.me.mention
            self.userbot2.username = self.userbot2.me.username
            assistantids.append(self.userbot2.id)
            LOGGER(__name__).info(f"Assistant 2 Started as {self.userbot2.name}")
        
        if self.three:
            await self.three.start()
            assistants.append(3)
            self.userbot3.id = self.userbot3.me.id
            self.userbot3.name = self.userbot3.me.mention
            self.userbot3.username = self.userbot3.me.username
            assistantids.append(self.userbot3.id)
            LOGGER(__name__).info(f"Assistant 3 Started as {self.userbot3.name}")
        
        if self.four:
            await self.four.start()
            assistants.append(4)
            self.userbot4.id = self.userbot4.me.id
            self.userbot4.name = self.userbot4.me.mention
            self.userbot4.username = self.userbot4.me.username
            assistantids.append(self.userbot4.id)
            LOGGER(__name__).info(f"Assistant 4 Started as {self.userbot4.name}")
        
        if self.five:
            await self.five.start()
            assistants.append(5)
            self.userbot5.id = self.userbot5.me.id
            self.userbot5.name = self.userbot5.me.mention
            self.userbot5.username = self.userbot5.me.username
            assistantids.append(self.userbot5.id)
            LOGGER(__name__).info(f"Assistant 5 Started as {self.userbot5.name}")

    async def decorators(self):
        # Register handlers only for active assistants
        active_clients = [c for c in [self.one, self.two, self.three, self.four, self.five] if c]
        
        for client in active_clients:
            @client.on_update(pytgfilters.chat_update(pytypes.ChatUpdate.Status.KICKED | pytypes.ChatUpdate.Status.LEFT_GROUP))
            async def stream_services_handler(_, update: pytypes.ChatUpdate):
                await self.stop_stream(update.chat_id)

            @client.on_update(pytgfilters.stream_end())
            async def stream_end_handler1(client, update: pytypes.StreamEnded):
                if update.stream_type != pytypes.StreamEnded.Type.AUDIO:
                    return
                await self.change_stream(client, update.chat_id)


Anony = Call()
