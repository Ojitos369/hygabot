import json
import pandas as pd
import gc
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from os import sys
from time import sleep
from do_embeds import do_embed
from slash.generales import Generales, Item

class Auction(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    save_data = 0

    async def get_auction_data(self, msg, separado):
        link_base = 'https://api.hypixel.net/skyblock/auctions'
        paginas_totales = 100
        pagina = 0
        paginando = True
        ahora = self.fecha_plana()
        ultima_actualizacion = self.save_data
        
        data = {}
        await msg.edit(content='**Actualizando datos en paginas 0 - 10**')
        active_auctions = []
        # obteniendo toda la auction
        while paginando:
            if pagina % 10 == 0:
                await msg.edit(content=f'**Actualizando datos en paginas {pagina} - {pagina + 10}**')
            primero = link_base + '?key='
            segundo = f'&page={pagina}'
            datos = self.consulta(primero, segundo)
            if 'success' in datos:
                if datos['success'] == False:
                    break
            auctions = datos['auctions']
            for auction in auctions:
                auc = {}
                auc['id'] = auction['uuid']
                auc['name'] = auction['item_name']
                auc['vendedor'] = auction['auctioneer']
                auc['inicio'] = auction['start']
                auc['fin'] = auction['end']
                auc['lore'] = auction['item_lore']
                auc['tier'] = auction['tier']
                auc['extra'] = auction['item_bytes']
                if 'bin' in auction:
                    auc['modo'] = 'bin'
                else:
                    auc['modo'] = 'auction'
                precio = auction['starting_bid']
                if auction['highest_bid_amount'] > precio:
                    precio = auction['highest_bid_amount']
                auc['precio'] = precio
                auc['categoria'] = auction['category']
                active_auctions.append(auc)

            pagina += 1
            if pagina > paginas_totales:
                break
        save_data = {}
        data['actualizacion'] = ahora

        await msg.edit(content='**Acomodando Datos...**')
        for auction in active_auctions:
            name = auction['name']
            name = name.lower().replace('_', ' ').replace('-', ' ').replace("'", "")
            for palabra in name.split():
                first_letter = palabra[0].lower()
                if first_letter in save_data:
                    if auction['id'] not in save_data[first_letter]:
                        save_data[first_letter][auction['id']] = auction
                else:
                    save_data[first_letter] = {auction['id']: auction}
        for auction in active_auctions:
            if name == 'Enchanted Book':
                for letra in save_data:
                    if auction['id'] not in save_data[letra]:
                        save_data[letra][auction['id']] = auction
        
        ultima_actualizacion = ahora
        del data
        gc.collect()

        auctions = []
        await msg.edit(content = '**Seleccionando datos...**')
        for palabra in separado:
            first_letter = palabra[0].lower()
            if first_letter in save_data:
                datos = save_data[first_letter].values()
                i = 0
                for dato in datos:
                    i += 1
                    auctions.append(dato)
        del save_data
        gc.collect()
        self.save_data = ultima_actualizacion
        return auctions
    
    def for_books_name(self, dato):
        item_bytes = dato['extra']
        book_replace = ''
        for linea in item_bytes['tag']['display']['Lore']:
            # from I to X
            if ' I ' in linea or 'II' in linea or 'III' in linea or 'IV' in linea or 'V' in linea or 'VI' in linea or 'VII' in linea or 'VIII' in linea or 'IX' in linea or 'X' in linea:
                book_replace += self.remplazar(linea) + ', '
        if book_replace.endswith(', '):
            book_replace = book_replace[:-2]
        return book_replace

    def filtrar_auctions(self, data, separado, quitar, bin, auction, rareza):
        def corregir_emoji(text):
            corrigiendo = False
            corregido = False
            for letra in range(len(text)):
                if text[letra] == '<':
                    corrigiendo = True
                if corrigiendo:
                    if text[letra] == ' ':
                        text = text[:letra] + '_' + text[letra + 1:]
                    if text[letra] == '>':
                        corrigiendo = False
                        corregido = True
                if corregido:
                    break
            return text
        def emoji_repalce(text):
            text = str(text)
            text = text.lower()
            text = corregir_emoji(text)
            remp = {
                "<": "",
                ">": " ",
                ":": " ",
            }
            for key in remp:
                text = text.replace(key, remp[key])
            return text

        def remplazos(text):
            remp = {
                "'": "",
                "-": " "
            }
            for key in remp:
                text = text.replace(key, remp[key])
            return text
        encontrados = {}
        for i in range(len(data)):
            dato = data[i]
            try:
                dato['extra'] = item_bytes = Item.decode_inventory_data(dato['extra'])['i'][0]
            except:
                pass
            encontrado = True
            original_name = dato['name'].replace('_', ' ')
            if original_name[0] == ' ':
                original_name = original_name[1:]
            if original_name == 'Enchanted Book':
                item_name = self.for_books_name(dato)
            else:
                item_name = original_name
            if item_bytes['Count'] > 1:
                item_name += f' x{item_bytes["Count"]}'
            for palabra in separado:
                if palabra.lower() not in remplazos(item_name.lower().replace(' ', '')):
                    encontrado = False
                    break
            if encontrado and quitar != '****------****':
                if quitar in item_name:
                    encontrado = False
            
            if encontrado and (bin or auction):
                modo = dato['modo']
                if bin and modo != 'bin':
                    encontrado = False
                if auction and modo != 'auction':
                    encontrado = False

            if encontrado and rareza != '':
                item_rarity = dato['tier'].lower()
                common = 'com common comun común'
                uncommon = 'uncom uncommon uncom uncomún'
                rare = 'rare raro rara rar'
                epic = 'epic epica ep epíca'
                legendary = 'leg legendary legendaria legendari legendária'
                mythic = 'myth mythic mitica mitíca'
                divine = 'div divine divina divin'
                special = 'special especial especiale especiale'
                rareza = rareza.lower()
                if rareza in common:
                    rareza = 'common'
                elif rareza in uncommon:
                    rareza = 'uncommon'
                elif rareza in rare:
                    rareza = 'rare'
                elif rareza in epic:
                    rareza = 'epic'
                elif rareza in legendary:
                    rareza = 'legendary'
                elif rareza in mythic:
                    rareza = 'mythic'
                elif rareza in divine:
                    rareza = 'divine'
                elif rareza in special:
                    rareza = 'special'

                if rareza != item_rarity:
                    encontrado = False

            if encontrado:
                try:
                    emoji = self.get_emoji_name(original_name, just_emoji = True)
                except:
                    emoji = ''
                if emoji_repalce(emoji) in emoji_repalce(item_name):
                    new_name = item_name
                else:
                    new_name = emoji + ' ' + item_name
                if emoji != '':
                    new_name = corregir_emoji(new_name)
                if len(new_name) > 150:
                    new_name = new_name[:150]
                    new_name += '...'
                dato['name'] = new_name
                
                if dato['id'] not in encontrados:
                    encontrados[dato['id']] = dato

        items_result = []
        for id in encontrados:
            if len(items_result) == 0:
                items_result.append(encontrados[id])
            else:
                for i in range(len(items_result)):
                    if encontrados[id]['precio'] < items_result[i]['precio']:
                        items_result.insert(i, encontrados[id])
                        break
                    elif i == len(items_result) - 1:
                        items_result.append(encontrados[id])
                        break
        return items_result

    def embeds_data_det(self, item, detallado, total):
        name = item['name']
        extra = item['extra']
        # recomb
        try:
            recomb = extra['tag']['ExtraAttributes']['rarity_upgrades']
        except:
            recomb = 0
        #potatos
        try:
            potatos = extra['tag']['ExtraAttributes']['hot_potato_count']
            fuming = 0
            if potatos > 10:
                potatos = 10
                fuming = potatos - 10
        except:
            potatos = 0
            fuming = 0
        #gemas
        try:
            gemas = extra['tag']['ExtraAttributes']['gems']
        except:
            gemas = {}

        if recomb > 0:
            name = name + self.recomb_item()
        lore = self.remplazar(item['lore'])
        vendedor = self.get_username(uuid = item['vendedor'])
        fin = self.obtener_tiempo_relativo(item['fin'])
        tier = item['tier'].lower().capitalize()
        precio = self.calculadora(f"{item['precio']} + 0", entero = True)
        categoria = item['categoria'].lower().capitalize()
        modo = item['modo'].lower().capitalize()
        # Doing data embed
        color = self.color_aleatorio()
        title = f'{name}'
        description = f'```{lore}```\n'
        description += f'**Vendedor:** `{vendedor}`\n'
        description += f'**Precio:** `{precio}`\n'
        description += f'**Tipo:** `{modo}`\n'
        description += f'**Tiempo restante:** `{fin}`\n'
        description += f'**Tier:** `{tier}`\n'
        description += f'**Categoría:** `{categoria}`\n'
        if recomb > 0:
            description += f'**Item recombulado**\n'
        if potatos > 0:
            description += f'**Hot Potato Books:** `{potatos}`\n'
            if fuming > 0:
                description += f'**Fuming Potato Books:** `{fuming}`\n'
        
        for_embed = {}
        for_embed['title'] = title
        for_embed['description'] = description
        for_embed['color'] = color
        embeds_data = [for_embed]
        return embeds_data

    def embeds_data(self, data, busqueda):
        def pet_item_replace(item):
            #pet_item.replace('Pet Item ', '').replace('Skill', 'EXP')
            replaces = {
                'Pet Item': '',
                'Skill': 'EXP'
            }
            for origin, replace in replaces.items():
                item = item.replace(origin, replace)
            return item
        items_por_pagina = 9
        items_totales = len(data)
        color = self.color_aleatorio()
        title = f'Resultados para {busqueda} - {items_totales} resultados'
        embeds_data = []
        items_en_pagina = 0
        for_embed = {}
        for_embed['title'] = title
        for_embed['color'] = color
        for_embed['fields'] = []
        name = ''
        value = ''
        item_total = 0
        for i in range(len(data)):
            item_total += 1
            item = data[i]
            name = item['name']
            name = f'{item_total}/{items_totales} {name}'
            extra = item['extra']
            fin = self.obtener_tiempo_relativo(item['fin'])
            tier = item['tier'].lower().capitalize()
            tier = f'*{tier}*' + self.auction_emoji(tier)
            precio = self.calculadora(f"{item['precio']} + 0", entero = True)
            categoria = item['categoria'].lower().capitalize()
            modo = item['modo'].lower().capitalize()
            try:
                recomb = extra['tag']['ExtraAttributes']['rarity_upgrades']
            except:
                recomb = 0
            if recomb > 0:
                name = name + self.recomb_item()
            enchants = ''
            try:
                enchantments = extra['tag']['ExtraAttributes']['enchantments']
                for ench, lvl in enchantments.items():
                    ench = ench.capitalize()
                    enchants += f'{ench}: {lvl}, '
                enchants = enchants[:-2]
            except:
                pass
            if len(enchants) > 150:
                enchants = enchants[:150]
                enchants += '...'

            pet_info = ''
            if '[Lvl' in name and ']' in name:
                pet_data = extra['tag']['ExtraAttributes']['petInfo']
                pet_data = json.loads(pet_data)
                try:
                    pet_item = pet_data['heldItem'].replace('_', ' ').title()
                    pet_item = pet_item_replace(pet_item)
                    item_emoji = self.get_emoji_name(pet_item, just_emoji = True)
                    pet_item = f'*{pet_item}* {item_emoji}'
                except:
                    pet_item = 0
                try:
                    candies = pet_data['candyUsed']
                except:
                    candies = 0
                try:
                    skin = pet_data['skin']
                    skin = skin.replace('_', ' ').title()
                except:
                    skin = 0
                if pet_item != 0:
                    pet_info += f'`Item:` {pet_item}\n'
                if candies != 0:
                    pet_info += f'`Dulces:` *{candies}*\n'
                if skin != 0:
                    pet_info += f'`Skin:` *{skin}*\n'

            value = ''
            value += f'`Precio:` *{precio}*\n'
            value += f'`Tipo:` *{modo}*\n'
            value += f'`Tiempo restante:` *{fin}*\n'
            value += f'`Tier:` {tier}\n'
            value += f'`Categoría:` *{categoria}*\n'
            if len(enchants) > 0:
                value += f'`Encantamientos:` *{enchants}*\n'
            if len(pet_info) > 0:
                value += pet_info
            for_embed['fields'].append([name, value, True])
            items_en_pagina += 1
            if items_en_pagina == items_por_pagina:
                embeds_data.append(for_embed)
                for_embed = {}
                for_embed['title'] = title
                for_embed['color'] = color
                for_embed['fields'] = []
                items_en_pagina = 0

        if items_en_pagina > 0:
            embeds_data.append(for_embed)
        paginas_totales = len(embeds_data)
        for i in range(len(embeds_data)):
            text = f'Pagina {i+1} de {paginas_totales}'
            embeds_data[i]['footer'] = text
        
        return embeds_data

    # ----------- COMANDO AH -----------
    @cog_ext.cog_slash(name="auctionHouse", description="Muestra el AH", options = [
        create_option(
            name = 'busqueda',
            description = 'Busqueda a realizar',
            option_type = 3,
            required=True
        ),
        create_option(
            name = 'modo',
            description = 'Filtro entre bin/auction',
            option_type = 3,
            required=False,
        ),
        create_option(
            name = 'quitar',
            description = 'Quitar resultados que coincidan',
            option_type = 3,
            required=False,
        ),
        create_option(
            name = 'rareza',
            description = 'Filtrar items por rareza',
            option_type = 3,
            required=False,
        ),
        create_option(
            name = 'detallar',
            description = 'Detallar un resultado en especifico',
            option_type = 4,
            required=False
        )
    ])
    async def auction(self, msg: SlashContext, busqueda: str, modo: str = '', quitar: str = '', rareza: str ='', detallar: int = -1):
        self.config()
        modo = modo.lower()
        if not  (modo == 'bin' or modo == 'auction' or modo == ''):
            await msg.reply('Modo invalido. puede ser ("bin" o "auction"')
            return
        
        # ---------  Revisando Modo ---------
        solo_bin = False
        solo_auction = False
        if modo == 'bin':
            solo_bin = True
        elif modo == 'auction':
            solo_auction = True
        
        # ---------  Revisando Quitar ---------
        if quitar == '':
            quitar = '****------****'
        quitar = quitar.lower()

        # ---------  Revisando Detallar ---------
        detallado = False
        if detallar != -1:
            detallado = True

        mostrar_res = 1
        if busqueda == '*' and msg.author.id not in self.developers_ids:
            await msg.reply('Esta busqueda solo esta disponible en version tester')
            return
        separado = busqueda.replace("'", "").split(' ')
        original_msg = msg
        msg = await msg.reply('**Cargando...**')
        
        now_inicial = datetime.now()
        auctions = await self.get_auction_data(msg, separado)
        await msg.edit(content='**Filtrando...**')
        try:
            items = self.filtrar_auctions(auctions, separado, quitar, solo_bin, solo_auction, rareza)
        except Exception as e:
            print(e)
            await msg.edit(content='**Error en el filtro. Por favor reporte el bug :3**')
            return

        if detallado:
            detallar -= 1
            if detallar > len(items) - 1:
                await msg.edit(content=f'**Revisas la lista compreta. Sola hay {len(items)} Para esta busqueda**')
                return
            embed_data = self.embeds_data_det(items[detallar], detallar + 1, len(items))
            embeds = do_embed(embed_data)
            await msg.edit(content = '', embed = embeds[0])
            return

        if len(items) == 0:
            await msg.edit(content=f'**No se encontraron resultados para "{busqueda}"**')
            return

        embed_data = self.embeds_data(items, busqueda)
        paginas_totales = len(embed_data)
        embeds = do_embed([embed_data[0]])
        now_final = datetime.now()
        total_time = now_final - now_inicial
        await msg.edit(content='', embed=embeds[0])
        user_id = original_msg.author.id
        id_mensaje = msg.id
        guardar = {
            'msg_id': id_mensaje,
            'user_id': user_id,
            'embeds': embed_data,
        }
        open(f'./embeds_data/emb_data.json', 'w').write(json.dumps(guardar, indent=4))
        await msg.channel.send(f'+load {id_mensaje}')
        if paginas_totales > 1:
            await msg.add_reaction('\U000025B6')
        return
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Auction(bot))