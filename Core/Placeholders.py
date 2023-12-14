import disnake
import datetime
import os
import yaml
from disnake.ext import commands

placeholder_map = {
    'author-mention': ('interaction.user.mention', 'author.mention'),
    'author-username': ('interaction.user.name', 'author.name'),
    'author-nickname': ('interaction.member.nick', 'author.nick'),
    'author-id': ('interaction.user.id', 'author.id'),
    'author-activity': ('', ''),
    'author-status': ('interaction.user.status', 'author.status'),
    'author-toprole': ('interaction.member.top_role.name', 'author.top_role.name'),
    'author-joined': ('interaction.member.joined_at', 'author.joined_at'),
    'author-firstjoin': ('', ''),
    'author-created': ('interaction.user.created_at', 'author.created_at'),
    'author-avatar': ('author.avatar.url', 'author.avatar.url'),
    
    'datetime-datelong': '',
    'datetime-dateshort': '',
    'datetime-time24': '',
    'datetime-time12': '',
    'datetime-day': '',
    'datetime-timestamp': '',

    'server-name': ('guild.name', 'guild.name'),
    'server-id': ('guild.id', 'guild.id'),
    'server-created': ('guild.created_at', 'guild.created_at'),
    'server-owner': ('guild.owner.name', 'guild.owner.name'),
    'server-ownerid': ('guild.owner_id', 'guild.owner_id'),
    'server-membercount': ('guild.member_count', 'guild.member_count'),

    'channel-name': ('channel.name', 'channel.name'),
    'channel-id': ('channel.id', 'channel.id'),
    'channel-mention': ('channel.mention', 'channel.mention'),
    'channel-created': ('channel.created_at', 'channel.created_at'),
    'channel-slowmode': ('channel.slowmode_delay', 'channel.slowmode_delay'),
    'channel-nsfw': ('channel.is_nsfw()', 'channel.is_nsfw()'),
    'channel-topic': ('channel.topic', 'channel.topic'),
}

class UnifiedContext:
    def __init__(self, context):
        if isinstance(context, disnake.Message):
            self.author = context.author
            self.guild = context.guild
            self.channel = context.channel
        elif isinstance(context, commands.Context):
            self.author = context.author
            self.guild = context.guild
            self.channel = context.channel
        else:
            self.author = context.user
            self.guild = context.guild
            self.channel = context.channel

    def get(self, attribute, default=None):
        return getattr(self, attribute, default)

def read_config():
    config_path = "Config.yml"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"The configuration file {config_path} was not found.")
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file) or {}
    return config_data

config = read_config()

def read_user_file(user_id):
    file_path = f"Users/{user_id}.yml"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    return None

def get_author_activity(context):
    if hasattr(context, 'interaction'):
        activities = context.interaction.user.activities
    else:
        activities = context.author.activities
    if activities:
        activity = activities[0]
        if isinstance(activity, disnake.Game):
            return f"Playing {activity.name}"
        elif isinstance(activity, disnake.Streaming):
            return f"Streaming {activity.name}"
        elif isinstance(activity, disnake.Spotify):
            return f"Listening to {activity.title} by {activity.artist}"
        elif isinstance(activity, disnake.CustomActivity):
            return f"{activity.name}"
        else:
            return "Unknown Activity"
    else:
        return "No Current Activity"
    
def get_placeholder_value(context, key, for_image=False):
    if key == 'author-avatar':
        avatar_url = getattr(context.author, 'avatar', None)
        if avatar_url:
            avatar_url = avatar_url.url
        else:
            avatar_url = 'N/A'
        if for_image:
            return {'url': avatar_url}
        else:
            return avatar_url
    if 'datetime-' in key or 'current-' in key:
        now = datetime.datetime.now()
        if key == 'datetime-datelong':
            return now.strftime('%d %B %Y')
        elif key == 'datetime-dateshort':
            date_format = config.get('Placeholders', {}).get('DateFormat', '%d/%m/%y')
            return now.strftime(date_format)
        elif key == 'datetime-time24':
            return now.strftime('%H:%M')
        elif key == 'datetime-time12':
            return now.strftime('%I:%M %p')
        elif key == 'datetime-day':
            return now.strftime('%A')
        elif key == 'datetime-timestamp':
            timestamp = int(now.timestamp())
            return f"<t:{timestamp}:f>"
    if key == 'author-firstjoin':
        user_data = read_user_file(context.author.id)
        return user_data.get('JoinedServer', 'Unknown') if user_data else 'Unknown'
    if key == 'author-mention':
        return f"<@{getattr(context.author, 'id', None)}>"
    attr_path = placeholder_map.get(key)
    if not attr_path:
        return 'N/A'
    attr = attr_path[0] if hasattr(context, 'interaction') else attr_path[1]
    value = get_nested_attr(context, attr)
    if isinstance(value, list) and key == 'author-activity':
        value = value[0].name if value else 'N/A'
    elif isinstance(value, datetime.datetime):
        value = value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, disnake.Status):
        value = str(value)
    elif isinstance(value, disnake.Role):
        value = value.name
    elif isinstance(value, disnake.Member) and key.endswith('nickname'):
        value = value.nick or value.name
    return value

def get_nested_attr(obj, attr):
    try:
        for part in attr.split('.'):
            obj = getattr(obj, part, None)
    except AttributeError:
        return 'N/A'
    return obj

def placeholder(template, context, for_image=False):
    ucontext = UnifiedContext(context)

    for key in placeholder_map.keys():
        placeholder_key = f'{{{key}}}'
        if placeholder_key in template:
            value = get_placeholder_value(ucontext, key, for_image)
            if isinstance(value, dict):
                value = value.get('url', '')
            template = template.replace(placeholder_key, str(value))

    return template

class Placeholders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Placeholders(bot))
