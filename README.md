# HelperBot
HelperBot is an easy to use Discord bot designed to auto reply to certain phrases in the chat.
There are different types of responses that you can use to fit your needs and many different placeholders you can use to customize the bot however you like.

# Support
If you find any issues with the bot please use the Issues tab.
If you need help using the bot please join my Discord https://discord.gg/2t6N9GwrHy

# Installation
HelperBot uses the Disnake library for Python.
Head over to [Releases](https://github.com/PadawanAmy/HelperBot/releases) to download the latest version.
1. Create a Discord application for your bot from https://discord.com/developers/applications
   - Click "New Application" in the top right
   - Click "Bot" and then "Reset Token"
   - Enable "Message Content Intent" under "Privileged Gateway Intents"
2. Put your new Bot Token in the `Config.yml`
3. Set your prefix and bots activity status
4. Install the dependencies and run the bot
   ```
   pip install -r requirements.txt
   python Main
   ```
5. When the bot starts there will be an Invite Link in the console, use it to invite your bot to a server.
6. Head over to [the wiki](https://github.com/PadawanAmy/HelperBot/wiki) to learn how to use the bot!

By default there are 3 example triggers, you can test the bot works by saying `helper bot test` in a text channel

# Updating
To update the bot, simply backup your Triggers.yml file and Config.yml file and download the latest version from [Releases](https://github.com/PadawanAmy/HelperBot/releases).
Any additions to the Config.yml will be stated in the release notes, you can either add them manually, or use the new default Config.yml and add your old values in.
