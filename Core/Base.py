import disnake
import os
import yaml
import datetime
from disnake.ext import commands

def read_config():
    with open("Config.yml", "r") as file:
        config_data = yaml.safe_load(file)
    return config_data

config = read_config()

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"#######################################\n##  Helper Bot started successfully. ##\n##             v1.0                  ##\n#######################################\nBot User: {self.bot.user}\nBot ID: {self.bot.user.id}")
        activity_name = config.get('Bot', {}).get('Status', {}).get('Text')
        activity_type = getattr(disnake.ActivityType, config.get('Bot', {}).get('Status', {}).get('Activity'))
        await self.bot.change_presence(activity=disnake.Activity(name=activity_name, type=activity_type))
        print("Invite Link: https://discord.com/oauth2/authorize?scope=bot+applications.commands&client_id={self.bot.user.id} \n...Ready for use")

def setup(bot: commands.Bot):
    bot.add_cog(Base(bot))
