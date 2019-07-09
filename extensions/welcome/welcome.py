import discord
from discord.ext import commands
from util import Handlers
import asyncio
class Welcome(commands.Cog, name="Welcome"):
    def __init__(self, crab):
        self.crab = crab
        self.verification = self.crab.config["verification"]
        self.guild = self.crab.get_guild(self.crab.config["guild"])
        self.info_channel = self.guild.get_channel(self.verification["info_channel"])
        self.waiting_time = self.verification["waiting_time"]
        self.verified_role = self.guild.get_role(self.verification["verified_role"])
        self.channel_name = self.verification["channel_name"]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        }
        channel = await self.guild.create_text_channel(self.channel_name + str(member.id), overwrites=overwrites)

        async for message in self.info_channel.history(limit=None):
            embed = discord.Embed(color=message.author.color)
            embed.description = message.content
            try:
                embed.set_image(url=message.attachments[0].url)
            except:
                pass
            await channel.send(embed=embed)

        time_left = self.waiting_time-10
        embed = discord.Embed(color=discord.Color(0x191919))
        embed.set_author(name="Welcome!", icon_url=member.avatar_url)
        embed.description = f"Please read the info above and wait {self.waiting_time} seconds!"
        embed.add_field(name="Time left", value=f"{time_left} seconds.")
        message = await channel.send(embed=embed)

        while time_left >= 0:
            await asyncio.sleep(10)
            time_left -= 5
            embed.set_field_at(index=0, name="Time left", value=f"{time_left+10} seconds.")
            await message.edit(embed=embed)
        try:
            await member.add_roles(self.verified_role)
        except:
            pass
        return await channel.delete()
