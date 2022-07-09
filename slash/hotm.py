import json
import pathlib
import os
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from slash.generales import Generales
class Hotm(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    arboles_previos = {}

    @cog_ext.cog_slash(name="hotm", description="Muestra datos del corazon de la montaña", options = [
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
    async def hotm(self, msg: SlashContext, username: str = '', perfil: str = ''):
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
        try:
            if uuid != '':
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True, uuid_key=uuid)
            else:
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        #open(f'./info_pruebas/{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        #print(f'Saved as {username}_{perfil_name}.json')
        if datos == 'usuario':
            await msg.reply('Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')
            return
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
        mensajes_totales = 4

        componentes = [
            {
                "type": 1,
                "components": [
                        {
                            "type": 2,
                            "label": "Comisiones",
                            "custom_id": "0",
                            "style": 2
                        },
                        {
                            "type": 2,
                            "label": "Cristales",
                            "custom_id": "1",
                            "style": 2
                        },
                        {
                            "type": 2,
                            "label": "Tree Perks",
                            "custom_id": "2",
                            "style": 2
                        },
                        {
                            "type": 2,
                            "label": "Powder y Perks",
                            "custom_id" :"3",
                            "style": 2
                        }
                ]
            }
        ]
        componentes = []
        new_com = {
            "type": 3,
            "custom_id": "tipo",
            "options":[
                {
                    "label": "Comisiones",
                    "value": "0",
                    "description": "Muestra las comisiones"
                },
                {
                    "label": "Cristales",
                    "value": "1",
                    "description": "Muestra tus cristales"
                },
                {
                    "label": "Tree perks",
                    "value": "2",
                    "description": "Tu arbol"
                },
                {
                    "label": "Powder y Perks",
                    "value": "3",
                    "description": "Cantidad de powder y niveles de perks"
                }
            ],
            "placeholder": "Elige un tipo"
        }
        comp = {
            "type": 1,
            "components": [new_com]
        }
        componentes.append(comp)
        msg = await msg.reply('**Cargando...**', components=componentes)
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
        for_embed_data = {}
        embed = discord.Embed(title=title, description = description, color=color)
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        embed.set_thumbnail(url=url)
        for_embed_data['title'] = title
        for_embed_data['description'] = description
        for_embed_data['color'] = color
        for_embed_data['tumb'] = url
        for_embed_data['fields'] = []
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
                    for_embed_data['fields'].append([name, value, False])
                    embed.add_field(name=name, value=value, inline=False)
            else:
                if tokens_totales == 15:
                    name = f':partying_face: :partying_face: :partying_face:'
                    value = '```'
                    value += f'Hotm al maximo Felicidades\n'
                    value += '```'
                    for_embed_data['fields'].append([name, value, False])
                    embed.add_field(name=name, value=value, inline=False)
                else:
                    name = f'Hotm al nivel maximo'
                    value = '```'
                    value += f'Aun puedes conseguir {15 - tokens_totales} tokens\n'
                    value += '```'
                    for_embed_data['fields'].append([name, value, False])
                    embed.add_field(name=name, value=value, inline=False)
        else:
            pass
        text = f'Pagina 1/{mensajes_totales}'
        dropeos_hall = self.dropeo_hall(original_msg)
        if dropeos_hall[0]:
            text += dropeos_hall[1]
        embed.set_footer(text = text)
        await msg.edit(content = '', embed = embed)
        for_embed_data['footer'] = text
        mensajes.append(embed)
        embeds_data.append(for_embed_data)
        for_embed_data = {}
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
            url=f'https://crafatar.com/renders/body/{uuid}?size=40'
            embed.set_thumbnail(url = url)
            for_embed_data['title'] = title
            for_embed_data['description'] = description
            for_embed_data['color'] = color
            for_embed_data['tumb'] = url
            for_embed_data['fields'] = []
            for fiel in data_for_fields:
                embed.add_field(name=fiel[0], value=fiel[1], inline=False)
                for_embed_data['fields'].append([fiel[0], fiel[1], False])
            text = f'Pagina 2/{mensajes_totales}'
            embed.set_footer(text = text)
            for_embed_data['footer'] = text
            mensajes.append(embed)
            embeds_data.append(for_embed_data)
            for_embed_data = {}
        else:
            description = f'Sin nivel para acceder a las crystal hollows'
            embed = discord.Embed(title=title,  description=description, color=color)
            embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
            text = f'Pagina 2/{mensajes_totales}'
            embed.set_footer(text = text)
            for_embed_data['title'] = title
            for_embed_data['description'] = description
            for_embed_data['color'] = color
            for_embed_data['tumb'] = f'https://crafatar.com/renders/body/{uuid}?size=40'
            for_embed_data['footer'] = text
            mensajes.append(embed)
            embeds_data.append(for_embed_data)
            for_embed_data = {}
        
        # ------------------------- Imagen de perks -----------------------------
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        tree_1, data_to_embed = self.perks_tree(data, title, color, level, url = url)
        embeds_data.append(data_to_embed[0])
        embeds_data.append(data_to_embed[1])
        mensajes.append(tree_1[0])
        mensajes.append(tree_1[1])
        
        self.msg = msg
        self.original_msg = original_msg
        
        await self.esperando_boton_embed(msg, mensajes, menu = True)

    def perks_tree(self, data, title, color, nivel, url = ''):
        def replaces_hotm(text):
            replaces = {
                'mining_experience': 'seasoned_mineman',
                'random_event': 'sky_mall',
                'special_0': 'Peak of the Mountain',
                'forge_time': 'Quick Forge',
                '_': ' '
            }
            for key, value in replaces.items():
                text = text.replace(key, value)
            return text
            
        path = pathlib.Path().resolve()
        coal = "<:coal:893388568091844619>"
        esmeralda = "<:emerald:893388567970197515>"
        glass = "<:glass_gray:893388568255426562>"
        diamond = "<:diamond:893587666069778492>"

        # emoji red / green / black / blue circles
        #coal = ":red_circle:"
        #esmeralda = ":green_circle:"
        #glass = ":black_circle:"
        #diamond = ":blue_circle:"

        nodes = data['nodes']
        #print(nodes)
        unique_name = ''
        perks_info = {
            1: {
                'mining_speed': 50
            },
            2: {
                'mining_fortune': 50,
                'titanium_insanium': 50,
                'forge_time': 20,
                'mining_speed_boost': 1,
                'pikobulus': 1
            },
            3: {
                'daily_powder': 100,
                'random_event': 45,
                'crystallized': 30
            },
            4: {
                'efficient_miner': 100,
                'mining_experience': 100,
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
            nivel_2 = ['void', 'mining_speed_boost', 'titanium_insanium', 'mining_fortune', 'forge_time', 'pikobulus', 'void']
            nivel_3 = ['void', 'random_event', 'void', 'daily_powder', 'void', 'crystallized', 'void']
            nivel_4 = ['sky_mall', 'mining_madness', 'mining_experience', 'efficient_miner', 'orbiter', 'front_loaded', 'precision_mining']
            nivel_5 = ['void', 'goblin_killer', 'void', 'special_0', 'void', 'star_powder', 'void']
            nivel_6 = ['vein_seeker', 'lonesome_miner', 'professional', 'mole', 'fortunate', 'great_explorer', 'maniac_miner']
            nivel_7 = ['void', 'mining_speed_2', 'void', 'powder_buff', 'void', 'mining_fortune_2', 'void']
            niveles = [nivel_1, nivel_2, nivel_3, nivel_4, nivel_5, nivel_6, nivel_7]
            mensaje = ''
            mensaje_niveles = []
            for i in range(0, 7):                
                lvl = niveles[i]
                msg_lvl = f'{i +1}: \t'
                name_for_level = f'Nivel hotm: {i + 1}\t'
                value_for_level = ''
                for perk in lvl:
                    if perk == 'void':
                        msg_lvl += f'\t{glass}\t'
                    elif perk in nodes:
                        if nodes[perk] >= perks_info[i+1][perk]:
                            msg_lvl += f'\t{diamond}\t'
                            value_for_level += f'{replaces_hotm(perk.lower()).capitalize()}: lvl `{nodes[perk]} maxeada`\n'
                        else:
                            msg_lvl += f'\t{esmeralda}\t'
                            value_for_level += f'{replaces_hotm(perk.lower()).capitalize()}: lvl `{nodes[perk]}`\n'
                        unique_name += f'{perk}'
                    else:
                        msg_lvl += f'\t{coal}\t'
                mensaje_niveles.append([name_for_level, value_for_level])
                mensaje = f'\n{msg_lvl}\n{mensaje}\n'
                
            if unique_name != '':
                self.arboles_previos[f'{unique_name}'] = mensaje
        # ------------------------- embed -----------------------------
        regresar = []
        embeds = []
        data_to_embed = {}
        mensaje = self.arboles_previos[f'{unique_name}']
        description = mensaje
        embed = discord.Embed(title=title,  description=description, color=color)
        embed.set_thumbnail(url=url)
        text = f'Pagina 3/4'
        embed.set_footer(text = text)
        data_to_embed['title'] = title
        data_to_embed['description'] = description
        data_to_embed['color'] = color
        data_to_embed['tumb'] = url
        data_to_embed['footer'] = text
        regresar.append(data_to_embed)
        embeds.append(embed)

        # ---------------------- Datos de nivel por perk --------------------
        # mensaje_niveles
        data_to_embed = {}
        mensaje = f'Niveles de perk'
        description = mensaje
        embed = discord.Embed(title=title,  description=description, color=color)
        embed.set_thumbnail(url=url)
        text = f'Pagina 4/4'
        embed.set_footer(text = text)
        data_to_embed['title'] = title
        data_to_embed['description'] = description
        data_to_embed['color'] = color
        data_to_embed['tumb'] = url
        data_to_embed['footer'] = text
        data_to_embed['fields'] = []

        for nivel_perk in mensaje_niveles:
            name = nivel_perk[0]
            value = nivel_perk[1]
            if value == '':
                value = 'Sin perks activos en este nivel'
            embed.add_field(name=name, value=value, inline=False)
            data_to_embed['fields'].append([name, value, False])

        # ---------------------- Powders --------------------
                    # ------ Mithril ------
        try:
            powder_mithril = data['powder_mithril']
        except:
            powder_mithril = 0
        try:
            powder_spent_mithril = data['powder_spent_mithril']
        except:
            powder_spent_mithril = 0
        total_mithril = powder_mithril + powder_spent_mithril
        powder_mithril = self.calculadora(f'{powder_mithril} + 0', entero = True)
        powder_spent_mithril = self.calculadora(f'{powder_spent_mithril} + 0', entero = True)
        total_mithril = self.calculadora(f'{total_mithril} + 0', entero = True)

                    # ------ Gemstone ------
        try:
            powder_gemstone = data['powder_gemstone']
        except:
            powder_gemstone = 0
        try:
            powder_spent_gemstone = data['powder_spent_gemstone']
        except:
            powder_spent_gemstone = 0
        total_gemstone = powder_gemstone + powder_spent_gemstone
        powder_gemstone = self.calculadora(f'{powder_gemstone} + 0', entero = True)
        powder_spent_gemstone = self.calculadora(f'{powder_spent_gemstone} + 0', entero = True)
        total_gemstone = self.calculadora(f'{total_gemstone} + 0', entero = True)

        name = 'Powder Mithril'
        value = ''
        value += '```cs\n'
        value += f'Disponible: "{powder_mithril}"\n'
        value += f'Gastada: "{powder_spent_mithril}"\n'
        value += f'Total: "{total_mithril}"\n'
        value += '```'
        embed.add_field(name=name, value=value, inline=False)
        data_to_embed['fields'].append([name, value, False])

        name = 'Powder Gemstone'
        value = ''
        value += '```ini\n'
        value += f'Disponible: [{powder_gemstone}]\n'
        value += f'Gastada: [{powder_spent_gemstone}]\n'
        value += f'Total: [{total_gemstone}]\n'
        value += '```'
        embed.add_field(name=name, value=value, inline=False)
        data_to_embed['fields'].append([name, value, False])

        regresar.append(data_to_embed)
        embeds.append(embed)
        return embeds, regresar
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Hotm(bot))
