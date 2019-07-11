import discord
from discord.ext import commands
from util import Handlers
import asyncio
class Welcome(commands.Cog, name="Welcome"):
    def __init__(self, crab):
        self.crab = crab

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        verification = self.crab.config["guilds"][str(guild.id)]["verification"]
        info_channel = guild.get_channel(verification["info_channel"])
        waiting_time = verification["waiting_time"]
        verified_role = guild.get_role(verification["verified_role"])
        channel_name = verification["channel_name"]
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        }
        channel = await guild.create_text_channel(channel_name + str(member.id), overwrites=overwrites)

        async for message in info_channel.history(limit=None):
            embed = discord.Embed(color=discord.Color(0x191919))
            embed.description = message.content
            try:
                embed.set_image(url=message.attachments[0].url)
            except:
                pass
            await channel.send(embed=embed)

        time_left = waiting_time-5
        embed = discord.Embed(color=discord.Color(0x191919))
        embed.set_author(name="Welcome!", icon_url=member.avatar_url)
        embed.description = f"Please read the info above and wait {waiting_time} seconds!"
        embed.add_field(name="Time left", value=f"{time_left} seconds.")
        message = await channel.send(embed=embed)

        while time_left >= 0:
            await asyncio.sleep(5)
            time_left -= 5
            embed.set_field_at(index=0, name="Time left", value=f"{time_left+5} seconds.")
            await message.edit(embed=embed)
        try:
            await member.add_roles(verified_role)
        except:
            pass
        return await channel.delete()
