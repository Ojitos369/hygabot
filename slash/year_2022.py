import random
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
    
    async def permitidos_msg(self, msg):
        original_msg = msg
        msg = await msg.reply('Enviando')
        await msg.delete()
        o_3695 = 88564386200827085
        o_369 = 673397248427556887
        dfot = 449754781854990346
        jalufo = 618743923912867851
        gearl = 386270777420414977
        ferqo = 299039228136783872
        channel_id = 831264017270964243
        #channel_id = 877023945189130301
        channel = self.bot.get_channel(channel_id)
        user_mention = ''
        user = original_msg.author
        user_id = user.id
        print(user_id == o_369)
        if user_id == o_369 or user_id == o_3695:
            user_mention = f'{user.name}'
        elif user_id == dfot:
            user_mention = f'beta-user y developer helper: {user.name}'
        elif user_id == jalufo or user_id == ferqo:
            user_mention = f'beta-user: {user.name}'
        elif user_id == gearl:
            user_mention = f'el gran jefe: {user.name}'
        year_2022 = ':two::zero::two::two:'
        title = f":partying_face: Excelente {year_2022} de parte de {user_mention}"
        description = f':tada: Que todas sus metas se cumplan :gift: y gracias por el apoyo recibido al bot\n'
        description += '\nHaremos lo posible por mejorar y traerles las funcionalidades que se merecen\n'
        description += '\nSigan apoyando y confiando en nosotros :relaxed: \n'
        description += '\nPor un 2022 lleno de metas cumplidas, dentro y fuera de hypixel\n'
        description += '\nMis mejores deseos\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title = title, description = description, color = color)
        text = ''
        await channel.send(content = '@everyone', embed = embed)
        return
    
    async def msg_general(self, msg):
        user = ' ' + msg.author.name + ' '
        emojis = []
        year_2022 = ':two::zero::two::two:'
        emojis.append(' :partying_face: ')
        emojis.append(' :tada: ')
        emojis.append(' :gift: ')
        inicios = []
        inicios.append('Feliz año nuevo')
        inicios.append(f'Excelente {year_2022}')
        extras = []
        extras.append(f'Que todas tus metas se cumplan')
        extras.append(f'Mis mejores deseos para ti')
        mensaje = random.choice(inicios)
        extra = random.choice(extras)
        emoji = random.choice(emojis)
        mensaje = mensaje + user + emoji + extra
        title = mensaje
        description = f'\n:tada: Que todas tus metas se cumplan :gift: y gracias por el apoyo recibido al bot\n'
        description += '\nHaremos lo posible por mejorar y trae las funcionalidades que mereces\n'
        description += '\Sigue apoyando y confiando en nosotros :relaxed: \n'
        description += '\nPor un 2022 lleno de metas cumplidas, dentro y fuera de hypixel\n'
        description += '\nNuestros mejores deseos\n'
        description += f"\n:partying_face: Excelente {year_2022} de parte del team de HygaBot\n"
        color = self.color_aleatorio()
        embed = discord.Embed(title = title, description = description, color = color)
        name = f'Jefe: '
        user = 386270777420414977
        user = self.bot.get_user(user)
        username = user.name
        value = username
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f'Desarrolladores:'
        #ojitos = 673397248427556887
        #dfot = 449754781854990346
        user = 673397248427556887
        user = self.bot.get_user(user)
        username = user.name
        value = username
        user = 449754781854990346
        user = self.bot.get_user(user)
        username = user.name
        value += f'\n{username}'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = 'Beta tester:'
        #jalufo = 618743923912867851
        #dfot = 449754781854990346
        #ferqo = 299039228136783872
        value = ''
        user = 618743923912867851
        user = self.bot.get_user(user)
        username = user.name
        value += f'\n{username}'
        user = 299039228136783872
        user = self.bot.get_user(user)
        username = user.name
        value += f'\n{username}'
        user = 449754781854990346
        user = self.bot.get_user(user)
        username = user.name
        value += f'\n{username}'
        
        embed.add_field(name = name, value = value, inline = False)
        
        await msg.reply(embed = embed)
        
    @cog_ext.cog_slash(name="feliz2022", description="Feliz año 2022", options=[])
    async def _funcion(self, msg: SlashContext):
        await self.msg_general(msg)
        return
        #o_3695 = 88564386200827085
        o_369 = 673397248427556887
        dfot = 449754781854990346
        #jalufo = 618743923912867851
        gearl = 386270777420414977
        #ferqo = 299039228136783872
        permitidos = [o_3695, o_369, dfot, jalufo, gearl, ferqo]
        if msg.author.id not in permitidos:
            await self.msg_general(msg)
            return
    
        await self.permitidos_msg(msg)
        return

def setup(bot):
    bot.add_cog(Basicos(bot))