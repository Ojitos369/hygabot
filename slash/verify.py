import json
import pandas as pd
import discord
from mojang import MojangAPI
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from os import sys
from time import sleep
from slash.generales import Generales

class Verificar(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="verificar", description="Asocia tu cuenta de hypixel con la de discord para comandos mas rapidos", options=[
        create_option(
            name = 'username',
            description = 'Username',
            option_type = 3,
            required=True,
        )
    ])
    async def verificar(self, msg: SlashContext, username: str):
        self.config()
        perfil_name = ''
        original_msg = msg
        msg = await msg.reply("***Cargando...***")
        
        uuid = MojangAPI.get_uuid(username)
        link_base_player = 'https://api.hypixel.net/player'
        primero = f'{link_base_player}?key='
        segundo = f'&uuid={uuid}'
        player = self.consulta(primero, segundo)
        try:
            username = player['player']['displayname']
        except:
            await msg.edit(content=f'Verifica que el usuario ***`{username}`*** este bien escrito')
            return

        user_tag = original_msg.author
        user_verify = ''
        try:
            user_verify = player['player']['socialMedia']['links']['DISCORD']
        except:
            pass
        user_tag = str(user_tag)
        user_verify = str(user_verify)
        id = original_msg.author.id
        title = f'Verificando con {username}'
        verificado = False
        if user_tag != user_verify:
            color = discord.Color.from_rgb(255, 0, 0)
            description = f'No se puede verificar a <@!{id}> con ***`{username}`***\n\n Utiliza **`/guiaverificar`** Para vincular tu cuenta de discord con hypixel'
        else:
            color = discord.Color.from_rgb(0, 255, 0)
            description = f'Verificado <@!{id}> como ***`{username}`***'
            verificado = True
        if verificado:
            try:
                query = f"INSERT INTO verificados  (id, username, uuid) VALUES ('{id}', '{username}', '{uuid}')"
                self.query_ejecutar(query)
            except:
                query = f"UPDATE verificados SET username = '{username}' WHERE id = '{id}'"
                self.query_ejecutar(query)
        
        embed = discord.Embed(title=title, description=description, color=color)
        await msg.edit(content = '', embed=embed)
        return

    @cog_ext.cog_slash(name="guiaverificar", description="Muestra la guia para la verificacion de hypixel")
    async def guia_verificar(self, msg: SlashContext):
        original_msg = msg
        msg = await msg.reply('***Cargando...***')
        embeds = []
        embed_data = []
        files = {}
        color = self.color_aleatorio()
        title = 'Sincronizacion de hypixel con discord'

        descriptions = []
        file_names = []
        descriptions.append('**Paso 1**\nEn el lobby de hypixel usa click derecho con el segundo item en mano')
        file_names.append("verify_0.png")

        descriptions.append('**Paso 2**\nEl click debe ser con el menu cerrado')
        file_names.append("verify_1.png")

        descriptions.append('**Paso 3**\nAparecera un menu. Seleccionar la opcion de ***`"Social Media"`***')
        file_names.append("verify_2.png")

        descriptions.append('**Paso 4**\nEn las opciones que aparecen seleccione ***`"Discord"`***')
        file_names.append("verify_3.png")

        descriptions.append('**Paso 5**\nDebe aparecer un mensaje indicando que pegues tu usuario de discord en el chat')
        file_names.append("verify_4.png")

        descriptions.append('**Paso 6**\nDebe estar en el canal general (/chat a). Pegue su usuario de discord incluyendo los numeros despues del numeral (username#0000)')
        file_names.append("verify_5.png")

        descriptions.append('**Paso 7**\nSi se realizo correctamente debe salir un mensaje indicando que se realizo el link con exito')
        file_names.append("verify_6.png")

        paginas_totales = len(descriptions)
        for i in range(paginas_totales):
            description = descriptions[i]
            embed = discord.Embed(title=title, description=description, color=color)
            filename  = file_names[i]
            file_path = f"./img/{filename}"
            file = discord.File(file_path, filename=filename)
            files[str(i)] = [file_path, filename]
            img_url = f"attachment://{filename}"
            embed.set_image(url=img_url)
            text = f'Pagina {i+1} de {paginas_totales}'
            embed.set_footer(text=text)
            for_embed = {}
            for_embed['color'] = color
            for_embed['title'] = title
            for_embed['description'] = description
            for_embed['image'] = img_url
            for_embed['footer'] = text
            embed_data.append(for_embed)
            embeds.append(embed)

        filename = file_names[0]
        file_path = f"./img/{filename}"
        file = discord.File(file_path, filename=filename)
        await msg.delete()
        msg = await original_msg.channel.send(content = '', file=file, embed=embeds[0])
        user_id = original_msg.author.id
        id_mensaje = msg.id
        guardar = {
            'msg_id': id_mensaje,
            'user_id': user_id,
            'embeds': embed_data,
            'files': files,
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
    bot.add_cog(Verificar(bot))