import os
import ast
import json
import platform
import random
from datetime import datetime
from time import sleep
from os import system
import discord
from multiprocessing import Process
from do_embeds import do_embed
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from funciones.generales import Full
from funciones.funciones import importar_funciones
from slash.generales import Generales
from discord import *
from discord.ext import *
from discord_components import *
from discord.utils import get
from slash.pruebas import Prueba

RUN_PROD_MODE = True if str(os.environ.get('RUN_PROD_MODE', True)).title() == 'True' else False
# clear screen on linux or windows
if platform.system() == 'Windows':
    system('cls')
else:
    system('clear')

HYPIXEL_APIS = ast.literal_eval(os.environ.get('HYPIXEL_APIS', '[]'))

# ---------- Variables ----------
if RUN_PROD_MODE:
    bot = os.environ.get('HYGABOT_TOKEN_PROD')
    bot_n = 0
else:
    bot = os.environ.get('HYGABOT_TOKEN_DEV')
    bot_n = 1
# open json
with open('./json/datos.json') as datos:
    datos = json.load(datos)
coleccion = []
mantenimiento = False
responder_mantenimiento = False
o_3695 = 885643862008270858
o_369 = 673397248427556887
developers_ids = [o_369, o_3695]
key = bot
actions = importar_funciones()
full_functions = Full()
intents = discord.Intents.default()
intents.members = True
intents = Intents.all()
prefijo = datos["prefijo"][bot_n]
largo_prefijo = len(prefijo)
#client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
client = commands.Bot(command_prefix=commands.when_mentioned_or(prefijo), intents=intents)
slash = SlashCommand(client, sync_commands=True)
mensajes_coleccion = {}
comandos_coleccion = {}
procesos_activos = []
generales = Generales()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"/help"))
    print('Activo como {0.user}'.format(client))

# ------ Normales ------
client.load_extension("slash.basic")
client.load_extension("slash.slayers")
client.load_extension("slash.hotm")
client.load_extension("slash.help")
client.load_extension("slash.bazar")
client.load_extension("slash.forge")
client.load_extension("slash.pets")
client.load_extension("slash.inventarios")
client.load_extension("slash.ender_chest")
client.load_extension("slash.wardrobe")
client.load_extension("slash.talismanes")
client.load_extension("slash.escencias")
client.load_extension("slash.ah_player")
client.load_extension("slash.novedades")
client.load_extension("slash.backpack")
client.load_extension("slash.buscar_inv")
client.load_extension("slash.kills")
client.load_extension("slash.skills")
client.load_extension("slash.verify")
client.load_extension("slash.items")
client.load_extension("slash.reforges")
client.load_extension("slash.auction_house")
client.load_extension("slash.buscarguild")
client.load_extension("slash.sug_bug")
client.load_extension("slash.player")
client.load_extension("slash.year_2022")
#client.load_extension("slash.pruebas")

@client.event
async def enviar_embeds(res = ''):
    if isinstance(res, type({})):
        msg = res["msg"]
        resultado = res["respuesta"]
        original = res["original"]

    if isinstance(resultado, type([])):
        try:
            mensaje_data = await msg.edit(embed = resultado[0])
        except:
            await resultado[0]
            return
        comando = original.content.lower()[:5]
        codigo_temp = f'{comando}_{original.author.id}'
        if codigo_temp in comandos_coleccion:
            anterior_id = comandos_coleccion[codigo_temp]
            del mensajes_coleccion[anterior_id]
        mensajes_coleccion[mensaje_data.id] = {
            'msg': msg,
            'data': mensaje_data,
            'respuestas': resultado,
            'respondida': 0,
            'user': original.author.id,
            'channel': original.channel.id,
            'file': None,
            'page_file': 0
        }
        comandos_coleccion[codigo_temp] = mensaje_data.id
        if len(resultado) > 1:
            #await mensaje_data.add_reaction('\U000025C0')
            await mensaje_data.add_reaction('\U000025B6')

@client.event
async def on_message(msg):
    global mantenimiento
    global responder_mantenimiento
    global comandos_coleccion
    
    if msg.author == client.user:
        if '+load' in msg.content.lower():
            msg_id = msg.content.lower().split(' ')[1]
            try:
                await msg.delete()
            except:
                pass
            with open(f'./embeds_data/emb_data.json') as datos:
                embeds_data = json.load(datos)
            embeds = do_embed(embeds_data['embeds'])
            open(f'./embeds_data/emb_data.json', 'w').write(json.dumps({}, indent=4))
            user_id = embeds_data["user_id"]
            if user_id in comandos_coleccion:
                del mensajes_coleccion[user_id]
            files = {}
            if 'files' in embeds_data:
                file = embeds_data['files']
                for key in file:
                    files[key] = file[key]
            mensajes_coleccion[user_id] = {
                'respuestas': embeds,
                'respondida': 0,
                'user': user_id,
                'msg_id': msg_id,
                'file': files,
                'page_file': 0
            }
            #await mensaje_data.add_reaction('\U000025C0')
            #await mensaje_data.add_reaction('\U000025B6')
        return

    if msg.author.bot:
        return
    guild = msg.guild
    
    # Chequeo continuo
    await generales.not_spam(msg, client)
    await generales.get_guilds_names(client)
    
    if guild == None:
        await msg.channel.send(f"{msg.author.mention} Te invitamos a unirte al server para poder platicar :D")
        await actions[0].invitar(msg, 'text')
        return

    if msg.content.lower() == 'pru':
        #prueba = Prueba(bot)
        #await prueba.pruebas(msg)
        pass
    
    if str(msg.content).split()[0] != prefijo:
        text = str(msg.content)[:(largo_prefijo)] + ' ' + str(msg.content)[(largo_prefijo):]
    else:
        text = msg.content
    text = text.replace('   ', '  ').replace('  ', ' ')

    # Funcionamieneto principal de mensaje
    if text.split()[0] == prefijo:
        if text == f'{prefijo} mantenimiento' and msg.author.id in developers_ids:
            mantenimiento = True
            responder_mantenimiento = True
            await msg.channel.send(f"Mantenimiento activado")
            return

        if mantenimiento:
            if msg.author.id not in developers_ids:
                if responder_mantenimiento:
                    await msg.reply("Estoy en mantenimiento. Regreso pronto")
                return
            if msg.author.id in developers_ids and text == f'{prefijo} reactivar':
                mantenimiento = False
                await msg.reply("Mantenimiento desactivado")
                return
        
        channel_sugerencias_id = '882986881120362527'
        channel_comandos_id = '882987518520352808'
        user = await client.fetch_channel(channel_sugerencias_id)
        
        resultado = full_functions.execute(msg, text, actions, prefijo, user)
        file = None
        pagina = 0
        if isinstance(resultado, type({})):
            try:
                if 'borrar' in resultado:
                    await msg.delete()
            except:
                pass
            #try:
            if 'not_embed' in resultado:
                for res in resultado['respuesta']:
                    await res
                return
            if 'file' in resultado:
                file = resultado['file']
                pagina = resultado['pagina']
            resultado = resultado['respuesta']
        if isinstance(resultado, type([])):
            especial_embed = False
            resultado_es = None
            if isinstance(resultado[len(resultado)-1], type([])):
                especial_embed = True
                resultado_es = resultado.pop(len(resultado)-1)
                resultado_es = resultado_es[1]
                print(resultado_es)
            try:
                if file != None:
                    if pagina == 0:
                        mensaje_data = await msg.reply(file=file, embed = resultado[0])
                    else:
                        mensaje_data = await msg.reply(embed = resultado[0])
                else:
                    mensaje_data = await msg.reply(embed = resultado[0])
            except:
                mensaje_data = await resultado[0]
            user_id = msg.author.id
            if user_id in comandos_coleccion:
                del mensajes_coleccion[user_id]
            mensajes_coleccion[user_id] = {
                'respuestas': resultado,
                'respondida': 0,
                'user': user_id,
                'msg_id': str(mensaje_data.id),
                'file': file,
                'page_file': pagina
            }
            if len(resultado) > 1:
                #await mensaje_data.add_reaction('\U000025C0')
                await mensaje_data.add_reaction('\U000025B6')
            
            if especial_embed:
                await msg.reply(resultado_es)
        else:
            await resultado
        #system("clear")

        mensaje = [text.replace(f'{prefijo} ', f'{prefijo}'),
        msg.author,
        msg.guild,
        msg.channel,
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
        coleccion.append(mensaje)

        color = actions[0].color_aleatorio()
        title = f'Autor: {mensaje[1]}'
        description = f'Comando: {mensaje[0]}\n'
        description += f'Guild: {mensaje[2]}\n'
        description += f'Channel: {mensaje[3]}\n'
        embed = discord.Embed(title = title, description = description, color = color)
        footer = f'Fecha: {mensaje[4]}'
        embed.set_footer(text=footer)

        aux = 1
        print()
        print('-'*100)
        for mensaje in coleccion:
            print(f'{aux}.- {mensaje[0]}\t : \t {mensaje[1]} \t:\t {mensaje[4]}')
            aux += 1
        print('-'*100)
        print()
            
        if bot == 0 and msg.author.id not in developers_ids:
            user = await client.fetch_channel(channel_comandos_id)
            await user.send(embed=embed)

@client.event
async def on_member_join(member):
    await generales.bienvenida(member, client)

@client.event
async def on_reaction_add(reaction, user):
    global comandos_coleccion
    if user != client.user:
        mesagge_id = str(reaction.message.id)
        user_id = user.id
        if user_id not in mensajes_coleccion and user_id in generales.developers_ids:
            for_beta = True
            for mensaje in coleccion:
                msg_id = mensajes_coleccion[mensaje]['msg_id']
                if str(msg_id) == str(mesagge_id):
                    user_id = mensaje
                    break
            
        if user_id in mensajes_coleccion:
            msg_id = mensajes_coleccion[user_id]['msg_id']
            if mesagge_id == msg_id:
                data = reaction.message
                respuestas = mensajes_coleccion[user_id]['respuestas']
                respondida = mensajes_coleccion[user_id]['respondida']
                files = mensajes_coleccion[user_id]['file']
                ultima_page = len(respuestas) - 1
                if reaction.emoji == '\U000025B6':
                    respondida += 1
                elif reaction.emoji == '\U000025C0':
                    respondida -= 1
                elif reaction.emoji == '⏩':
                    respondida = ultima_page
                elif reaction.emoji == '⏪':
                    respondida = 0


                intentando = True
                while intentando:
                    try:
                        if str(respondida) in files:
                            file = discord.File(files[str(respondida)][0], filename=files[str(respondida)][1])
                            channel = data.channel
                            await data.delete()
                            data = await channel.send(file = file, embed = respuestas[respondida])
                            mensajes_coleccion[user_id]['msg_id'] = str(data.id)

                        else:
                            await data.edit(file = None, embed = respuestas[respondida])
                        mensajes_coleccion[user_id]['respondida'] = respondida
                        await data.clear_reactions()
                        if respondida != 0 and respondida != 1:
                            await data.add_reaction('⏪')
                        if respondida > 0:
                            await data.add_reaction('\U000025C0')
                        if respondida < len(respuestas) - 1:
                            await data.add_reaction('\U000025B6')
                        if respondida != ultima_page and respondida != len(respuestas) - 2:
                            await data.add_reaction('⏩')
                        intentando = False
                    except:
                        sleep(1)

client.run(key)


# Nacimiento del bot
# 17 Agosto 2021 