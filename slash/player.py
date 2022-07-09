import json
import pandas as pd
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

class Player(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
        
    def user_data(self, user_data, username, profile, uuid):
        for_embed = {}
        try:
            rango = user_data['newPackageRank']
            rango = rango.replace('_', '').replace('PLUS', '+')
            rango = f'`{rango}`'
        except:
            rango = ''
        title = f'User: {username} {rango}'
        description = f'Ultimo perfil activo: {profile}'
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        for_embed['title'] = title
        for_embed['description'] = description
        for_embed['tumb'] = url
        for_embed['fields'] = []
        
        ingresos = False
        alias_conocidos = True
        perfiles = True
        social_media = True
        
        if ingresos:
            name = f'Ingresos:'
            first_login = user_data['firstLogin']
            last_login = user_data['lastLogin']
            first_login = self.obtener_tiempo_relativo(first_login)
            last_login = self.obtener_tiempo_relativo(last_login)
            first_login = first_login.replace('-', '')
            last_login = last_login.replace('-', '')
            value = ''
            value += f'\nPrimer ingreso hace: {first_login}\n'
            value += f'\nUltimo ingreso hace: {last_login}\n'
            
            for_embed['fields'].append([name, value, False])
        
        if alias_conocidos:
            name = 'Alias conocidos:\n'
            value = ''
            aliases = user_data['knownAliases']
            for alias in aliases:
                value += f'{alias}\n'
                
            for_embed['fields'].append([name, value, False])
        
        if perfiles:
            name = 'Perfiles:\n'
            value = ''
            perfiles = user_data['stats']['SkyBlock']['profiles']
            profiles = []
            link_base_player = 'https://api.hypixel.net/skyblock/profile'
            primero = f'{link_base_player}?key='
            for key in perfiles:
                perfil = perfiles[key]
                profile_name = perfil['cute_name']
                profile_id = perfil['profile_id']
                segundo = f'&profile={profile_id}'
                player = self.consulta(primero, segundo)
                try:
                    modo = player['profile']['game_mode']
                    modo = modo.title()
                except:
                    modo = ''
                players = len(player['profile']['members'])
                if players > 1:
                    if modo != '':
                        modo = f'co-op {players} players, {modo}'
                    else:
                        modo = f'co-op {players} players'
                if modo != '':
                    modo = f': `{modo}`'
                profile_name = f'{profile_name}{modo}'
                profiles.append(profile_name)
            for profile in profiles:
                value += f'{profile}\n'
                
            for_embed['fields'].append([name, value, False])
        
        if social_media:
            name = 'Social media:\n'
            value = ''
            try:
                links = user_data['socialMedia']['links']
                for link in links:
                    value += f'{link.title()}: {links[link]}\n'
            except:
                value += 'Sin cuentas vinculadas\n'
                
            for_embed['fields'].append([name, value, False])
        
        return for_embed
    
    @cog_ext.cog_slash(name="player", description="Muestra la informacion de un usuario", options=[
        create_option(
            name = 'username',
            description = 'Username',
            option_type = 3,
            required=False
        )
    ])
    async def player(self, msg: SlashContext, username: str = ''):
        self.config()
        uuid = ''
        if username == '':
            id = msg.author.id
            uuid = self.get_verify_user(id)
            username = self.get_username(uuid = uuid)
        if username == '':
            await msg.reply(f'Debes verificar antes la cuenta para poder usar el comando sin especificar username. Utiliza /verificar')
            return
        #perfil_name = 'Raspberry'
        perfil_name = ''
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
        
        base = 'https://api.hypixel.net/player'
        base += '?key='
        segundo = f'&uuid={uuid}'
        user_data = self.consulta(base, segundo)
        user_data = user_data['player']
        
        embeds_data = []
        for_embed = self.user_data(user_data, username, perfil_name, uuid)
        embeds_data.append(for_embed)
        embeds = do_embed(embeds_data)
        await msg.edit(content = '', embed = embeds[0])
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Player(bot))