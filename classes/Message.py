import discord, re

invite_regex = re.compile(r"(discord\.gg/|discordapp\.com/invite/)(\w+)\s")

class Message(discord.Message):
    Invites = list()

    def __init__(self, message : discord.Message, bot : discord.Client):
        # data = dict()
        super().__init__(state=self._state, channel=self.channel, data=self.data)
        # for part in self.content.split(" "):
        for finding in invite_regex.finditer(self.content):
            invite = bot.fetch_invite(finding.string, with_counts=False)
            """
            groups = finding.groups()
            data = dict()
            data["code"] = groups[3]
            invite = discord.Invite(state=dict(), data=data)
            """
            self.Invites.append(invite)