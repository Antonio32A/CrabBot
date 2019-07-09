import discord
from discord.ext import commands
import typing
from util.handlers import Handlers
from util.ctx import Context

class Crab(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Handlers.JSON.read("config")

    async def update_activity(self):
        activity = discord.Activity(name=self.config["activity"]["name"],
                                    type=getattr(discord.ActivityType, self.config["activity"]["type"]))
        await self.change_presence(activity=activity)

    async def load_extensions(self):
        extensions = ["owner", "general", "welcome"]
        for extension in extensions:
            self.load_extension(f"extensions.{extension}")
            print(f"Loaded {extension}.")
        print("Starting...")

    async def on_ready(self):
        print("Starting...")
        await self.load_extensions()
        await self.update_activity()
        print(f"Logged in as {self.user} ({self.user.id})")

    async def on_message(self, message):
        ctx = await self.get_context(message=message, cls=Context)
        await self.invoke(ctx)

def get_pre(crab, message):
    id = crab.user.id
    l = [f"<@{id}> ", f"<@!{id}> ", crab.config["prefix"]]
    return l

crab = Crab(command_prefix=get_pre, owner_id=166630166825664512)
