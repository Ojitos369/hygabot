import json
import pandas as pd
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from os import sys
from time import sleep
from slash.generales import Generales, Item

class SugBug(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    
    # ----------- COMANDO SUGERENCIA -----------
    @cog_ext.cog_slash(name="sugerencia", description="Ayuda a crecer al bot :D tus ideas son valiosas", options = [
        create_option(
            name = 'sugerencia',
            description = 'Mensaje de tu sugerencia :D',
            option_type = 3,
            required=True
        )
    ])
    async def sugerencia(self, msg: SlashContext, sugerencia: str):
        user = msg.author
        channel = msg.channel
        guild = msg.guild
        msg = await msg.reply('Enviando sugerencia')
        await msg.delete()
        
        title = f'Sugerencia de {user}\nEn {channel} - {guild}'
        description = f'{sugerencia}'
        color = self.color_aleatorio()
        user_avatar = user.avatar_url
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_thumbnail(url=user_avatar)
        
        neko_channel_id = 882986881120362527
        neko_channel = self.bot.get_channel(neko_channel_id)
        await neko_channel.send(embed=embed)
        
        title = f'Sugerencia id: '
        description = f'{sugerencia}'
        embed = discord.Embed(title=title, description=description, color=color)
        hy_channel_id = 924488851400048650
        hy_channel = self.bot.get_channel(hy_channel_id)
        msg = await hy_channel.send(embed=embed)
        title = f'Sugerencia id: {msg.id}'
        description = f'{sugerencia}'
        embed = discord.Embed(title=title, description=description, color=color)
        await msg.edit(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await user.send(f'Tu sugerencia ha sido enviada y se tomara en cuenta :D')

    # ----------- COMANDO BUG -----------
    @cog_ext.cog_slash(name="bug", description="Ayuda a crecer al bot :D disminuyamos los errores", options = [
        create_option(
            name = 'bug',
            description = 'Describe el bug lo mas detallado posible, de ser posible adjuntar id del mensaje original',
            option_type = 3,
            required=True
        )
    ])
    async def bug(self, msg: SlashContext, bug: str):
        user = msg.author
        channel = msg.channel
        guild = msg.guild
        msg = await msg.reply('Enviando el bug')
        await msg.delete()
        
        title = f'Bug de {user}\nEn {channel} - {guild}'
        description = f'{bug}'
        color = self.color_aleatorio()
        user_avatar = user.avatar_url
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_thumbnail(url=user_avatar)
        
        neko_channel_id = 924501313042137099
        neko_channel = self.bot.get_channel(neko_channel_id)
        await neko_channel.send(embed=embed)
        
        title = f'Bug report id: '
        description = f'{bug}'
        embed = discord.Embed(title=title, description=description, color=color)
        hy_channel_id = 924488876612014081
        hy_channel = self.bot.get_channel(hy_channel_id)
        msg = await hy_channel.send(embed=embed)
        title = f'Sugerencia id: {msg.id}'
        description = f'{bug}'
        embed = discord.Embed(title=title, description=description, color=color)
        await msg.edit(embed=embed)
        await user.send(f'Tu bug fue reportado y se trabajara pronto para resolverlo :partying_face:')

def setup(bot):
    bot.add_cog(SugBug(bot))