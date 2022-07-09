
import json
import pandas as pd
import discord
from do_embeds import do_embed
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from os import sys
from time import sleep
from slash.generales import Generales

class Reforjes(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="reforje", description="Muestra la informacion de los reforges que coincidan", options=[
        create_option(
            name = 'reforje',
            description = 'palabras de filtro',
            option_type = 3,
            required=True,
        )
    ])
    async def reforje(self, msg: SlashContext, reforje: str):
        original_msg = msg
        item = reforje
        msg = await msg.reply('***Buscando...***')

        items_data = self.buscar_item_data(item)
        if len(items_data) == 0:
            color = self.color_aleatorio()
            title = 'No se encontraron coincidencias :pleading_face:'
            description = 'Recuerda que se estan agregando reforjes constantemente\n\n'
            description += f'Se ha enviado **{item}** pronto sera agregado\n'
            embed = discord.Embed(title=title, description=description, color=color)
            await msg.edit(content = '', embed=embed)
            id_channel = 907827106304655361
            channel = self.bot.get_channel(id_channel)
            title = f'Nuevo Reforje: {item}'
            embed = discord.Embed(title=title, color=color)
            name = f'Autor:'
            value = f'{original_msg.author}'
            embed.add_field(name=name, value=value, inline=False)
            name = f'Server:'
            value = f'{original_msg.guild.name}'
            embed.add_field(name=name, value=value, inline=False)
            name = f'Canal:'
            value = f'{original_msg.channel}'
            embed.add_field(name=name, value=value, inline=False)
            await channel.send(embed=embed)
            return

        embeds_data = self.data_for_embeds(items_data)
        paginas = len(embeds_data)
        for i in range(paginas):
            text = f'Pagina {i+1} / {paginas}'
            embeds_data[i]['footer'] = text
        
        embeds = do_embed(embeds_data)
        await msg.edit(content = '', embed=embeds[0])
        user_id = original_msg.author.id
        id_mensaje = msg.id
        guardar = {
            'msg_id': id_mensaje,
            'user_id': user_id,
            'embeds': embeds_data,
        }
        open(f'./embeds_data/emb_data.json', 'w').write(json.dumps(guardar, indent=4))
        await msg.channel.send(f'+load {id_mensaje}')
        if paginas > 1:
            await msg.add_reaction('\U000025B6')
    
    def buscar_item_data(self, item):
        def replaces(item):
            replaces_dict = {
                "'": '',
                ".": '',
                "-": '',
                '_10': '_x',
                '_1': '_i',
                '_2': '_ii',
                '_3': '_iii',
                '_4': '_iv',
                '_5': '_v',
                '_6': '_vi',
                '_7': '_vii',
                '_8': '_viii',
                '_9': '_ix',
                "_": ' ',
            }
            for key, value in replaces_dict.items():
                item = item.replace(key, value)
            return item
        
        with open('./json/reforges.json') as datos:
            items_data = json.load(datos)

        item = item.lower()
        item = replaces(item)
        separado = item.split(' ')
        items_encontrados = []
        for item_actual in items_data:
            encontrado = True
            name_temp = item_actual.lower()
            name_temp = replaces(name_temp)
            try:
                alias = str(items_data[item_actual]['alias'])
                alias = replaces(alias.lower())
            except:
                alias = ''
            for palabra in separado:
                if palabra not in name_temp and palabra not in alias:
                    encontrado = False
                    break
            if encontrado:
                items_encontrados.append({
                    'name': items_data[item_actual]['name'],
                    'data': items_data[item_actual],
                })
        return items_encontrados

    def data_for_embeds(self, item_data):
        embeds_data = []
        color = self.color_aleatorio()
        for item in item_data:
            title = item['name'].replace('_', ' ').lower()
            title = title.title()
            data = item['data']
            fields = self.fields_data(data)
            for_embed = {}
            for_embed['title'] = title
            for_embed['color'] = color
            for_embed['fields'] = fields
            embeds_data.append(for_embed)
        return embeds_data

    def fields_data(self, data):
        fields = []

        if 'stone' in data:
            name = 'Stone'
            value = self.get_emoji_name(data['stone'])
            fields.append([name, value, False])

        # --------- Obtencion ----------
        name = f'Obtencion'
        value = f'{data["obtencion"]}'
        fields.append([name, value, False])

        # --------- Aplicable ----------
        name = f'Se aplica'
        value = ''
        for tipo in data['aplicable']:
            value += f'{tipo}\n'
        fields.append([name, value, False])

        # --------- Requisitos ----------
        if 'requisitos' in data:
            name = f'Requisitos'
            value = ''
            for tipo in data['requisitos']:
                value += f'{tipo}\n'
            fields.append([name, value, False])

        # --------- Rarezas ----------
        for rareza in data['rarezas']:
            rareza_name = rareza
            rareza = data['rarezas'][rareza]
            emoji = self.general_emoji(rareza_name)
            name = f'\n{rareza_name.capitalize()} {emoji}'
            value = ''
            value += '***Costo***\n'
            value += f'{rareza["costo"]}\n'
            value += '***Stats***\n'
            for stat in rareza['stats']:
                value += f'{stat["stat"]}: **`{stat["cantidad"]}`**\n'
            value += '\n'
            fields.append([name, value, True])

        return fields

    def emoji_for_item(self, item):
        with open('./json/for_items_command.json') as datos:
            emojis_data = json.load(datos)
        text = item.lower().replace(' ', '_')
        emoji = ''
        if text in emojis_data:
            emoji = emojis_data[text].split()[0]
        return f'{emoji} {item}'

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Reforjes(bot))