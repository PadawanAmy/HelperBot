import disnake
import os
import yaml
import time
import random
from disnake.ext import commands
from Core import placeholder

def read_config(file_name):
    with open(file_name, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data

config = read_config("Config.yml")

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.phrases, self.trigger_count = self.load_phrases()
        self.cooldowns = {}

    def load_phrases(self):
        phrases = {}
        trigger_count = 0
        file_path = os.path.join("Triggers.yml")

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                phrases_data = yaml.safe_load(file)
                if phrases_data:
                    phrases = phrases_data
                    trigger_count = sum(1 for phrase, data in phrases.items() if phrase != "Ignore")
        return phrases, trigger_count

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or isinstance(message.channel, disnake.DMChannel):
            return
        if not isinstance(message.author, disnake.Member):
            return
        ignore_channels = config.get('Ignore', {}).get('Channels', [])
        ignore_categories = config.get('Ignore', {}).get('Categories', [])
        if message.channel.id in ignore_channels or \
           (message.channel.category and message.channel.category.id in ignore_categories):
            return
        content = message.content.lower()
        
        for phrase, data in self.phrases.items():
            if phrase == "Ignore":
                continue
            triggers = data.get("Triggers", [])
            is_strict = data.get("Strict", False)
            required_role = data.get("Role")
            missing_role = data.get("MissingRole")
            reply = data.get("Reply", False)
            has_required_role = not required_role or any(role.id == int(required_role) for role in message.author.roles)
            lacks_missing_role = not missing_role or all(role.id != int(missing_role) for role in message.author.roles)
            if ((is_strict and content in map(str.lower, triggers)) or \
                (not is_strict and any(trigger.lower() in content for trigger in triggers))) and \
                has_required_role and lacks_missing_role:
                trigger_cooldown = data.get("Cooldown", 0)
                last_used_time = self.cooldowns.get(phrase, 0)
                current_time = time.time()
                if current_time - last_used_time > trigger_cooldown:
                    self.cooldowns[phrase] = current_time
                    response_type = data.get("Type", "TEXT").upper()
                    if response_type == "RANDOM":
                        responses = data.get("Responses", [])
                        if responses:
                            parsed_response = random.choice(responses)
                            if reply:
                                await message.reply(parsed_response)
                            else:
                                await message.channel.send(parsed_response)
                    elif response_type == "TEXT":
                        response = data.get("Response")
                        if response:
                            parsed_response = placeholder(response, message)
                            if reply:
                                await message.reply(parsed_response)
                            else:
                                await message.channel.send(parsed_response)
                    elif response_type == "EMBED":
                        embed_data = data.get("Embed", {})
                        embed = disnake.Embed(description=placeholder(embed_data.get("Description", ""), message),
                                            color=disnake.Color(int(embed_data.get("Colour", "FFFFFF"), 16)))
                        if "Author" in embed_data:
                            author_data = embed_data["Author"]
                            author_name = placeholder(author_data.get("Name", ""), message)
                            author_icon = placeholder(author_data.get("Icon", ""), message)
                            author_url = author_data.get("Url", "")
                            embed.set_author(name=author_name, icon_url=author_icon, url=author_url)
                        if "Fields" in embed_data:
                            fields_data = embed_data["Fields"]
                            for field_key, field_data in fields_data.items():
                                field_name = placeholder(field_data.get("Name", field_key), message)
                                field_text = placeholder(field_data.get("Text", ""), message)
                                inline = field_data.get("Inline", False)
                                embed.add_field(name=field_name, value=field_text, inline=inline)
                        if "Image" in embed_data:
                            image = placeholder(embed_data.get("Image", ""), message)
                            embed.set_image(url=image)
                        if "Title" in embed_data:
                            title = embed_data["Title"]
                            parsed_title = placeholder(title, message)
                            embed.title = parsed_title
                        if "Thumbnail" in embed_data:
                            image = placeholder(embed_data.get("Thumbnail", ""), message)
                            embed.set_thumbnail(url=image)
                        if "Footer" in embed_data:
                            footer_data = embed_data["Footer"]
                            footer_text = placeholder(footer_data.get("Text", ""), message)
                            footer_icon = placeholder(footer_data.get("Icon", ""), message)
                            embed.set_footer(text=footer_text, icon_url=footer_icon)
                        if reply:
                            await message.reply(embed=embed)
                        else:
                            await message.channel.send(embed=embed)

def setup(bot: commands.Bot):
    HelperCog = Helper(bot)
    bot.add_cog(HelperCog)
    print(f"Successfully Loaded {HelperCog.trigger_count} triggers!")
