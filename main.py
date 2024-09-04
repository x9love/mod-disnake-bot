import disnake
from disnake.ext import commands
import os
import sys

from database.LogsDatabase import LogsDatabase
from database.UserInfoDatabase import UsersDataBase


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

intents = disnake.Intents.all()
intents.message_content = True
prefix = os.getenv('PREFIX')
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    users_db = UsersDataBase()
    log_db = LogsDatabase()

    await log_db.create_table_log_chanel()
    await users_db.create_table()
    await users_db.create_table_warns()
    
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

token = os.getenv('STABLE')
bot.run('твой токен')
