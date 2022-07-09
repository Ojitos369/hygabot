import json
import pandas as pd
import discord
import random
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from os import sys
from time import sleep
from slash.generales import Generales, Item

class Basicos(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    last_ah_update = ''
    auction_items = [{} for i in range(100)]
    fecha_de_actualizacion = ''
    
    # ----------- COMANDO HOLA -----------
    @cog_ext.cog_slash(name="hola", description="Se educado y saluda")
    async def hola(self, msg: SlashContext):
        user = ' ' + msg.author.mention + ' '
        emojis = []
        emojis.append('👋 ')
        emojis.append('🤝 ')
        emojis.append(':grin: ')
        emojis.append('<:unperro2:897500510083502150> ')
        emojis.append('<:Holaaaa:873365207731298304> ')
        emojis.append('<:rosa:879479778506317895> ')
        inicios = []
        inicios.append('Hola')
        inicios.append('Hi')
        inicios.append('Hey')
        inicios.append('Que tal')
        inicios.append('Buen dia')
        extras = []
        extras.append(f'Como te encuentras hoy?')
        extras.append(f'Todo va bien?')
        extras.append(f'Que tal?')
        extras.append(f'Ten un gran dia :3')
        extras.append(f'Ya comiste?')
        saludo = random.choice(inicios)
        extra = random.choice(extras)
        emoji = random.choice(emojis)
        saludo = saludo + user + emoji + extra
        await msg.reply(saludo)
    
    # ----------- COMANDO ADIOS -----------
    @cog_ext.cog_slash(name="adios", description="Se educado y despidete")
    async def adios(self, msg: SlashContext):
        user = ' ' + msg.author.mention + ' '
        emojis = []
        emojis.append('👋 ')
        emojis.append(':smiling_face_with_3_hearts: ')
        emojis.append(':grin: ')
        emojis.append('<:unperro2:897500510083502150> ')
        emojis.append('<:rosa:879479778506317895> ')
        inicios = []
        inicios.append('Adios')
        inicios.append('Bye')
        inicios.append('Hasta luego')
        inicios.append('Nos leemos luego')
        extras = []
        extras.append(f'Cuidate mucho')
        extras.append(f'Descansar es bueno')
        extras.append(f'Te estare esperando')
        extras.append(f'Ten un gran dia :3')
        mensaje = random.choice(inicios)
        extra = random.choice(extras)
        emoji = random.choice(emojis)
        mensaje = mensaje + user + emoji + extra
        await msg.reply(mensaje)
    
    # ----------- COMANDO PING -----------
    @cog_ext.cog_slash(name="ping", description="Comando para ver el ping del bot")
    async def ping(self, msg: SlashContext):
        await msg.reply(f'Latencia: {round(self.bot.latency * 1000)}ms')

    # ----------- COMANDO OPERACION -----------
    @cog_ext.cog_slash(name="operacion", description="Realiza operaciones: + , - , * , /, ()", options = [
        create_option(
            name = 'operacion',
            description = 'Operacion a realizar',
            option_type = 3,
            required=True,
        )
    ])
    async def operacion(self, msg: SlashContext, operacion: str):
        remplazos = {
            'k': ' * 1000',
            'm': ' * 1000000',
            'b': ' * 1000000000'
        }
        op_original = operacion
        operacion = operacion.lower()
        for key, value in remplazos.items():
            operacion = operacion.replace(key, value)
        text = operacion
        try:
            resultado = eval(text)
        except:
            await msg.reply('No se pudo realizar la operacion')
            return
        letra = self.redondear_letras(float(resultado))
        resultado = '{:,.2f}'.format(float(resultado)) + f' ({letra})'
        color = self.color_aleatorio()
        embed = discord.Embed(title=f'{op_original}', description=f'Resultado: {resultado}', color = color)
        await msg.reply(embed=embed)

    # ----------- COMANDO LIMPIAR -----------
    @cog_ext.cog_slash(name="limpiar", description="Muestra tiempo sin conectarse", options = [
        create_option(
            name = 'guild',
            description = 'Nombre de la guild',
            option_type = 3,
            required=True,
        ),
        create_option(
            name = 'dias',
            description = 'Dias sin conectarse',
            option_type = 4,
            required=True,
        )
    ])
    async def limpiar(self, msg: SlashContext, guild: str, dias: int):
        self.config()
        admin = msg.author.guild_permissions.administrator
        if not admin:
            await msg.reply('No tienes permisos para usar este comando')
            return
        ahora = datetime.strptime(datetime.now().strftime('%d-%m-%Y %H:%M:%S'), '%d-%m-%Y %H:%M:%S')
        link_base_player = 'https://api.hypixel.net/player'
        link_base = 'https://api.hypixel.net/guild'
        inicio = f'{link_base}?key='
        fin = f'&name={guild}'
        hydata = self.consulta(inicio, fin)
        metrica = hydata['guild']
        cantidad = 0
        color = self.color_aleatorio()
        embed = discord.Embed(title=f'Limpiando {guild} el {ahora}', description=f'Limpieza de {dias} dias', color = color)
        miembro_cantidad = 0
        puntos = 2
        mensaje_temporal = await msg.reply('Cargando' + str('.' * puntos))
        for miembro in metrica['members']:
            total = 0
            for valor in miembro['expHistory'].values():
                total += float(valor)
            uuid = miembro["uuid"]
            primero = f'{link_base_player}?key='
            segundo = f'&uuid={uuid}'
            player = self.consulta(primero, segundo)
            try:
                fecha = int(player['player']['lastLogin'])
                ultima_conexion = self.obtener_tiempo_relativo(fecha)
                offline_days = abs(int(ultima_conexion.split(' ')[0]))
                if offline_days >= dias:
                    cantidad += 1
                    value = '```'
                    value += f'Rank: {miembro["rank"]}\n'
                    value += f'Tiempo sin conectarse: {str(self.obtener_tiempo_relativo(fecha)).replace("-", "")}\n'
                    value += '```'
                    embed.add_field(name=f'\n{cantidad}.- Player: {player["player"]["displayname"]}', value=value, inline = False)
                    #print(f'en {cantidad} {miembro_cantidad}/{largo_metrica}')
            except:
                pass
            miembro_cantidad += 1
            #puntos += 1
            #await mensaje_temporal.edit(content='Cargando' + str('.' * puntos))
            #if puntos == 5:
            #    puntos = 0
        embed.set_footer(text = f'{cantidad} Miembros sin conectarse en los ultimos {dias} dias')
        await mensaje_temporal.edit(content = '', embed=embed)

    # ----------- COMANDO INVITAR -----------
    @cog_ext.cog_slash(name="invitar", description="Invitame a tu server :3")
    async def invitar(self, msg: SlashContext):
        link = 'https://discord.com/oauth2/authorize?client_id=876992671284076546&permissions=8&scope=bot%20applications.commands'
        yt = 'https://www.youtube.com/channel/UCt8_k3luF9gAek76rgjv4CA'
        dc = 'https://discord.gg/GvpR7tdmfW'
        componentes = [
            {
                "type": 1,
                "components": [
                        {
                            "type": 2,
                            "label": "Invitame",
                            "url": link,
                            "style": 5,
                            "emoji": {
                                "name": "unperro2",
                                "id": 897500510083502150,
                            }
                        }
                ]
            }
        ]
        color = self.color_aleatorio()
        description = f'Gracias por invitar.'# Te Invitamos a seguirnos tambien en: '
        title = f'HygaBot'
        embed = discord.Embed(title=title, description=description, color = color, url = link)

        title = f'Invite HygaBot'
        description = f'[Bot]({link})'
        embed.add_field(name=title, value=description, inline = False)

        title = f'YouTube GDGABO97'
        description = f'[YouTube]({yt})'
        #embed.add_field(name=title, value=description, inline = False)

        gabo_server_id = 831264016101802064
        guild = self.bot.get_guild(gabo_server_id)
        if guild == None:
            guild = "GDEGABO97 Discord"
        title = f"{guild}"
        description = f'[Discord]({dc})'
        #embed.add_field(name=title, value=description, inline = False)
        filename = 'hygabot.png'
        file_path = f"./img/{filename}"
        file = discord.File(file_path, filename=filename)
        img_url = f"attachment://{filename}"
        embed.set_image(url=img_url)
        await msg.reply(content = '', file = file, embed = embed, components=componentes)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Basicos(bot))