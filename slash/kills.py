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
from slash.generales import Generales

class Kills(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot

    def ordenar_dic(self, dic):
        i = 0
        ordenado = {}
        dic_aux = {}
        ordenando = []
        for item in dic:
            dic_aux[item] = {}
            dic_aux[item]['nombre'] = item
            dic_aux[item]['cantidad'] = dic[item]           
            dic_aux[item]['posicion'] = i
            i += 1

        for item in dic_aux:
            if len(ordenando) == 0:
                ordenando.append(dic_aux[item])
            else:
                for i in range(len(ordenando)):
                    if dic_aux[item]['cantidad'] > ordenando[i]['cantidad']:
                        ordenando.insert(i, dic_aux[item])
                        break
                    elif i == len(ordenando) - 1:
                        ordenando.append(dic_aux[item])
                        break
        for item in ordenando:
            ordenado[item['nombre']] = item['cantidad']
        
        return ordenado

    
    @cog_ext.cog_slash(name="kills", description="description", options=[
        create_option(
            name = 'username',
            description = 'Username',
            option_type = 3,
            required=False,
        ),
        create_option(
            name = 'filtro',
            description = 'Filtro de mobs a buscar',
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
    async def kills(self, msg: SlashContext, username: str = '', filtro: str = '*', perfil: str = ''):
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
        msg = await msg.reply("***Cargando...***")
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
        kills = {}
        for dato in datos['stats']:
            if dato.startswith('kills_'):
                key = dato.replace('kills_', '')
                kills[key] = datos['stats'][dato]
        
        filtro_separado = filtro.split(' ')

        # ------------- Buscando -----------------
        datos = {}

        for mob in kills:
            encontrado = True
            for palabra in filtro_separado:
                if palabra not in mob.replace('_', ' ').lower():
                    encontrado = False
            if filtro == '*':
                encontrado = True
            if encontrado:
                datos[mob] = int(kills[mob])
        
        # ------------ Order by cantidad -----------
        datos = self.ordenar_dic(datos)
        
        # ------------- Embeds -----------------
        embeds_data = []
        embeds = []
        color = self.color_aleatorio()
        title = title = f'Kills de {username} en {perfil_name}'
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        description = ''
        mob_en_pagina = 1
        for mob in datos:
            mob_name = mob.replace('_', ' ').title()
            cantidad = datos[mob]
            if cantidad > 1000:
                cantidad_letras = self.calculadora(f'{cantidad} + 0', letras = True)
                description += f'\n**{mob_name}**: ' + '{:,.0f}'.format(float(cantidad)) + f' ({cantidad_letras})\n'
            else:
                description += f'\n**{mob_name}**: {cantidad}\n'
            if mob_en_pagina == 10:
                embed = discord.Embed(title=title, description=description, color=color, url=url)
                embed.set_thumbnail(url=url)
                embeds.append(embed)
                for_embed = {}
                for_embed['color'] = color
                for_embed['title'] = title
                for_embed['tumb'] = url
                for_embed['description'] = description
                embeds_data.append(for_embed)
                description = ''
                mob_en_pagina = 0
            mob_en_pagina += 1

        if description != '':
            embed = discord.Embed(title=title, description=description, color=color, url=url)
            embed.set_thumbnail(url=url)
            embeds.append(embed)
            for_embed = {}
            for_embed['color'] = color
            for_embed['title'] = title
            for_embed['tumb'] = url
            for_embed['description'] = description
            embeds_data.append(for_embed)
        
        pagina = len(embeds)
        for i in range(pagina):
            text = f'Pagina {i+1}/{pagina}'
            embeds[i].set_footer(text=text)
            embeds_data[i]['footer'] = text
        if pagina == 0:
            await msg.edit(content = 'No se encontraron mobs con este nombre')
            return
        await msg.edit(content = '', embed = embeds[0])
        user_id = original_msg.author.id
        id_mensaje = msg.id
        guardar = {
            'msg_id': id_mensaje,
            'user_id': user_id,
            'embeds': embeds_data,
        }
        open(f'./embeds_data/emb_data.json', 'w').write(json.dumps(guardar, indent=4))
        await msg.channel.send(f'+load {id_mensaje}')
        if pagina > 1:
            await msg.add_reaction('\U000025B6')
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Kills(bot))