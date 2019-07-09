from .bot import crab
from .handlers import Handlers

async def setup(crab):
    await crab.add_cog(Util(crab))
