import json
import os
import discord
import asyncio

class Handlers:
    class JSON:
        def __init__(self, crab):
            self.crab = crab

        def read(file):
            with open(f"{file}.json", "r", encoding="utf8") as file:
                data = json.load(file)
            return data

        def dump(file, data):
            with open(f"{file}.json", "w", encoding="utf8") as file:
                    json.dump(data, file, indent=4)
