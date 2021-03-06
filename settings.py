import os

extensions = [
    # 'plex',
    # 'plex_manager',
    # 'plex_manager_nodb',
    'jellyfin'
    # 'jellyfin_manager',
    # 'emby_manager',
    # 'olaris_manager',
    # 'booksonic',
    # 'rclone',
    # 'news',
    # 'marta',
    # 'roles',
    # 'espn',
    # 'yahoo_fantasy',
    # 'sengled',
    # 'google_home',
    # 'wink',
    # 'coronavirus',
    # 'speedtest',
    # 'voice_channel'
]

PREFIX = "*"
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

USE_DROPBOX = False
# True: Can download/upload cogs from Dropbox
# False: Cogs have to be local
DROPBOX_API_KEY = os.environ.get('DROPBOX_API_KEY')

USE_REMOTE_CONFIG = False
# True: Load/store cogs from a remote "cogs.txt" file in Dropbox (will need to know folder.file of each)
# False: Load cogs from the ext list below.
