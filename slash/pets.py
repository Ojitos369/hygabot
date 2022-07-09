import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
import pandas as pd
from datetime import datetime
from slash.generales import Generales
class Pets(commands.Cog, Generales):

    def acomodar_lista(self, lista, llave):
        acomodado = []
        for elemento in lista:
            if len(acomodado) == 0:
                acomodado.append(elemento)
            else:
                for i in range(len(acomodado)):
                    if elemento[llave] > acomodado[i][llave]:
                        acomodado.insert(i, elemento)
                        break
                    elif i == len(acomodado) - 1:
                        acomodado.append(elemento)
        return acomodado

    @cog_ext.cog_slash(name="pets", description="Muestra los pets", options = [
        create_option(
            name = 'username',
            description = 'Username',
            option_type = 3,
            required=False,
        ),
        create_option(
            name = 'perfil',
            description = 'Nombre del prefil',
            option_type = 3,
            required=False,
        )
    ])
    async def pets(self, msg: SlashContext, username: str = '', perfil: str = ''):
        self.config()
        uuid = ''
        if username == '':
            id = msg.author.id
            uuid = self.get_verify_user(id)
            username = self.get_username(uuid = uuid)
        if username == '':
            await msg.reply(f'Debes verificar antes la cuenta para poder usar el comando sin especificar username. Utiliza /verificar')
            return
        perfil_name = perfil
        original_msg = msg
        embeds_data = []
        pets_por_pagina = 10
        
        msg = await msg.reply("**Cargando...**")
        try:
            if uuid != '':
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True, uuid_key=uuid)
            else:
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        #open(f'./info_pruebas/{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return
        username = self.for_tsuru(username)

        # -------------- Verificcacion de la api de inventario ------------------
        try:
            pets = datos["pets"]
        except:
            return msg.reply(f'Revise que la API de inventario este activa')

        # -------------- Decodicicacion de datos ----------------
        # open pet_xp_levels.json
        pet_xp_levels = json.loads(open('./json/pet_xp_levels.json', 'r').read())
        pets_data = []
        for pet in pets:
            rareza = pet["tier"].lower()
            xp_pet = pet['exp']
            activo = pet['active']
            if xp_pet < 5000:
                nivel = 1
            else:
                nivel = 100
            candies = pet['candyUsed']
            skin = pet['skin']
            try:
                item = pet['heldItem'].lower().replace('_', ' ')
                item = item.replace('pet item ', '')
                item = item.replace('skill', 'exp')
                item = item.capitalize()
                emoji_item = self.get_emoji_name(item).replace(item, '')
            except:
                item = None
                emoji_item = ''
            for i in range(1, 100):
                if xp_pet >= pet_xp_levels[rareza.replace('mythic', 'legendary')][str(i)] and xp_pet < pet_xp_levels[rareza.replace('mythic', 'legendary')][str(i+1)]:
                    nivel = i
                    break
            try:
                next_level_xp = pet_xp_levels[rareza.replace('mythic', 'legendary')][str(nivel + 1)]
            except:
                next_level_xp = -1
            name = f'[Lvl {nivel}] ' + rareza.capitalize() + ' ' + pet["type"].lower().replace('_', ' ').capitalize() + ' Pet '
            if activo:
                name = self.get_emoji_name(f'_**`{name}`**_')  + ' ' + emoji_item
            else:
                name = self.get_emoji_name(f'{name}')  + ' ' + emoji_item
            
            pets_data.append({
                'nombre': name,
                'nivel': nivel,
                'activo': activo,
                'xp': xp_pet,
                'xp_para_siguiente_nivel': next_level_xp,
                'candies': candies,
                'skin': skin,
                'item': item
            })
        # -------------- Ordenacion de datos ----------------
        pet_activo = []
        pets_mythic = []
        pets_legendary = []
        pets_epic = []
        pets_rare = []
        pets_uncommon = []
        pets_common = []
        for i in range(len(pets_data)):
            pet = pets_data[i]
            if pet['activo']:
                pet_activo = [pets_data[i]]
                pets_data.pop(i)
                break
        
        for pet in pets_data:
            if 'mythic' in pet['nombre'].lower():
                pets_mythic.append(pet)
            elif 'legendary' in pet['nombre'].lower():
                pets_legendary.append(pet)
            elif 'epic' in pet['nombre'].lower():
                pets_epic.append(pet)
            elif 'rare' in pet['nombre'].lower():
                pets_rare.append(pet)
            elif 'uncommon' in pet['nombre'].lower():
                pets_uncommon.append(pet)
            else:
                pets_common.append(pet)
        
            # -------- Ordenando por nivel de alto a bajo --------

        pets_mythic = self.acomodar_lista(pets_mythic, 'nivel')
        pets_legendary = self.acomodar_lista(pets_legendary, 'nivel')
        pets_epic = self.acomodar_lista(pets_epic, 'nivel')
        pets_rare = self.acomodar_lista(pets_rare, 'nivel')
        pets_uncommon = self.acomodar_lista(pets_uncommon, 'nivel')
        pets_common = self.acomodar_lista(pets_common, 'nivel')

        pets_data = pet_activo + pets_mythic + pets_legendary + pets_epic + pets_rare + pets_uncommon + pets_common

        # -------------- Creacion de embed ----------------
        numero_de_pets = len(pets_data)
        mensajes = []
        numero_de_pet = 0
        numero_de_pagina = 1
        paginas = int(numero_de_pets / pets_por_pagina) + 1
        color = self.color_aleatorio()
        title = f'{username} {perfil_name}'
        url =  f'https://crafatar.com/renders/body/{uuid}?size=40'
        embed = discord.Embed(title=title, color=color)
        embed.set_thumbnail(url=url)
        drop_event = self.dropeo_hall(original_msg)
        aux = 1

        for_embed = {}
        for_embed['title'] = title
        for_embed['tumb'] = url
        for_embed['color'] = color
        for_embed['fields'] = []
        
        for i in range(numero_de_pets):
            pet = pets_data[i]
            name = f'{aux}.- {pet["nombre"]}'
            value = '```'
            if pet['activo']:
                value += f'Pet Activo\n'
            xp_actual = f'{pet["xp"]:,.0f}'
            
            if pet['xp_para_siguiente_nivel'] != -1:
                xp_siguiente = f'{pet["xp_para_siguiente_nivel"]:,.0f}'
                xp_faltante = f'{pet["xp_para_siguiente_nivel"] - pet["xp"]:,.0f}'
                value += f'XP: {xp_actual}/{xp_siguiente}\n'
                value += f'Falta: {xp_faltante} para el nivel {pet["nivel"] + 1}\n'
            else:
                value += f'XP: {xp_actual}\n'
                value += f'Pet Maxeada\n'
            if pet['candies'] != 0:
                value += f'Candies: {pet["candies"]}\n'
            if pet['skin'] != None:
                value += f'Skin: {pet["skin"]}\n'
            if pet['item'] != None:
                value += f'Item: {pet["item"]}\n'
            value += '```'
            embed.add_field(name=name, value=value, inline=False)
            for_embed['fields'].append([name, value, False])
            aux += 1
            if numero_de_pet + 1 == pets_por_pagina:
                mensajes.append(embed)
                embeds_data.append(for_embed)
                numero_de_pet = 0
                numero_de_pagina += 1
                embed = discord.Embed(title=title, color=color)
                embed.set_thumbnail(url=url)
                for_embed = {}
                for_embed['title'] = title
                for_embed['tumb'] = url
                for_embed['color'] = color
                for_embed['fields'] = []
            numero_de_pet += 1
        if numero_de_pet != 1:
            mensajes.append(embed)
            embeds_data.append(for_embed)
        
        for i in range(len(mensajes)):
            text = f'Pagina {i + 1}/{len(mensajes)}'
            if drop_event[0]: text += f'{drop_event[1]}'
            mensajes[i].set_footer(text=text)
            embeds_data[i]['footer'] = text
        await msg.edit(content = '', embed = mensajes[0])
        user_id = original_msg.author.id
        id_mensaje = msg.id
        guardar = {
            'msg_id': id_mensaje,
            'user_id': user_id,
            'embeds': embeds_data,
        }
        open(f'./embeds_data/emb_data.json', 'w').write(json.dumps(guardar, indent=4))
        await msg.channel.send(f'+load {id_mensaje}')
        await msg.add_reaction('\U000025B6')

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Pets(bot))
