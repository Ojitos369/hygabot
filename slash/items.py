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

class Items(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="item", description="Muestra la informacion de algunos items", options=[
        create_option(
            name = 'item',
            description = 'palabras de filtro',
            option_type = 3,
            required=True,
        ),
        create_option(
            name = 'quitar',
            description = 'quitar items que contengan coincidencias',
            option_type = 3,
            required=False,
        )
    ])


    async def crafteo(self, msg: SlashContext, item: str, quitar: str  = ''):
        original_msg = msg
        msg = await msg.reply('***Buscando...***')

        items_data = self.buscar_item_data(item, quitar)
        if len(items_data) == 0:
            color = self.color_aleatorio()
            title = 'No se encontraron coincidencias :pleading_face:'
            description = 'Recuerda que se estan agregando items constantemente\n\n'
            description += f'Se ha enviado **{item}** pronto sera agregado\n'
            embed = discord.Embed(title=title, description=description, color=color)
            await msg.edit(content = '', embed=embed)
            id_channel = 907827106304655361
            channel = self.bot.get_channel(id_channel)
            title = f'Nuevo item: {item}'
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
    
    def buscar_item_data(self, item, quitar):
        def replaces(item):
            replaces_dict = {
                "'": '',
                "_": ' ',
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
            }
            for key, value in replaces_dict.items():
                item = item.replace(key, value)
            return item
        with open('./json/items.json') as datos:
            items_data = json.load(datos)
        item = item.lower()
        item = replaces(item)
        separado = item.split(' ')
        items = {}
        for palabra in separado:
            first_letter = palabra[0]
            if first_letter in items_data:
                items_now = items_data[first_letter]
                for item_temp in items_now:
                    if item_temp not in items:
                        items[item_temp] = items_now[item_temp]
        del items_data
        items_encontrados = []
        for item_actual in items:
            encontrado = True
            name_temp = item_actual.lower()
            name_temp = replaces(name_temp)
            try:
                alias = str(items[item_actual]['alias'])
                alias = replaces(alias.lower())
            except:
                alias = item_actual
            for palabra in separado:
                if not (palabra in name_temp or palabra in alias):
                    encontrado = False
                    break
            if encontrado and quitar != '':
                quitar = replaces(quitar.lower())
                for palabra in quitar.split():
                    if (palabra in name_temp or palabra in alias):
                        encontrado = False
                        break
            if encontrado:
                items_encontrados.append({
                    'name': items[item_actual]['name'],
                    'data': items[item_actual],
                })
        return items_encontrados

    def data_for_embeds(self, item_data):
        embeds_data = []
        color = self.color_aleatorio()
        for item in item_data:
            title = item['name'].replace('_', ' ').lower()
            title = title.title()
            title = self.get_emoji_name(title)
            data = item['data']
            if 'rareza' in data:
                emoji = self.general_emoji(data['rareza'])
                title = f'{title} {emoji}'
            fields = self.fields_data(data)
            for_embed = {}
            for_embed['title'] = title
            for_embed['color'] = color
            for_embed['fields'] = fields
            embeds_data.append(for_embed)
        return embeds_data

    def fields_data(self, data):
        fields = []
        if 'crafteo' in data:
            emoji = self.general_emoji('crafting table')
            name = f'\n{emoji} Crafteo'
            value = ''
            for item in data['crafteo']:
                item_craft = self.get_emoji_name(item["item"])
                value += f'{item_craft}: `{item["cantidad"]}`\n'
            value += '\n'
            fields.append([name, value, False])

        if 'obtencion' in data:
            emoji = self.general_emoji('obtencion')
            name = f'\n{emoji} Obtencion'
            value = ''
            if isinstance(data['obtencion'], type("")):
                value += data['obtencion']
            elif isinstance(data['obtencion'], type([])):
                for obtencion in data['obtencion']:
                    value += f'*{obtencion}\n'
            value += '\n'
            fields.append([name, value, False])

        if 'forja' in data:
            emoji = self.general_emoji('forja')
            name = f'\n{emoji} Forja'
            value = ''
            dat = data['forja']
            value += '**Items**\n'
            for item in dat['items']:
                item_name = self.get_emoji_name(item['item'])
                value += f'{item_name}: `{item["cantidad"]}`\n'
            value += f'**Tiempo:** {dat["tiempo"]}\n'
            value += '\n'
            fields.append([name, value, False])

        if 'costo' in data:
            emoji = self.general_emoji('cash')
            name = f'\n{emoji} Costo'
            value = ''
            value += data['costo']
            value += '\n'
            fields.append([name, value, False])

        if 'drop_rate' in data:
            emoji = self.general_emoji('probabilidad')
            name = f'\n{emoji} Probabilidad'
            value = ''
            if isinstance(data['drop_rate'], type("")):
                value += data['drop_rate']
            elif isinstance(data['drop_rate'], type([])):
                for rate in data['drop_rate']:
                    value += f'{rate["forma"]}: **`{rate["rate"]}`**\n'
            value += '\n'
            fields.append([name, value, False])

        if 'stats' in data:
            emoji = self.general_emoji('combat')
            name = f'\n{emoji} Stats'
            value = ''
            for stat in data['stats']:
                value += f'{stat["stat"]}: `{stat["cantidad"]}`\n'
            value += '\n'
            fields.append([name, value, False])

        if 'gemas' in data:
            emoji = self.general_emoji('gemas')
            name = f'\n{emoji} Gemas'
            value = ''
            for gema in data['gemas']:
                item_craft = self.emoji_for_item(gema["gema"])
                value += f'{item_craft}: `{gema["cantidad"]}`\n'
            value += '\n'
            fields.append([name, value, False])
        
        if 'requisitos' in data:
            emoji = self.general_emoji('requisitos')
            name = f'\n{emoji} Requisitos'
            value = ''
            for requisito in data['requisitos']:
                value += f'{requisito["requisito"]}\n'
            value += '\n'
            fields.append([name, value, False])
        
        if 'usos' in data:
            emoji = self.general_emoji('crafting table')
            name = f'\n{emoji} Usos'
            value = ''
            for uso in data['usos']:
                uso = self.get_emoji_name(uso)
                value += f'{uso}\n'
            value += '\n'
            fields.append([name, value, False])

        if 'compra' in data:
            emoji = self.general_emoji('compra')
            name = f'\n{emoji} Se puede comprar en:'
            value = ''
            for modo in data['compra']:
                value += f'{modo}\n'
            value += '\n'
            fields.append([name, value, False])
        
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
    bot.add_cog(Items(bot))