import disnake
from disnake.ext import commands
import os
import yaml

def read_config():
    with open("Config.yml", "r") as file:
        config_data = yaml.safe_load(file)
    return config_data

config = read_config()

clientIntents = disnake.Intents.default()
clientIntents.message_content = True
prefix = config.get('Bot', {}).get('Prefix')
bot = commands.Bot(command_prefix=prefix, reload=False, intents=clientIntents)
bot.load_extension("Core.Base")
bot.load_extension("Core.Commands")
bot.load_extension("Core.Placeholders")
bot.load_extension("Core.Helper")

bot.run(config.get('Bot', {}).get('Token'))