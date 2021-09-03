
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME
from config import Config
from config import STREAM
CHAT=Config.CHAT
ADMINS=Config.ADMINS

async def is_admin(_, client, message: Message):
    admins = await mp.get_admins(CHAT)
    if message.from_user is None and message.sender_chat:
        return True
    if message.from_user.id in admins:
        return True
    else:
        return False

admin_filter=filters.create(is_admin)   


@Client.on_message(filters.command(["radio", f"radio@{USERNAME}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def radio(client, message: Message):
    if Config.CPLAY:
        if 3 in RADIO:
            k=await message.reply_text("Tampaknya pemutaran saluran diaktifkan dan daftar putar tidak kosong.\nGunakan /clearplaylist untuk mengosongkan daftar putar.")
            await mp.delete(k)
            await mp.delete(message)
            return
        else:
            await mp.start_radio()
            k=await message.reply_text(f"Pemutaran Saluran dari <code>{STREAM}</code> dimulai.")
            await mp.delete(k)
            await mp.delete(message)
            return
    if 1 in RADIO:
        k=await message.reply_text("Mohon hentikan Radio Stream /stopradio yang ada")
        await mp.delete(k)
        await mp.delete(message)
        return
    await mp.start_radio()
    k=await message.reply_text(f"Memulai Radio: <code>{STREAM}</code>")
    await mp.delete(k)
    await mp.delete(message)

@Client.on_message(filters.command(['stopradio', f"stopradio@{USERNAME}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def stop(_, message: Message):
    if Config.CPLAY:
        if 3 not in RADIO:
            k=await message.reply_text("Tampaknya pemutaran saluran diaktifkan dan daftar putar kosong.\nGunakan /radio untuk memulai ulang pemutaran.")
            await mp.delete(k)
            await mp.delete(message)
            return
        else:
            k=await message.reply_text("Sepertinya pemutaran saluran diaktifkan.\nGunakan /clearplaylist putar untuk menghapus daftar putar.")
            await mp.delete(k)
            await mp.delete(message)
            return 
    if 0 in RADIO:
        k=await message.reply_text("Silakan mulai Radio First /radio")
        await mp.delete(k)
        await mp.delete(message)
        return
    await mp.stop_radio()
    k=await message.reply_text("Streaming radio berakhir.")
    await mp.delete(k)
    await mp.delete(message)
