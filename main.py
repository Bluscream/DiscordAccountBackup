import discord, json, os
from config import *
from utils import saveJSON, loadJSON, MyEncoder, log
from classes.User import User, Me
from classes.Guild import Guild
file = os.path.basename(__file__)
path = os.path.dirname(os.path.realpath(__file__))
log(file, "START")

class MyClient(discord.Client):
    async def on_ready(self):
        log('Logged on as', self.user)
        self.backupPath = os.path.join(path, str(self.user.id))
        await self.backupAccountDetails()
        self.backupUsers("friends", self.user.friends)
        self.backupUsers("blocked", self.user.blocked)
        await self.backupGuilds()
        # self.saveBackup()
        log("Backups finished!")
        await self.logout()
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
    async def backupGuilds(self):
        log("Backing up", len(self.guilds), "guilds")
        guilds = list()
        for guild in self.guilds:
            log("Guild", guild.name, guild.id)
            if guild: guilds.append(Guild(guild, self))
        savePath = os.path.join(self.backupPath, "guilds.json")
        saveJSON(savePath, guilds, encoder=MyEncoder)
        log("Backed up", len(guilds), "guilds to", savePath)


client = MyClient()
log("Logging in with", discord_token.split(".")[0]+"...")
client.run(discord_token, bot=False)
log(file, "END")