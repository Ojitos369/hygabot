import json
import pathlib
import os
import discord
from datetime import datetime
from discord import embeds
from funciones.generales import Generales
class Hotm(Generales):
    arboles_previos = {}
    
    def hotm(self, msg = '', text = ''):
        self.config()
        # -------------- Separacion de datos buscando opciones y usuario ----------------
        separado = text.split(' ')
        username = separado[0]
        try:
            perfil_name = separado[1]
        except:
            perfil_name = ''
        
        # -------------- Verificar detallado ----------------
        detallado = False
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-d' or separado[i] == '-detallado':
                detallado = True
                posicion = i
                break
        if posicion != -1:
            separado.pop(posicion)

        try:
            username = self.get_username(username)
        except:
            pass

        # -------------- Obtencion de datos ----------------
        try:
            datos, perfil_name, uuid = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        #open(f'./info_pruebas/{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            return msg.reply('Verifica que el Usuario este bien escrito')
        if datos == 'perfil':
            return msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')

        username = self.for_tsuru(username)

        levels_data = {
            1: {
                'requerida': 0,
                'acumulada': 0
            },
            2: {
                'requerida': 3000,
                'acumulada': 3000
            },
            3: {
                'requerida': 9000,
                'acumulada': 12000
            },
            4: {
                'requerida': 25000,
                'acumulada': 37000
            },
            5: {
                'requerida': 60000,
                'acumulada': 97000
            },
            6: {
                'requerida': 100000,
                'acumulada': 197000
            },
            7: {
                'requerida': 150000,
                'acumulada': 347000
            }
        }

        data = datos['mining_core']
        mensajes = []
        mensajes_totales = 3
        # ---------------------------------  HOTM LEVEL ---------------------------------
        # -------------- Tokens ----------------
        tokens_totales = 0
        try:
            tokens_disponibles = data['tokens']
        except:
            tokens_disponibles = 0
        try:
            tokens_gastados = data['tokens_spent']
        except:
            tokens_gastados = 0
        tokens_totales = tokens_disponibles + tokens_gastados

        # -------------- Level ----------------
        try:
            experiencia = data['experience']
        except:
            experiencia = 0
        level = 1
        for nivel, datos_nivel in levels_data.items():
            if experiencia >= datos_nivel['acumulada']:
                level = nivel
        xp_de_nivel = experiencia - levels_data[level]['acumulada']
        try:
            xp_requerida_next_level = levels_data[level + 1]['requerida']
        except:
            xp_requerida_next_level = 0

        color = self.color_aleatorio()
        title = f'{username} en {perfil_name} Hotm lvl {level}'
        if level < 7:
            description = f'Experiencia: {xp_de_nivel:,.0f}/{xp_requerida_next_level:,.0f} para nivel {level + 1} ({(xp_de_nivel/xp_requerida_next_level*100):,.0f}%)'
        else:
            description = f'Experiencia: {experiencia:,.0f}'
        embed = discord.Embed(title=title, description = description, color=color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')

        if True:
            # -------------- Exp por accion ----------------
            nucleo = 800
            crystal = 400
            mines = 100

            if level < 7:
                for i in range(level + 1, 8):
                    con_nucleo = (levels_data[i]['acumulada'] - experiencia) // nucleo + 1
                    con_crystal = (levels_data[i]['acumulada'] - experiencia) // crystal + 1
                    con_mines = (levels_data[i]['acumulada'] - experiencia) // mines + 1

                    name = f'Comisiones para el nivel {i}'
                    value = '```'
                    value += f'xp total: {experiencia:,.0f}/{levels_data[i]["acumulada"]:,.0f} ({(experiencia/levels_data[i]["acumulada"]*100):,.0f}%)\n'
                    if i > 2:
                        value += f'Nucleos: {con_nucleo:,.0f}\n'
                        value += f'Crystal: {con_crystal:,.0f}\n'
                    value += f'Mines: {con_mines:,.0f}\n'
                    value += '```'
                    embed.add_field(name=name, value=value, inline=False)
            else:
                if tokens_totales == 16:
                    name = f':partying_face: :partying_face: :partying_face:'
                    value = '```'
                    value += f'Hotm al maximo Felicidades\n'
                    value += '```'
                    embed.add_field(name=name, value=value, inline=False)
                else:
                    name = f'Hotm al nivel maximo'
                    value = '```'
                    value += f'Aun puedes conseguir {16 - tokens_totales} tokens\n'
                    value += '```'
                    embed.add_field(name=name, value=value, inline=False)
        else:
            pass
        
        text = f'Pagina 1/{mensajes_totales}'
        embed.set_footer(text = text)
        mensajes.append(embed)
        # --------------------------------- Crystales ---------------------------------
        if level > 2:
            crystal_data = data['crystals']
            crystals = [
                "jade_crystal",
                "amber_crystal",
                "topaz_crystal",
                "sapphire_crystal",
                "amethyst_crystal",
                "jasper_crystal",
                "ruby_crystal"
            ]
            menor_colocado = 0
            data_for_fields = []

            for crystal in crystals:
                name = crystal.replace('_', ' ').replace('crystal','gemstone')
                name = self.get_emoji_name(name)
                name = name.replace('gemstone', 'crystal')
                split_name = name.split(' ')
                name = ''
                for palabra in split_name:
                    name += f'{palabra.capitalize()} '
                try:
                    estado = crystal_data[crystal]['state'].lower()
                    estado = estado.replace('placed', 'colocado')
                    estado = estado.replace('not_found', 'sin_encontrar')
                    estado = estado.replace('found', 'encontrado')
                    estado = estado.replace('_', ' ')
                    estado = estado.capitalize()
                    try:
                        colocados = crystal_data[crystal]['total_placed']
                    except:
                        colocados = 0
                except:
                    estado = 'Sin encontrar'
                    colocados = 0
                if not ('jasper' in name.lower() or 'ruby' in name.lower()):
                    if menor_colocado == 0:
                        menor_colocado = colocados
                    if colocados < menor_colocado:
                        menor_colocado = colocados
                    
                estado = estado.replace("Sin encontrar" ,"'Pendiente'")
                estado = estado.replace("Colocado" ,'"Colocado"')

                value = f'**```ml\n{estado}```**'

                data_for_fields.append([name, value])
            
            description = f'Cristales | Nucleos completados: {menor_colocado}'
            embed = discord.Embed(title=title,  description=description, color=color)
            embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
            for fiel in data_for_fields:
                embed.add_field(name=fiel[0], value=fiel[1], inline=False)
            text = f'Pagina 2/{mensajes_totales}'
            embed.set_footer(text = text)
            mensajes.append(embed)
        else:
            description = f'Sin nivel para acceder a las crystal hollows'
            embed = discord.Embed(title=title,  description=description, color=color)
            embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
            text = f'Pagina 2/{mensajes_totales}'
            embed.set_footer(text = text)
            mensajes.append(embed)
        
        # ------------------------- Imagen de perks -----------------------------
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        #try:
        tree_1 = self.perks_tree(data, title, color, level, url = url)
        mensajes.append(tree_1)
#        except:
#            description = 'No se encontraron mejoras en el hotm'
#            #description = 'Pagina en desarollo'
#            embed = discord.Embed(title=title,  description=description, color=color)
#            embed.set_thumbnail(url=url)
#            text = f'Pagina 3/3'
#            embed.set_footer(text = text)
#            mensajes.append(embed)
        return mensajes

    def perks_tree(self, data, title, color, nivel, url = ''):
        path = pathlib.Path().resolve()
        coal = "<:coal:893388568091844619>"
        esmeralda = "<:emerald:893388567970197515>"
        glass = "<:glass_gray:893388568255426562>"
        diamond = "<:diamond:893587666069778492>"
        nodes = data['nodes']
        unique_name = ''
        perks_info = {
            1: {
                'mining_speed': 50
            },
            2: {
                'mining_fortune': 50,
                'titanium_insanium': 50,
                'quick_forge': 20,
                'mining_speed_boost': 1,
                'pikobulus': 1
            },
            3: {
                'daily_powder': 100,
                'luck_of_the_cave': 45,
                'crystallized': 30
            },
            4: {
                'efficient_miner': 100,
                'seasoned_mineman': 100,
                'orbiter': 80,
                'mining_madness': 1,
                'front_loaded': 1,
                'sky_mall': 1,
                'precision_mining': 1
            },
            5: {
                'special_0': 5,
                'goblin_killer': 1,
                'star_powder': 1
            },
            6: {
                'mole': 190,
                'professional': 140,
                'fortunate': 20,
                'lonesome_miner': 45,
                'great_explorer': 20,
                'vein_seeker': 1,
                'maniac_miner': 1
            },
            7: {
                'powder_buff': 50,
                'mining_speed_2': 50,
                'mining_fortune_2': 50
            }
        }
        # ---------------------- Guardado imagen si no existe --------------------
        if unique_name not in self.arboles_previos:
            nivel_1 = ['void', 'void', 'void', 'mining_speed', 'void', 'void', 'void']
            nivel_2 = ['void', 'mining_speed_boost', 'titanium_insanium', 'mining_fortune', 'quick_forge', 'pikobulus', 'void']
            nivel_3 = ['void', 'luck_of_the_cave', 'void', 'daily_powder', 'void', 'crystallized', 'void']
            nivel_4 = ['sky_mall', 'mining_madness', 'seasoned_mineman', 'efficient_miner', 'orbiter', 'front_loaded', 'precision_mining']
            nivel_5 = ['void', 'goblin_killer', 'void', 'special_0', 'void', 'star_powder', 'void']
            nivel_6 = ['vein_seeker', 'lonesome_miner', 'professional', 'mole', 'fortunate', 'great_explorer', 'maniac_miner']
            nivel_7 = ['void', 'mining_speed_2', 'void', 'powder_buff', 'void', 'mining_fortune_2', 'void']
            niveles = [nivel_1, nivel_2, nivel_3, nivel_4, nivel_5, nivel_6, nivel_7]
            mensaje = ''
            for i in range(0, 7):                
                lvl = niveles[i]
                msg_lvl = f'{i +1}: \t'
                for perk in lvl:
                    if perk == 'void':
                        msg_lvl += f'\t{glass}\t'
                    elif perk in nodes:
                        if nodes[perk] >= perks_info[i+1][perk]:
                            msg_lvl += f'\t{diamond}\t'
                        else:
                            msg_lvl += f'\t{esmeralda}\t'                        
                        unique_name += f'{perk}'
                    else:
                        msg_lvl += f'\t{coal}\t'
                mensaje = f'\n{msg_lvl}\n{mensaje}\n'
            if unique_name != '':
                self.arboles_previos[f'{unique_name}'] = mensaje
        # ------------------------- embed -----------------------------
        mensaje = self.arboles_previos[f'{unique_name}']
        description = mensaje
        embed = discord.Embed(title=title,  description=description, color=color)
        embed.set_thumbnail(url=url)
        text = f'Pagina 3/3'
        embed.set_footer(text = text)
        return embed
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'hotm': self.hotm
        }
