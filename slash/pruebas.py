import json
import time
import pandas as pd
import discord
from do_embeds import do_embed
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord import *
from dislash.interactions import *
from discord_components import *
from discord.utils import get
from datetime import datetime
from time import sleep
from slash.generales import Generales, Item

#class Prueba(Generales):
class Prueba(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="prueba", description="description")
    async def pruebas(self, msg: SlashContext):
        o_3695 = 885643862008270858
        o_369 = 673397248427556887
        dfot = 449754781854990346
        jalufo = 618743923912867851
        gearl = 386270777420414977
        ferqo = 299039228136783872
        permitidos = [o_3695, o_369, dfot, jalufo, gearl, ferqo]
        if msg.author.id not in permitidos:
            await msg.reply("Comando disponible solo para beta-tester y desarrollador")
            return
        
        
        channel_id = 831264017270964243
        channel_id = 877023945189130301
        channel = self.bot.get_channel(channel_id)
        user_mention = ''
        user = msg.author
        user_id = user.id
        if user_id == o_369 or user_id == o_3695:
            user_mention = f'{user.mention}'
        elif user_id == dfot:
            user_mention = f'beta-user y developer helper: {user.mention}'
        elif user_id == jalufo or user_id == ferqo:
            user_mention = f'beta-user: {user.mention}'
        elif user_id == gearl:
            user_mention = f'el gran jefe: {user.mention}'
        year_2022 = ':two::zero::two::two:'
        title = f":partying_face: Excelente {year_2022} de parte de {user_mention}"
        description = f':tada: Que todas sus metas se cumplan :gift: y gracias por el apoyo recibido al bot\n'
        description += '\nHaremos lo posible por mejorar y traerles las funcionalidades que se merecen\n'
        description += '\nSigan apoyando y confiando en nosotros :relaxed: \n'
        description += '\nPor un 2022 lleno de metas cumplidas, dentro y fuera de hypixel\n'
        description += '\nMis mejores deseos @everyone\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title = title, description = description, color = color)
        text = ''
        await msg.delete()
        await channel.send(title)
        return
        from ah_data.actualizacion import Auction
        while True:
            auction = Auction()
            await auction.check_data(msg.channel)
            sleep(301)
        return
        
        id = msg.author.id
        uuid = self.get_verify_user(id)
        #base = 'https://api.hypixel.net/resources/skyblock/items'
        #base = 'https://api.hypixel.net/resources/skyblock/skills'
        #base = 'https://api.hypixel.net/resources/skyblock/collections'
        base = 'https://api.hypixel.net/player'
        base += '?key='
        segundo = f'&uuid={uuid}'
        data = self.consulta(base, segundo)
        # save data as pruebas.json
        open('./info_pruebas/pruebas.json', 'w').write(json.dumps(data, indent=4))
        #print(data)
        await msg.reply(f'guardado')
        
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]
def setup(bot):
    bot.add_cog(Prueba(bot))