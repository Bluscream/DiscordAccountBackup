import discord
from base64 import b64encode, b64decode

class User(object):
    id = 0
    username = ""
    discriminator = 0
    def __init__(self, user : discord.user.User):
        self.id = user.id
        self.username = user.name
        self.discriminator = user.discriminator

class Me(object):
    avatar = ""
    username = ""
    def __init__(self, user: discord.user.ClientUser):
        # print("Mro:", user.__class__.__mro__)
        # super().__init__(super(discord.user.ClientUser, user))
        self.username = user.name

    async def setAvatar(self, user: discord.user.ClientUser):
        avatar = await user.avatar_url_as().read()
        self.avatar = b64encode(avatar).decode('utf-8')