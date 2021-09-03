#MIT License

#Copyright (c) 2021 SUBIN

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from pyrogram import Client, emoji
from utils import mp, playlist
from config import Config


HELP = """

<b>
Gunakan /play <nama lagu> atau gunakan /play sebagai balasan file audio atau tautan youtube.

Gunakan /yplay untuk memutar semua lagu dari playlist youtube.

Anda juga dapat menggunakan <code>/splay song name</code> untuk memutar lagu dari Jio Saavn atau <code>/splay -a album name</code> untuk memutar semua lagu dari album jiosaavn atau /cplay <channel nama pengguna atau id saluran> untuk memutar musik dari saluran telegram.</b>

**Perintah User**:

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
**/keluar** Tinggalkan obrolan suara saat ini
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



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    admins = await mp.get_admins(Config.CHAT)
    if query.from_user.id not in admins and query.data != "help":
        await query.answer(
            "😒 Played Joji.mp3",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Empty Playlist"
        else:
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(
                    f"{pl}",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏯", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Paused\n\n{pl},",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="resume"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass
    
    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Resumed\n\n{pl}",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Listing first 25 songs of total {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Skipped\n\n{pl}",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass

    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton('⚙️ Update Channel', url='https://t.me/subin_works'),
                InlineKeyboardButton('🧩 Source', url='https://github.com/subinps/MusicPlayer'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        try:
            await query.edit_message_text(
                HELP,
                reply_markup=reply_markup

            )
        except MessageNotModified:
            pass

