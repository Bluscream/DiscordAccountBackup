import asyncio

import discord, json, os
from config import *
from util import *
from classes.User import User, Me
from classes.Guild import Guild
# from time import sleep
file = os.path.basename(__file__)
path = os.path.dirname(os.path.realpath(__file__))
log(file, "START")

class MyClient(discord.Client):
    backupPath = ""
    async def on_ready(self):
        log('Logged on as', self.user)
        self.backupPath = os.path.join(path, str(self.user.id))
        # await self.backupAllEmojis() # Emojis(600772945161486356) # 589047740361867284)
        await self.backupAccountDetails()
        self.backupUsers("friends", self.user.friends)
        self.backupUsers("blocked", self.user.blocked)
        # await self.backupGuilds()
        # self.saveBackup()
        log("Backups finished!")
        await self.logout()

    async def backupAllEmojis(self):
        for guild in self.guilds:
            await self.backupEmojis(guild)
    async def backupEmojis(self, guild = None):
        # _guild : discord.Guild = discord.Guild(state=dict(), data=dict())
        # _emoji : discord.Emoji = discord.Emoji(state=dict(), data=dict(), guild=_guild)
        if guild is int: guild = self.get_guild(guild)
        emojipath = os.path.join(self.backupPath, "guilds", str(guild.id), "emojis")
        log("Backing up", len(guild.emojis), "emojis from guild", guild.name, "(", guild.id, ") into", emojipath)
        createDirFor(emojipath, isDir=True)
        for emoji in guild.emojis:
            extension = str(emoji.url).split(".")[-1]# "gif" if emoji.animated else "png"
            filename = f"{emoji.name}.{extension}"
            path = os.path.join(emojipath, filename)
            log("Saving Emoji", emoji.name, "from", emoji.url, "to", path)
            await emoji.url.save(path)
            # downloadFile(emoji.url, filename)
        teststr = ""
        for emoji in guild.emojis:
            teststr += f":{emoji.name}:"
        print(teststr)
    def backupUsers(self, name, users):
        log("Backing up", name)
        # print("Friends:", , "(",", ".join([f"{a.name}#{a.discriminator}" for a in self.user.friends]),")")
        _users = list()
        for friend in users:
            user = User(friend)
            _users.append(user)
        savePath = os.path.join(self.backupPath, f"{name}.json")
        saveJSON(savePath, _users, encoder=MyEncoder)
        log("Backed up", len(_users), name, "to", savePath)
    async def backupAccountDetails(self):
        log("Backing up account details")
        savePath = os.path.join(self.backupPath, "account.json")
        me = Me(self.user)
        await me.setAvatar(self.user)
        saveJSON(savePath, me, encoder=MyEncoder)

    async def aio_guilds(self):
        guilds = self.guilds
        for guild in guilds:
            yield guild
    async def backupGuilds(self):
        log("Backing up", len(self.guilds), "guilds")
        guilds = list()
        async for guild in self.aio_guilds():
            log("Guild", guild.name, guild.id)
            if not guild or not guild.me: continue
            _guild = Guild(guild)
            await _guild.getInvite(guild) # TODO: FIX UNVERIFICATION
            await asyncio.sleep(sleep_between_invites) # sleep(sleep_between_invites)
            guilds.append(_guild)
        savePath = os.path.join(self.backupPath, "guilds.json")
        saveJSON(savePath, guilds, encoder=MyEncoder)
        log("Backed up", len(guilds), "guilds to", savePath)


client = MyClient()
log("Logging in with", discord_token.split(".")[0]+"...")
client.run(discord_token, bot=False)
log(file, "END")