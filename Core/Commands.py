import disnake
import yaml
from disnake.ext import commands
from disnake.ext.commands import has_permissions, CommandError

def read_config():
    with open("Config.yml", "r") as file:
        config_data = yaml.safe_load(file)
    return config_data

config = read_config()

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload")
    @has_permissions(manage_messages=True)
    async def reload_ctx(self, ctx):
        self.bot.reload_extension('Core.Helper')
        embed = disnake.Embed(title=f"Reloaded!", color=2669318)
        embed.description = f"```Helper was successfully reloaded!```"
        embed.set_footer(text=f"{self.bot.user}")
        await ctx.send(embed=embed)

    @commands.slash_command()
    async def helper(self, inter):
        pass
    @helper.sub_command(description="Reload helper triggers")
    @has_permissions(manage_messages=True)
    async def reload(self, inter):
        self.bot.reload_extension('Core.Helper')
        embed = disnake.Embed(title=f"Reloaded!", color=2669318)
        embed.description = f"```Helper was successfully reloaded!```"
        embed.set_footer(text=f"{self.bot.user}")
        await inter.send(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed()
            embed.title = "⚠️ Error."
            embed.color = 14279195
            embed.description = "You do not have the required permissions to use this command."
            await inter.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, CommandError):
            await inter.send(f"An error occurred: {error}", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Commands(bot))