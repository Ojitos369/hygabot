import json
import pandas as pd
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from do_embeds import do_embed
from os import sys
from time import sleep
from slash.generales import Generales, Item

class Basicos(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="name", description="description", options=[])
    async def _funcion(self, msg: SlashContext):
        await msg.reply('Hola Mundo')
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Basicos(bot))