import json
import pandas as pd
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord import *
from dislash.interactions import *
from discord_components import *
from discord.utils import get
from datetime import datetime
from time import sleep
from slash.generales import Generales, Item

class Slayer_player(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    uuid = ''
    atrox = {
        "xp": False,
        "price": False,
        "drops": False
    }

    def calcular_slayer(self, slayer_info, username, msg, datos, xp_por_niveles, tipo_slayer, interno = False, emoji = False):
        numeros = self.numeros
        uuid = self.uuid
        try:
            slayer_xp = slayer_info['xp']
        except:
            slayer_xp = 0

        if tipo_slayer.lower() == 'revenant':
            tipo_slayer = 'Revenant Horror'
        elif tipo_slayer.lower() == 'tarantula':
            tipo_slayer = 'Tarantula Broodfather'
        elif tipo_slayer.lower() == 'sven':
            tipo_slayer = 'Sven Packmaster'
        elif tipo_slayer.lower() == 'voidgloom':
            tipo_slayer = 'Voidgloom Seraph'

        # Verificar nivel
        level = 0
        if slayer_xp < xp_por_niveles[1]:
            level = 0
        elif slayer_xp < xp_por_niveles[2]:
            level = 1
        elif slayer_xp < xp_por_niveles[3]:
            level = 2
        elif slayer_xp < xp_por_niveles[4]:
            level = 3
        elif slayer_xp < xp_por_niveles[5]:
            level = 4
        elif slayer_xp < xp_por_niveles[6]:
            level = 5
        elif slayer_xp < xp_por_niveles[7]:
            level = 6
        elif slayer_xp < xp_por_niveles[8]:
            level = 7
        elif slayer_xp < xp_por_niveles[9]:
            level = 8
        else:
            level = 9

        if interno:
            return level
        
        embeds_data = []
        text = ''
        dropeos_hall = self.dropeo_hall(msg)
        if dropeos_hall[0]:
            text += dropeos_hall[1]
        color = self.color_aleatorio()
        title = f'{emoji} {self.for_tsuru(username)} {tipo_slayer.title()} lvl {numeros[level]}'
        sl_xp_impresion = ''
        if slayer_xp > 1000:
            sl_xp_impresion = self.calculadora(f'{slayer_xp} + 0', entero = True)
        else:
            sl_xp_impresion = self.calculadora(f'{slayer_xp} + 0', numeros = True, entero = True)
        description = f'XP Total: {sl_xp_impresion}' 
        embed = discord.Embed(title = title, description = description, color=color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
        for_embed = {}
        for_embed['fields'] = []
        for_embed['title'] = title
        for_embed['description'] = description
        for_embed['color'] = color
        for_embed['tumb'] = f'https://crafatar.com/renders/body/{uuid}?size=40'
        mensajes = []
        value = ''
        if self.atrox['xp']:
            for lvl in datos:
                datos[lvl]['xp'] *= 1.25
        if self.atrox['price']:
            for lvl in datos:
                datos[lvl]['costo'] *= 0.5
        niveles_por_mensaje = 0
        if level < 9:
            for i in range(level, 9):
                xp_lvl = xp_por_niveles[i + 1]
                xp_requerida = xp_lvl - slayer_xp
                lvl_1_faltantes = int(xp_requerida // datos[1]['xp']) + 1
                lvl_2_faltantes = int(xp_requerida // datos[2]['xp']) + 1
                lvl_3_faltantes = int(xp_requerida // datos[3]['xp']) + 1
                lvl_4_faltantes = int(xp_requerida // datos[4]['xp']) + 1
                try:
                    lvl_5_faltantes = int(xp_requerida // datos[5]['xp']) + 1
                except:
                    pass
                gasto_total_lvl_1 = lvl_1_faltantes * datos[1]['costo']
                gasto_total_lvl_2 = lvl_2_faltantes * datos[2]['costo']
                gasto_total_lvl_3 = lvl_3_faltantes * datos[3]['costo']
                gasto_total_lvl_4 = lvl_4_faltantes * datos[4]['costo']
                try:
                    gasto_total_lvl_5 = lvl_5_faltantes * datos[5]['costo']
                except:
                    pass

                exp_faltante = f' de experiencia para el nivel {i + 1}'
                if xp_requerida < 1000:
                    xp_requerida = self.calculadora(f'{xp_requerida} + 0', impresion = True, entero = True)
                else:
                    xp_requerida = self.calculadora(f'{xp_requerida} + 0', entero = True)
                name = f'Falta {xp_requerida} {exp_faltante}'
                value = '```elm\n'
                if lvl_1_faltantes > 1000:
                    lvl_1_faltantes = self.calculadora(f'{lvl_1_faltantes} + 0')
                if gasto_total_lvl_1 > 1000:
                    gasto_total_lvl_1 = self.calculadora(f'{gasto_total_lvl_1} + 0')
                value += f'T1: {lvl_1_faltantes} \nCosto total de: {gasto_total_lvl_1} \n\n'

                if lvl_2_faltantes > 1000:
                    lvl_2_faltantes = self.calculadora(f'{lvl_2_faltantes} + 0')
                if gasto_total_lvl_2 > 1000:
                    gasto_total_lvl_2 = self.calculadora(f'{gasto_total_lvl_2} + 0')
                value += f'T2: {lvl_2_faltantes} \nCosto total de: {gasto_total_lvl_2} \n\n'

                if lvl_3_faltantes > 1000:
                    lvl_3_faltantes = self.calculadora(f'{lvl_3_faltantes} + 0')
                if gasto_total_lvl_3 > 1000:
                    gasto_total_lvl_3 = self.calculadora(f'{gasto_total_lvl_3} + 0')
                value += f'T3: {lvl_3_faltantes} \nCosto total de: {gasto_total_lvl_3} \n\n'

                if lvl_4_faltantes > 1000:
                    lvl_4_faltantes = self.calculadora(f'{lvl_4_faltantes} + 0')
                if gasto_total_lvl_4 > 1000:
                    gasto_total_lvl_4 = self.calculadora(f'{gasto_total_lvl_4} + 0')
                value += f'T4: {lvl_4_faltantes} \nCosto total de: {gasto_total_lvl_4} \n\n'
                
                try:
                    if lvl_5_faltantes > 1000:
                        lvl_5_faltantes = self.calculadora(f'{lvl_5_faltantes} + 0')
                    if gasto_total_lvl_5 > 1000:
                        gasto_total_lvl_5 = self.calculadora(f'{gasto_total_lvl_5} + 0')
                    value += f'T5: {lvl_5_faltantes} \nCosto total de: {gasto_total_lvl_5} \n\n'
                except:
                    pass
                value += '```'
                embed.add_field(name=name, value=value, inline=False)
                for_embed['fields'].append([name, value, False])
                niveles_por_mensaje += 1

                if niveles_por_mensaje == 3:
                    mensajes.append(embed)
                    embeds_data.append(for_embed)
                    value = ''
                    embed = discord.Embed(title = title, description = description, color=color)
                    embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
                    for_embed = {}
                    for_embed['fields'] = []
                    for_embed['title'] = title
                    for_embed['description'] = description
                    for_embed['color'] = color
                    for_embed['tumb'] = f'https://crafatar.com/renders/body/{uuid}?size=40'
                    niveles_por_mensaje = 0
        else:
            name = f'{tipo_slayer} al maximo\n'
            value = f'Felicidades :partying_face:'
            embed.add_field(name=name, value=value, inline=False)
            for_embed['fields'].append([name, value, False])
            mensajes.append(embed)
            embeds_data.append(for_embed)
        
        if niveles_por_mensaje < 3 and niveles_por_mensaje != 0:
            embed.add_field(name=name, value=value, inline=False)
            for_embed['fields'].append([name, value, False])
            mensajes.append(embed)
            embeds_data.append(for_embed)
        paginas = len(mensajes)
        for i in range(paginas):
            text = f'pagina {i+1} / {paginas}'
            mensajes[i].set_footer(text=text)
            embeds_data[i]['footer'] = text
        return mensajes, embeds_data

    def aux_general(self, syaler_info, username, msg, datos, xp_por_niveles, slayer_name, emoji):
        tipo_slayer = ''
        if slayer_name.lower() == 'revenant':
            tipo_slayer = 'zombie'
            slayer_name = 'Revenant Horror'
        elif slayer_name.lower() == 'tarantula':
            tipo_slayer = 'spider'
            slayer_name = 'Tarantula Broodfather'
        elif slayer_name.lower() == 'sven':
            tipo_slayer = 'wolf'
            slayer_name = 'Sven Packmaster'
        elif slayer_name.lower() == 'voidgloom':
            tipo_slayer = 'enderman'
            slayer_name = 'Voidgloom Seraph'

        lvl = self.calcular_slayer(syaler_info, username, msg, datos, xp_por_niveles, tipo_slayer,interno = True)
        numeros = self.numeros
        
        try:
            xp = syaler_info['xp']
        except:
            xp = 0
        
        xp_format = self.calculadora(f'{xp} + 0', letras = True)
        xp_siguiente_format = self.calculadora(f'{xp_por_niveles[lvl]} + 0', letras = True)
        value = '``` \n'
        try:
            xp_siguiente = xp_por_niveles[lvl + 1]
            xp_faltante = xp_siguiente - xp
            xp_faltante_format = self.calculadora(f'{xp_faltante} + 0', letras = True)
            name = f'{emoji} {slayer_name.title()} {numeros[lvl]}'
            value += f'XP: {xp_format}/{xp_siguiente_format}\n'
            value += f'Falta: {xp_faltante_format}\n'
            value += f'Para informacion detallada selecciona {slayer_name}'
            value += '```'
        except:
            name = f'{emoji} {slayer_name.title()} {numeros[lvl]}'
            value += f'XP: {xp_format}/{xp_siguiente_format}\n{slayer_name.title()} al Maximo. '
            value += '```'
            value += f'Felicidades :partying_face:'
        if xp > 1:
            value += '```excel\n'
            #print(syaler_info)
            for i in range(5):
                buscar = f'boss_kills_tier_{i}'
                try:
                    muertes = syaler_info[buscar]
                    value += f'Tier {i + 1}: {muertes}\n'
                except:
                    pass
            value += '```'
        return name, value
    
    def info_general(self, slayer_info, username, msg, tipo_slayer, emojis):
        numeros = self.numeros
        #return msg.reply(f'Comando corto en proceso, mientras continua utilizando -s (tipo de slayer)')
        # Tipos De Slayer
        # zombie,spider,wolf,enderman
        uuid = self.uuid
        zombie_emoji = emojis[0]
        spider_emoji = emojis[1]
        wolf_emoji = emojis[2]
        enderman_emoji = emojis[3]
        text = ''
        dropeos_hall = self.dropeo_hall(msg)
        if dropeos_hall[0]:
            text += dropeos_hall[1]
        color = self.color_aleatorio()
        embed = discord.Embed(title=f'Slayers de {self.for_tsuru(username)}', color=color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
        # Zombies
        xp_por_niveles = {
            0: 0,
            1: 5,
            2: 15,
            3: 200,
            4: 1000,
            5: 5000,
            6: 20000,
            7: 100000,
            8: 400000,
            9: 1000000
        }
        datos = {
            1: {
                'xp': 5,
                'costo': 2000
            },
            2: {
                'xp': 25,
                'costo': 7500
            },
            3: {
                'xp': 100,
                'costo': 20000
            },
            4: {
                'xp': 500,
                'costo': 50000
            },
            5: {
                'xp': 1500,
                'costo': 100000
            }
        }
        zombie_info = slayer_info['zombie']        
        name , value = self.aux_general(zombie_info, username, msg, datos, xp_por_niveles, "revenant", zombie_emoji)
        embed.add_field(name=name, value=value, inline=True)

        # Spider
        xp_por_niveles = {
            0: 0,
            1: 5,
            2: 25,
            3: 200,
            4: 1000,
            5: 5000,
            6: 20000,
            7: 100000,
            8: 400000,
            9: 1000000
        }
        datos = {
            1: {
                'xp': 5,
                'costo': 2000
            },
            2: {
                'xp': 25,
                'costo': 7500
            },
            3: {
                'xp': 100,
                'costo': 20000
            },
            4: {
                'xp': 500,
                'costo': 50000
            }
        }
        spider_info = slayer_info['spider']
        name , value = self.aux_general(spider_info, username, msg, datos, xp_por_niveles, "tarantula", spider_emoji)
        embed.add_field(name=name, value=value, inline=True)
        
        # Wolf
        xp_por_niveles = {
            0: 0,
            1: 10,
            2: 30,
            3: 250,
            4: 1500,
            5: 5000,
            6: 20000,
            7: 100000,
            8: 400000,
            9: 1000000
        }
        datos = {
            1: {
                'xp': 5,
                'costo': 2000
            },
            2: {
                'xp': 25,
                'costo': 7500
            },
            3: {
                'xp': 100,
                'costo': 20000
            },
            4: {
                'xp': 500,
                'costo': 50000
            }
        }
        wolf_info = slayer_info['wolf']
        name , value = self.aux_general(wolf_info, username, msg, datos, xp_por_niveles, "sven", wolf_emoji)
        embed.add_field(name=name, value=value, inline=True)

        # Enderman
        xp_por_niveles = {
            0: 0,
            1: 10,
            2: 30,
            3: 250,
            4: 1500,
            5: 5000,
            6: 20000,
            7: 100000,
            8: 400000,
            9: 1000000
        }
        datos = {
            1: {
                'xp': 5,
                'costo': 2000
            },
            2: {
                'xp': 25,
                'costo': 7500
            },
            3: {
                'xp': 100,
                'costo': 20000
            },
            4: {
                'xp': 500,
                'costo': 50000
            }
        }
        enderman_info = slayer_info['enderman']
        name , value = self.aux_general(enderman_info, username, msg, datos, xp_por_niveles, "voidgloom", enderman_emoji)
        embed.add_field(name=name, value=value, inline=True)
        embed.set_footer(text=text)
        return embed

    def remove_acute(self, text):
        replaces =  {
            'á': 'a',
            'é': 'e',
            'í': 'i',
            'ó': 'o',
            'ú': 'u'
        }
        for key, value in replaces.items():
            text = text.replace(key, value)
        return text

    @cog_ext.cog_slash(name="slayer", description="Muestra datos sobre slayers", options = [
        create_option(
            name = 'username',
            description = 'Username',
            option_type = 3,
            required =False
        ),
        create_option(
            name = 'perfil',
            description = 'Nombre del prefil',
            option_type = 3,
            required=False,
        )
    ])
    async def slayer(self, msg: SlashContext, username: str = '', perfil: str = ''):
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
        emojis = [
            '<:revenant:892834994832162817>',
            '<:tarantula:892834995125755964>',
            '<:sven:892834995239022602>',
            '<:voidgloom:892834995163512832>'
        ]
        componentes = [
            {
                "type": 1,
                "components": [
                    {
                        "type": 3,
                        "custom_id": "tipo",
                        "options":[
                            {
                                "label": "Generales",
                                "value": "0",
                                "description": "Muestra informacion general de todas las slayer",
                                "emoji": {
                                    "name": "combat",
                                    "id": "905669276780867624"
                                }
                            },
                            {
                                "label": "Revenant Horror",
                                "value": "1",
                                "description": "Detalles de Revenant Horror",
                                "emoji": {
                                    "name": "revenant",
                                    "id": "892834994832162817"
                                },
                            },
                            {
                                "label": "Tarantula Broodfather",
                                "value": "2",
                                "description": "Detalles de Tarantula Broodfather",
                                "emoji": {
                                    "name": "tarantula",
                                    "id": "892834995125755964"
                                },
                            },
                            {
                                "label": "Sven Packmaster",
                                "value": "3",
                                "description": "Detalles de Sven Packmaster",
                                "emoji": {
                                    "name": "sven",
                                    "id": "892834995239022602"
                                },
                            },
                            {
                                "label": "Voidgloom Seraph",
                                "value": "4",
                                "description": "Detalles de Voidgloom Seraph",
                                "emoji": {
                                    "name": "voidgloom",
                                    "id": "892834995163512832"
                                },
                            }
                        ],
                        "placeholder": "Elige un tipo"
                    }
                ]
            }
        ]
        msg = await msg.reply(content = f'Cargando...', components = componentes)

        # -------------- Obtencion de datos ----------------
        try:
            if uuid != '':
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True, uuid_key=uuid)
            else:
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True)
            self.uuid = uuid
            #open(f'./info_pruebas/{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return
        
        try:
            datos = datos[0]
        except:
            datos = datos

        slayers_info = datos['slayer_bosses']

        nombres = ['zombie', 'spider', 'wolf', 'enderman']
        embed_general =  self.info_general(slayers_info, username, original_msg, nombres, emojis)
        await msg.edit(content = '', embed = embed_general)
        total_mensajes = []
        total_emb_data = []
        total_mensajes.append(embed_general)
        total_emb_data.append([])
        # agregando embeds de las slayers
        if True:
            xp_por_niveles = {
                0: 0,
                1: 5,
                2: 15,
                3: 200,
                4: 1000,
                5: 5000,
                6: 20000,
                7: 100000,
                8: 400000,
                9: 1000000
            }
            datos = {
                1: {
                    'xp': 5,
                    'costo': 2000
                },
                2: {
                    'xp': 25,
                    'costo': 7500
                },
                3: {
                    'xp': 100,
                    'costo': 20000
                },
                4: {
                    'xp': 500,
                    'costo': 50000
                },
                5: {
                    'xp': 1500,
                    'costo': 100000
                }
            }
            mensajes, embeds_data = self.calcular_slayer(slayers_info['zombie'], username, original_msg, datos, xp_por_niveles, 'Revenant', emoji = emojis[0])
            total_mensajes.append(mensajes)
            total_emb_data.append(embeds_data)
            xp_por_niveles = {
                0: 0,
                1: 5,
                2: 25,
                3: 200,
                4: 1000,
                5: 5000,
                6: 20000,
                7: 100000,
                8: 400000,
                9: 1000000
            }
            datos = {
                1: {
                    'xp': 5,
                    'costo': 2000
                },
                2: {
                    'xp': 25,
                    'costo': 7500
                },
                3: {
                    'xp': 100,
                    'costo': 20000
                },
                4: {
                    'xp': 500,
                    'costo': 50000
                }
            }
            mensajes, embeds_data = self.calcular_slayer(slayers_info['spider'], username, original_msg, datos, xp_por_niveles, 'Tarantula', emoji = emojis[1])
            total_mensajes.append(mensajes)
            total_emb_data.append(embeds_data)
            xp_por_niveles = {
                0: 0,
                1: 10,
                2: 30,
                3: 250,
                4: 1500,
                5: 5000,
                6: 20000,
                7: 100000,
                8: 400000,
                9: 1000000
            }
            datos = {
                1: {
                    'xp': 5,
                    'costo': 2000
                },
                2: {
                    'xp': 25,
                    'costo': 7500
                },
                3: {
                    'xp': 100,
                    'costo': 20000
                },
                4: {
                    'xp': 500,
                    'costo': 50000
                }
            }
            mensajes, embeds_data = self.calcular_slayer(slayers_info['wolf'], username, original_msg, datos, xp_por_niveles, 'Sven', emoji = emojis[2])
            total_mensajes.append(mensajes)
            total_emb_data.append(embeds_data)
            xp_por_niveles = {
                0: 0,
                1: 10,
                2: 30,
                3: 250,
                4: 1500,
                5: 5000,
                6: 20000,
                7: 100000,
                8: 400000,
                9: 1000000
            }
            datos = {
                1: {
                    'xp': 5,
                    'costo': 2000
                },
                2: {
                    'xp': 25,
                    'costo': 7500
                },
                3: {
                    'xp': 100,
                    'costo': 20000
                },
                4: {
                    'xp': 500,
                    'costo': 50000
                }
            }
            mensajes, embeds_data = self.calcular_slayer(slayers_info['enderman'], username, original_msg, datos, xp_por_niveles, 'Voidgloom', emoji = emojis[3])
            total_mensajes.append(mensajes)
            total_emb_data.append(embeds_data)
            
        text = ''
        if self.atrox['xp']:
            text += f'Buff de XP\n'
        if self.atrox['price']:
            text += f'Buff de PRECIO\n'
        if self.atrox['drops']:
            text += f'Buff de DROPS\n'
        if text != '':
            for i in range(1, 5):
                paginas_totales = total_mensajes[i]
                text = f'Perks activos de Aatrox:\n' + text
                for j in range(paginas_totales):
                    total_mensajes[i][j].set_footer(text = text)
                    total_emb_data[i][j]['footer'] = text
                    
        self.msg = msg
        self.original_msg = original_msg
        
        await self.esperando_boton_embed(msg, total_mensajes, menu=True, data_emb = total_emb_data)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Slayer_player(bot))
