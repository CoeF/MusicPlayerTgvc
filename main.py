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
try:
    import asyncio
    from pyrogram import Client, idle, filters
    import os
    from config import Config
    from utils import mp, USERNAME, FFMPEG_PROCESSES
    from pyrogram.raw import functions, types
    import os
    import sys
    from time import sleep
    from threading import Thread
    from signal import SIGINT
    import subprocess
    
except ModuleNotFoundError:
    import os
    import sys
    import subprocess
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)


CHAT=Config.CHAT
bot = Client(
    "Musicplayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
async def main():
    async with bot:
        await mp.start_radio()
def stop_and_restart():
    bot.stop()
    os.system("git pull")
    sleep(10)
    os.execl(sys.executable, sys.executable, *sys.argv)


bot.run(main())
bot.start()

@bot.on_message(filters.command(["restart", f"restart@{USERNAME}"]) & filters.user(Config.ADMINS) & (filters.chat(CHAT) | filters.private))
async def restart(client, message):
    await message.reply_text("🔄 Memperbarui dan Memulai Ulang...")
    await asyncio.sleep(3)
    try:
        await message.delete()
    except:
        pass
    process = FFMPEG_PROCESSES.get(CHAT)
    if process:
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(e)
            pass
        FFMPEG_PROCESSES[CHAT] = ""
    Thread(
        target=stop_and_restart
        ).start()    


bot.send(
    functions.bots.SetBotCommands(
        commands=[
            types.BotCommand(
                command="start",
                description="Periksa apakah bot hidup"
            ),
            types.BotCommand(
                command="help",
                description="Menampilkan pesan bantuan"
            ),
            types.BotCommand(
                command="play",
                description="Putar lagu dari youtube/audiofile"
            ),
            types.BotCommand(
                command="splay",
                description="Putar lagu dari JioSaavn, gunakan -a flag untuk memutar album."
            ),
            types.BotCommand(
                command="cplay",
                description="Memutar file musik dari saluran."
            ),
            types.BotCommand(
                command="yplay",
                description="Memutar file musik dari playlist youtube."
            ),
            types.BotCommand(
                command="player",
                description="Menampilkan lagu yang sedang diputar dengan kontrol"
            ),
            types.BotCommand(
                command="playlist",
                description="Menampilkan daftar putar"
            ),
            types.BotCommand(
                command="clearplaylist",
                description="Menghapus daftar putar saat ini"
            ),
            types.BotCommand(
                command="shuffle",
                description="Acak daftar putar"
            ),
            types.BotCommand(
                command="export",
                description="Ekspor daftar putar saat ini sebagai file json untuk penggunaan di masa mendatang."
            ),
            types.BotCommand(
                command="import",
                description="Impor daftar putar yang diekspor sebelumnya."
            ),
            types.BotCommand(
                command="upload",
                description="Unggah lagu yang sedang diputar sebagai file audio."
            ),
            types.BotCommand(
                command="skip",
                description="Lewati lagu saat ini"
            ),           
            types.BotCommand(
                command="join",
                description="Bergabung dengan VC"
            ),
            types.BotCommand(
                command="leave",
                description="Meninggalkan VC"
            ),
            types.BotCommand(
                command="vc",
                description="Periksa apakah VC bergabung"
            ),
            types.BotCommand(
                command="stop",
                description="Berhenti Memutar"
            ),
            types.BotCommand(
                command="radio",
                description="Mulai radio / Siaran langsung"
            ),
            types.BotCommand(
                command="stopradio",
                description="Menghentikan radio / Siaran langsung"
            ),
            types.BotCommand(
                command="replay",
                description="Putar ulang dari awal"
            ),
            types.BotCommand(
                command="clean",
                description="Membersihkan file RAW"
            ),
            types.BotCommand(
                command="pause",
                description="Jeda lagunya"
            ),
            types.BotCommand(
                command="resume",
                description="Lanjutkan lagu yang dijeda"
            ),
            types.BotCommand(
                command="mute",
                description="Bisukan di VC"
            ),
            types.BotCommand(
                command="volume",
                description="Atur volume antara 0-200"
            ),
            types.BotCommand(
                command="unmute",
                description="Suarakan di VC"
            ),
            types.BotCommand(
                command="restart",
                description="Perbarui dan mulai ulang bot"
            )
        ]
    )
)

idle()
bot.stop()
