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
from slash.generales import Generales, Item

class Skills(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    xp_per_level = {
        0: {'requerida': 0, 'acumulada': 0},
        1: {'requerida': 50, 'acumulada': 50},
        2: {'requerida': 125, 'acumulada': 175},
        3: {'requerida': 200, 'acumulada': 375},
        4: {'requerida': 300, 'acumulada': 675},
        5: {'requerida': 500, 'acumulada': 1175},
        6: {'requerida': 750, 'acumulada': 1925},
        7: {'requerida': 1000, 'acumulada': 2925},
        8: {'requerida': 1500, 'acumulada': 4425},
        9: {'requerida': 2000, 'acumulada': 6425},
        10: {'requerida': 3500, 'acumulada': 9925},
        11: {'requerida': 5000, 'acumulada': 14925},
        12: {'requerida': 7500, 'acumulada': 22425},
        13: {'requerida': 10000, 'acumulada': 32425},
        14: {'requerida': 15000, 'acumulada': 47425},
        15: {'requerida': 20000, 'acumulada': 67425},
        16: {'requerida': 30000, 'acumulada': 97425},
        17: {'requerida': 50000, 'acumulada': 147425},
        18: {'requerida': 75000, 'acumulada': 222425},
        19: {'requerida': 100000, 'acumulada': 322425},
        20: {'requerida': 200000, 'acumulada': 522425},
        21: {'requerida': 300000, 'acumulada': 822425},
        22: {'requerida': 400000, 'acumulada': 1222425},
        23: {'requerida': 500000, 'acumulada': 1722425},
        24: {'requerida': 600000, 'acumulada': 2322425},
        25: {'requerida': 700000, 'acumulada': 3022425},
        26: {'requerida': 800000, 'acumulada': 3822425},
        27: {'requerida': 900000, 'acumulada': 4722425},
        28: {'requerida': 1000000, 'acumulada': 5722425},
        29: {'requerida': 1100000, 'acumulada': 6822425},
        30: {'requerida': 1200000, 'acumulada': 8022425},
        31: {'requerida': 1300000, 'acumulada': 9322425},
        32: {'requerida': 1400000, 'acumulada': 10722425},
        33: {'requerida': 1500000, 'acumulada': 12222425},
        34: {'requerida': 1600000, 'acumulada': 13822425},
        35: {'requerida': 1700000, 'acumulada': 15522425},
        36: {'requerida': 1800000, 'acumulada': 17322425},
        37: {'requerida': 1900000, 'acumulada': 19222425},
        38: {'requerida': 2000000, 'acumulada': 21222425},
        39: {'requerida': 2100000, 'acumulada': 23322425},
        40: {'requerida': 2200000, 'acumulada': 25522425},
        41: {'requerida': 2300000, 'acumulada': 27822425},
        42: {'requerida': 2400000, 'acumulada': 30222425},
        43: {'requerida': 2500000, 'acumulada': 32722425},
        44: {'requerida': 2600000, 'acumulada': 35322425},
        45: {'requerida': 2750000, 'acumulada': 38072425},
        46: {'requerida': 2900000, 'acumulada': 40972425},
        47: {'requerida': 3100000, 'acumulada': 44072425},
        48: {'requerida': 3400000, 'acumulada': 47472425},
        49: {'requerida': 3700000, 'acumulada': 51172425},
        50: {'requerida': 4000000, 'acumulada': 55172425},
        51: {'requerida': 4300000, 'acumulada': 59472425},
        52: {'requerida': 4600000, 'acumulada': 64072425},
        53: {'requerida': 4900000, 'acumulada': 68972425},
        54: {'requerida': 5200000, 'acumulada': 74172425},
        55: {'requerida': 5500000, 'acumulada': 79672425},
        56: {'requerida': 5800000, 'acumulada': 85472425},
        57: {'requerida': 6100000, 'acumulada': 91572425},
        58: {'requerida': 6400000, 'acumulada': 97972425},
        59: {'requerida': 6700000, 'acumulada': 104672425},
        60: {'requerida': 7000000, 'acumulada': 111672425},
    }
    xp_per_level_runecrafting = {
        0:{'requerida':	0, 'acumulada':	0},
        1:{'requerida':	50, 'acumulada':	50},
        2:{'requerida':	100, 'acumulada':	150},
        3:{'requerida':	125, 'acumulada':	275},
        4:{'requerida':	160, 'acumulada':	435},
        5:{'requerida':	200, 'acumulada':	635},
        6:{'requerida':	250, 'acumulada':	885},
        7:{'requerida':	315, 'acumulada':	1200},
        8:{'requerida':	400, 'acumulada':	1600},
        9:{'requerida':	500, 'acumulada':	2100},
        10:{'requerida':	625, 'acumulada':	2725},
        11:{'requerida':	785, 'acumulada':	3510},
        12:{'requerida':	1000, 'acumulada':	4510},
        13:{'requerida':	1250, 'acumulada':	5760},
        14:{'requerida':	1600, 'acumulada':	7325},
        15:{'requerida':	2000, 'acumulada':	9325},
        16:{'requerida':	2465, 'acumulada':	11825},
        17:{'requerida':	3125, 'acumulada':	14950},
        18:{'requerida':	4000, 'acumulada':	18950},
        19:{'requerida':	5000, 'acumulada':	23950},
        20:{'requerida':	6200, 'acumulada':	30200},
        21:{'requerida':	7800, 'acumulada':	38050},
        22:{'requerida':	9800, 'acumulada':	47850},
        23:{'requerida':	12200, 'acumulada':	60100},
        24:{'requerida':	15300, 'acumulada':	75400},
        25:{'requerida':	19050, 'acumulada':	94450},
    }
    skill_niveles = []

    def level_data(self, xp, max_level = 50, especial = False, promediar = True):
        if not especial:
            xp_per_level = self.xp_per_level
        else:
            if especial == 'runecrafting':
                xp_per_level = self.xp_per_level_runecrafting
        level = 0
        xp_level = 0
        for_next = 0
        for nivel in xp_per_level:
            try:
                if xp < xp_per_level[nivel + 1]['acumulada']:
                    level = nivel
                    xp_level = xp - xp_per_level[nivel]['acumulada']
                    for_next = xp_per_level[nivel + 1]['requerida']
                    break
            except:
                level = nivel
                xp_level = xp - xp_per_level[nivel]['acumulada']
                for_next = -1
                break
        if level > max_level:
            level = max_level
            for_next = -1
            xp_level = 0
        if promediar:
            self.skill_niveles.append(level)
        return {'level': level, 'xp_level': xp_level, 'for_next': for_next, 'total' : xp}

    def decode_skill_data(self, skill_data, skill_name):
        info = {}
        level = skill_data['level']
        xp_level = skill_data['xp_level']
        for_next = skill_data['for_next']
        total = skill_data['total']
        skill_emoji = self.general_emoji(f'skill_{skill_name}')
        o_level = level
        if for_next == -1:
            level = 'Max'
        name = f'{skill_emoji}*{skill_name}* nivel **{o_level}**'
        value = ''
        if level != 'Max':
            value += "```\n"
            porcentaje = xp_level / for_next * 100
            porcentaje = round(porcentaje, 2)
            text_xp_level = self.calculadora(f'{xp_level} + 0', letras = True)
            text_for_next = self.calculadora(f'{for_next} + 0', letras = True)
            value += f'{text_xp_level}/{text_for_next} ({porcentaje}%)\n'
        else:
            value += f'**{skill_name} al maximo** :partying_face:\n'
            value += "```\n"
        text_total = self.calculadora(f'{total} + 0')
        value += f'Total: {text_total}\n'
        value += '\n```'

        info['name'] = name
        info['value'] = value
        return info

    def get_data_embed(self, datos):
        
        fields = []
        skills_list = [
            {
                'nombre': 'Combat',
                'maximo': 60,
                'especial': False,
                'promediar': True
            },
            {
                'nombre': 'Farming',
                'maximo': 60,
                'especial': False,
                'promediar': True
            },
            {
                'nombre': 'Mining',
                'maximo': 60,
                'especial': False,
                'promediar': True
            },
            {
                'nombre': 'Foraging',
                'maximo': 50,
                'especial': False,
                'promediar': True
            },
            {
                'nombre': 'Fishing',
                'maximo': 50,
                'especial': False,
                'promediar': True
            },
            {
                'nombre': 'Enchanting',
                'maximo': 60,
                'especial': False,
                'promediar': True
            },
            {
                'nombre': 'Alchemy',
                'maximo': 50,
                'especial': False,
                'promediar': True
            },
            {
                'nombre': 'Taming',
                'maximo': 50,
                'especial': False,
                'promediar': True
            },
            {
                'nombre': 'Carpentry',
                'maximo': 50,
                'especial': False,
                'promediar': False
            },
            {
                'nombre': 'Runecrafting',
                'maximo': 25,
                'especial': 'runecrafting',
                'promediar': False
            }
        ]
        for skill in skills_list:
            try:
                total_xp = datos[f'experience_skill_{skill["nombre"].lower()}']
            except:
                total_xp = 0
            if not skill['especial']:
                especial = False
            else:
                especial = skill['especial']
            if skill['promediar']:
                promediar = True
            else:
                promediar = False
            skill_data = self.level_data(total_xp, max_level = skill['maximo'], especial = especial, promediar = promediar)
            fields.append(self.decode_skill_data(skill_data, skill['nombre']))
        return fields
    
    @cog_ext.cog_slash(name="skills", description="Muestra informacion de las skills de un jugador", options = [
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
    async def skills(self, msg: SlashContext, username: str = '', perfil: str = ''):
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
        
        data_embed = self.get_data_embed(datos)
        color = self.color_aleatorio()
        title = f'Skills de {username} en {perfil_name}'
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        promedio_skill = sum(self.skill_niveles) / len(self.skill_niveles)
        for skill_lvl in self.skill_niveles:
            print(skill_lvl)
        primedio_skill = round(promedio_skill, 2)
        description = f'Promedio de skills: {primedio_skill}'
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_thumbnail(url=url)
        for field in data_embed:
            embed.add_field(name=field['name'], value=field['value'], inline=False)
        text = f'El promedio de las skills no incluye runecrafting ni carpentry'
        embed.set_footer(text=text)
        await msg.edit(content = '', embed = embed)
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Skills(bot))
