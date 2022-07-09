import json
import discord
from datetime import datetime
from mojang import MojangAPI
from funciones.generales import Generales

class Slayer_player(Generales):
    uuid = ''
    def calcular_slayer(self, slayer_info, username, msg, datos, xp_por_niveles, tipo_slayer, interno = False, emoji = False):
        numeros = self.numeros
        uuid = self.uuid
        try:
            slayer_xp = slayer_info['xp']
        except:
            slayer_xp = 0

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
        
        color = self.color_aleatorio()
        title = f'{emoji} {self.for_tsuru(username)} {tipo_slayer.capitalize()}s lvl {numeros[level]}'
        description = f'XP Total: ' + "{:,.2f}".format(slayer_xp) 
        embed = discord.Embed(title = title, description = description, color=color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
        mensajes = []
        value = ''
        if level < 9:
            niveles_por_mensaje = 0
            for i in range(level, 9):
                xp_requerida = xp_por_niveles[i + 1] - slayer_xp
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
                name = 'Falta ' + "{:,.0f}".format(xp_requerida) + str(exp_faltante)
                value = f'```T1: ' + "{:,.0f}".format(lvl_1_faltantes) + ' \nCosto total de: ' + "{:,.0f}".format(gasto_total_lvl_1) + '\n\n'
                value += f'T2: ' + "{:,.0f}".format(lvl_2_faltantes) + ' \nCosto total de: ' + "{:,.0f}".format(gasto_total_lvl_2) + '\n\n'
                value += f'T3: ' + "{:,.0f}".format(lvl_3_faltantes) + ' \nCosto total de: ' + "{:,.0f}".format(gasto_total_lvl_3) + '\n\n'
                value += f'T4: ' + "{:,.0f}".format(lvl_4_faltantes) + ' \nCosto total de: ' + "{:,.0f}".format(gasto_total_lvl_4) + '\n\n'
                try:
                    value += f'T5: ' + "{:,.0f}".format(lvl_5_faltantes) + ' \nCosto total de: ' + "{:,.0f}".format(gasto_total_lvl_5) + '\n\n```'
                except:
                    value += '```'
                embed.add_field(name=name, value=value, inline=False)
                niveles_por_mensaje += 1

                if niveles_por_mensaje == 3:
                    mensajes.append(embed)
                    value = ''
                    embed = discord.Embed(title = title, description = description, color=color)
                    embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
                    niveles_por_mensaje = 0
        else:
            name = f'{tipo_slayer} al maximo\n'
            value = f'Felicidades :partying_face:'
        
        if level % 3 == 0:
            embed.add_field(name=name, value=value, inline=False)
        mensajes.append(embed)
        return mensajes

    def aux_general(self, syaler_info, username, msg, datos, xp_por_niveles, slayer_name, emoji):
        tipo_slayer = ''
        if slayer_name.lower() == 'revenant':
            tipo_slayer = 'zombie'
        elif slayer_name.lower() == 'tarantula':
            tipo_slayer = 'spider'
        elif slayer_name.lower() == 'sven':
            tipo_slayer = 'wolf'
        elif slayer_name.lower() == 'voidgloom':
            tipo_slayer = 'enderman'

        lvl = self.calcular_slayer(syaler_info, username, msg, datos, xp_por_niveles, tipo_slayer,interno = True)
        numeros = self.numeros
        try:
            xp = syaler_info['xp']
        except:
            xp = 0
        try:
            xp_siguiente = xp_por_niveles[lvl + 1]
            xp_faltante = xp_siguiente - xp
            xp_format = "{:,.2f}".format(xp)
            xp_siguiente_format = "{:,.2f}".format(xp_siguiente)
            xp_faltante_format = "{:,.2f}".format(xp_faltante)
            name = f'{emoji} {tipo_slayer.capitalize()} {numeros[lvl]}'
            value = f'```XP: {xp_format}/{xp_siguiente_format}\n'
            value += f'Falta: {xp_faltante_format}\n'
            value += f'Para informacion detallada usa:\n"{self.prefijo}sy {username} -s {slayer_name}"```'
        except:
            xp_format = "{:,.2f}".format(xp)
            xp_siguiente_format = "{:,.2f}".format(xp_por_niveles[lvl])
            name = f'{emoji} {tipo_slayer.capitalize()} {numeros[lvl]}'
            value = f'```XP: {xp_format}/{xp_siguiente_format}\n{tipo_slayer.capitalize()} al Maximo```'
            value += f'Felicidadres :partying_face:'
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
        embed.add_field(name=name, value=value, inline=False)

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
        embed.add_field(name=name, value=value, inline=False)
        
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
        embed.add_field(name=name, value=value, inline=False)

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
        embed.add_field(name=name, value=value, inline=False)

        return msg.reply(embed = embed)

    def slayer(self, msg = '', text = ''):
        numeros = self.numeros
        separado = text.split(' ')
        username = separado[0]
        try:
            username = self.get_username(username)
        except:
            return msg.reply('Revise que el usuario este bien escrito')
        tipo_slayer = ''
        detalle = False
        especificado = False
        # ------------- verificar tipo de slayer -------------
        posicion = -1 
        for i in range(len(separado)):
            if separado[i].lower() == '-s' or separado[i].lower() == '-slayer':
                try:
                    tipo_slayer = separado[i + 1].lower()
                    posicion = i
                    detalle = True
                    break
                except:
                    return msg.reply(f'Despues de -s se debe especificar el tipo de slayer. Ejemplo: -s revenant')

        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
            especificado = True
        
        """ if not especificado:
            return msg.reply(f'Se debe especificar el tipo de slayer con -s/-slayer. Ejemplo: -s revenant') """
        if especificado:
            slayer_zombie = False
            slayer_tarantula = False
            slayer_lobo = False
            slayer_ender = False
            if 'zom' in tipo_slayer or 'rev' in tipo_slayer or 'hor' in tipo_slayer:
                slayer_zombie = True
            if 'tara' in tipo_slayer or 'spi' in tipo_slayer or 'ara' in tipo_slayer or 'bro' in tipo_slayer or 'tar' in tipo_slayer:
                slayer_tarantula = True
            if 'lob' in tipo_slayer or 'sve' in tipo_slayer or 'pac' in tipo_slayer or 'wol' in tipo_slayer:
                slayer_lobo = True
            if 'end' in tipo_slayer or 'voi' in tipo_slayer or 'ser' in tipo_slayer:
                slayer_ender = True
            
            if not (slayer_zombie or slayer_tarantula or slayer_lobo or slayer_ender):
                return msg.reply(f'No se encontraron slayers que coincidan')
        
        perfil_name = ''
        if len(separado) > 1:
            perfil_name = separado[1]

        # -------------- Obtencion de datos ----------------
        try:
            datos, perfil_name, self.uuid = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        if datos == 'usuario':
            return msg.reply('Verifica que el Usuario este bien escrito')
        if datos == 'perfil':
            msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')
        
        try:
            datos = datos[0]
        except:
            datos = datos

        slayers_info = datos['slayer_bosses']
        emojis = [
            '<:revenant:892834994832162817>',
            '<:tarantula:892834995125755964>',
            '<:sven:892834995239022602>',
            '<:voidgloom:892834995163512832>'
        ]

        if not detalle:
            nombres = ['zombie', 'spider', 'wolf', 'enderman']
            mensajes = []
            mensajes.append(self.info_general(slayers_info, username, msg, nombres, emojis))
            mensajes.append(['especial', f'Este comando esta disponible con ***/slayer*** pronto dejara de funcionar con *{self.prefijo}slayer*'])
            return mensajes

        # ------------- Funcion dependiendo del slayer -------------
        if slayer_zombie:
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
            mensajes = self.calcular_slayer(slayers_info['zombie'], username, msg, datos, xp_por_niveles, 'Revenant', emoji = emojis[0])
        elif slayer_tarantula:
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
            mensajes = self.calcular_slayer(slayers_info['spider'], username, msg, datos, xp_por_niveles, 'Tarantula', emoji = emojis[1])
        elif slayer_lobo:
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
            mensajes = self.calcular_slayer(slayers_info['wolf'], username, msg, datos, xp_por_niveles, 'Sven', emoji = emojis[2])
        elif slayer_ender:
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
            mensajes = self.calcular_slayer(slayers_info['enderman'], username, msg, datos, xp_por_niveles, 'Voidgloom', emoji = emojis[3])
        mensajes.append(['especial', f'Este comando esta disponible con ***/slayer*** pronto dejara de funcionar con *{self.prefijo}slayer*'])
        return mensajes
        
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'slayer': self.slayer,
            'slayers': self.slayer,
            'sy': self.slayer
        }