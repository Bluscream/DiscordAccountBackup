import discord
from classes.User import User
from classes.Message import Message
from util import log

class Guild(object):
    id = 0
    name = ""
    owner = None
    invite_urls = []

    def __init__(self, guild : discord.guild.Guild):
        self.id = guild.id
        self.name = guild.name
        if guild.owner: self.owner = User(guild.owner)

    async def createInvite(self, channel : discord.TextChannel):
        invite = await channel.create_invite(reason="", max_age=0, max_uses=0, temporary=False, unique=False)
        log("Created Invite", invite.code, "for", invite.guild.name)
        self.invite_urls.append(invite.url)

    async def getInvite(self, guild : discord.guild.Guild):
        for channel in guild.text_channels:
            msgs = channel.history()
            for msg in msgs:
                _msg = Message(msg)

    async def createInvites(self, guild : discord.guild.Guild, singleInviteOnly=True):
        if guild.me.guild_permissions.create_instant_invite:
            if guild.system_channel:
                if guild.system_channel.permissions_for(guild.me).create_instant_invite:
                    await self.createInvite(guild.system_channel)
                    if singleInviteOnly: return self.invite_urls
        else:
            for channel in guild.channels:
                if channel.permissions_for(guild.me).create_instant_invite:
                    await self.createInvite(channel)
                    if singleInviteOnly: return self.invite_urls
        return self.invite_urls