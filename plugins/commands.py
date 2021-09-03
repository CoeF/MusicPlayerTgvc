
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from utils import USERNAME, mp
from config import Config
U=USERNAME
CHAT=Config.CHAT
msg=Config.msg
HOME_TEXT = "<b>Helo, [{}](tg://user?id={})\n\nIam MusicPlayer 2.0 which plays music in Channels and Groups 24*7.\n\nI can even Stream Youtube Live in Your Voicechat.\n\nDeploy Your Own bot from source code below.\n\nHit /help to know about available commands.</b>"
HELP = """

<b>
Gunakan /play <nama lagu> atau gunakan /play sebagai balasan file audio atau tautan link youtube.

Gunakan /yplay untuk memutar semua lagu dari playlist youtube.

Anda juga dapat menggunakan <code>/splay song name</code> untuk memutar lagu dari Jio Saavn atau <code>/splay -a album name</code> untuk memutar semua lagu dari album jiosaavn atau /cplay <channel nama pengguna atau id saluran> untuk memutar musik dari saluran telegram.</b>

**Perintah Umum**:

**/play** Balas file audio atau tautan YouTube untuk memutarnya atau menggunakan /play <nama lagu>.
**/splay** Putar musik dari Jio Saavn, Gunakan /splay <song name> atau <code>/splay -a album name</code> untuk memutar semua lagu dari album tersebut.
**/player** Menampilkan lagu yang sedang diputar.
**/upload** Mengupload lagu yang sedang diputar sebagai file audio.
**/help** Tampilkan bantuan untuk perintah
**/playlist** Menampilkan daftar putar.

**Perintah Admin**:
**/skip** [n] ... Lewati saat ini atau n di mana n >= 2.
**/cplay** Putar musik dari file musik saluran.
**/yplay** Putar musik dari playlist youtube.
**/join** Bergabung dengan obrolan suara.
**/leave** Tinggalkan obrolan suara saat ini
**/shuffle** Daftar Putar Acak.
**/vc** Periksa VC mana yang bergabung.
**/stop** Berhenti bermain.
**/radio** Mulai Radio.
**/stopradio** Menghentikan Radio Stream.
**/clearplaylist** Hapus daftar putar.
**/ekspor** Ekspor daftar putar saat ini untuk penggunaan di masa mendatang.
**/import** Impor daftar putar yang telah diekspor sebelumnya.
**/replay** Mainkan dari awal.
**/clean** Hapus file RAW PCM yang tidak digunakan.
**/jeda** Jeda pemutaran.
**/resume** Lanjutkan pemutaran.
**/volume** Ubah volume (0-200).
**/mute** Bisukan di VC.
**/unmute** Suarakan di VC.
**/restart** Perbarui dan mulai ulang Bot.
"""




@Client.on_message(filters.command(['start', f'start@{U}']))
async def start(client, message):
    buttons = [
        [
        InlineKeyboardButton('🔱 Update Channel', url='https://t.me/ChannelTrident'),
        # InlineKeyboardButton('🧩 Source', url='https://github.com/subinps/MusicPlayer'),
    ],
    [
        InlineKeyboardButton('👨🏼‍🦯 Help', callback_data='help'),
        
    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)



@Client.on_message(filters.command(["help", f"help@{U}"]))
async def show_help(client, message):
    buttons = [
        [
        InlineKeyboardButton('⚙️ Update Channel', url='https://t.me/ChannelTrident'),
        # InlineKeyboardButton('🧩 Source', url='https://github.com/subinps/MusicPlayer'),
    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_text(
        HELP,
        reply_markup=reply_markup
        )
    await mp.delete(message)
