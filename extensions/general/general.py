import discord
from discord.ext import commands
import os
import time
from util import Handlers

class General(commands.Cog, name="General"):
    def __init__(self, crab):
        self.crab = crab

    @commands.command()
    async def ping(self, ctx):
        b = time.monotonic()
        message = await ctx.send("Pinging...")
        await ctx.trigger_typing()
        ping = (time.monotonic() - b) * 1000
        ping = round(ping)
        await message.delete()
        return await ctx.send(f"Pong, {ping}ms")
