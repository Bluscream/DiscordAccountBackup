import discord
from base64 import b64encode
from classes.User import User
from utils import log

class Guild(object):
    id = 0
    owner = None
    invite_urls = []
    async def createInvite(self, channel : discord.TextChannel):
        invite = await channel.create_invite(reason="", max_age=0, max_uses=0, temporary=False, unique=False)
        log("Created Invite", invite.code, "for", invite.guild.name)
        return invite.url
    def __init__(self, guild : discord.guild.Guild, bot : discord.Client, singleInviteOnly=True):
        self.id = guild.id
        self.owner = User(guild.owner)
        if guild.me.guild_permissions.create_instant_invite:
                self.invite_urls.append(self.createInvite(guild.system_channel))
                if singleInviteOnly: return
        else:
            for channel in guild.channels:
                perms = channel.permissions_for(guild.me)
                if discord.permissions.Permissions.create_instant_invite in perms:
                    self.invite_urls.append(self.createInvite(channel))
                    if singleInviteOnly: return
