echo "Cloning Repo...."
git clone https://github.com/qowwim-lab/MusicPlayerTgvc.git /MusicPlayerTgvc
cd /MusicPlayerTgvc
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py