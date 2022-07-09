import json
from discord import embeds
import pandas as pd
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from os import sys
from time import sleep
from slash.generales import Generales
from verificar import get_mochila

class Hallowen(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="hallBag", description="muestra tu inventario de hallowen")
    async def hall_inv(self, msg: SlashContext):
        username = msg.author.name
        user_id = msg.author.id
        new_msg = await msg.reply("**Cargando...**")
        mochila = get_mochila(user_id, user_id)
        color = self.color_aleatorio()
        title = f'Inventario de hallowen de {username}'
        description = ''
        valor = '0'
        value_items = ''
        if len(mochila) == 0:
            description += 'Inventario Vacio'
        else:
            for item in mochila:
                nombre = item[2]
                cantidad = item[3]
                item_value = self.dropeos_hallowen[nombre]["valor"]
                if self.dropeos_hallowen[nombre]['valor'] != None:
                    val = f'{item_value} * {cantidad}'
                    res = self.calculadora(val, letras = True)
                    description += f'{self.dropeos_hallowen[nombre]["emoji"]} x{cantidad}\t|\t({res})\n'
                    valor += f'+{val}'
                else:
                    description += f'{self.dropeos_hallowen[nombre]["emoji"]} x{cantidad}\n'
                    value_items += f'{nombre.replace("_", " ").capitalize()}  x{cantidad}\n'
        valor = self.calculadora(valor)
        embed = discord.Embed(title=title, description=description, color=color)
        name = f'Cantidad en coins: '
        value = f'{valor}'
        embed.add_field(name=name, value=value, inline=False)
        if value_items != '':
            name = f'Items: '
            value = f'{value_items}'
            embed.add_field(name=name, value=value, inline=False)
        
        query = f"SELECT  * FROM cambios WHERE user_id = '{user_id}'"
        peticiones = self.query_consulta(query)
        if len(peticiones) > 0:
            pendiente = ''
            pendiente_cantidad = '0'
            pendiente_items = 0
            entregado = ''
            entregado_cantidad = '0'
            entregado_items = 0
            for pet in peticiones:
                if pet[7] == 'pendiente':
                    if pet[3] == 1:
                        operacion = f'{pendiente_cantidad}  + {pet[4]}'
                        pendiente_cantidad = self.calculadora(operacion, letras = True)
                    elif pet[3] == 2:
                        pendiente_items += pet[4]
                else:
                    if pet[3] == 1:
                        operacion = f'{entregado_cantidad}  + {pet[4]}'
                        entregado_cantidad = self.calculadora(operacion, letras = True)
                    elif pet[3] == 2:
                        entregado_items += pet[4]
            if pendiente_cantidad != '0':
                pendiente = f'Coins: {pendiente_cantidad}\n'
            if pendiente_items != 0:
                pendiente += f'God Potion: {pendiente_items}\n'
            if pendiente != '':
                name = f'Cambios pendientes por entregar:'
                value = f'{pendiente}'
                embed.add_field(name=name, value=value, inline=False)
            if entregado_cantidad != '0':
                entregado = f'Coins: {entregado_cantidad}\n'
            if entregado_items != 0:
                entregado += f'God Potion: {entregado_items}\n'
            if entregado != '':
                name = f'Entregados:'
                value = f'{entregado}'
                embed.add_field(name=name, value=value, inline=False)
        await new_msg.edit(content = '', embed = embed)

    @cog_ext.cog_slash(name="hallValues", description="muestra los valores de cada item")
    async def hall_values(self, msg: SlashContext):
        self.dropeos_hallowen
        title = 'Valores de los items'
        description = ''
        color = self.color_aleatorio()
        msg = await msg.reply('**Cargando...**')
        for item, data in self.dropeos_hallowen.items():
            description += f'{data["emoji"]} - {data["value"]}\n'
        embed = discord.Embed(title=title, description=description, color=color)
        text = 'Se iran agregando items a lo largo del evento'
        embed.set_footer(text=text)
        await msg.edit(content = '', embed = embed)

def setup(bot):
    bot.add_cog(Hallowen(bot))