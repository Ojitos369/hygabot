import json
import discord
import pandas as pd
from datetime import datetime
from funciones.generales import Generales
class Pets(Generales):

    def acomodar_lista(self, lista, llave):
        acomodado = []
        for elemento in lista:
            if len(acomodado) == 0:
                acomodado.append(elemento)
            else:
                for i in range(len(acomodado)):
                    if elemento[llave] > acomodado[i][llave]:
                        acomodado.insert(i, elemento)
                        break
                    elif i == len(acomodado) - 1:
                        acomodado.append(elemento)
        return acomodado

    def pets(self, msg = '', text = '', datos = False):
        #return msg.reply("Comando en desarrollo :3")
        # -------------- Separacion de datos buscando opciones y usuario ----------------
        text = self.correccion_opciones(text)
        separado = text.split()
        numero_item = 0
        detallado = False
        interno = False
        # -------------- Verificando Detallado ----------------
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-d' or  separado[i] == '-detalles' or  separado[i] == '-detallado':
                try:
                    numero_item = int(separado[i+1])
                    posicion = i
                    detallado = True
                    break
                except:
                    return msg.reply('Despues de -d se espera un numero de la lista. Ejemplo: -d 1')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        
        # -------------- Verificando Numero por pagina ----------------
        posicion = -1
        pets_por_pagina = 10
        for i in range(len(separado)):
            if separado[i] == '-c' or  separado[i] == '-cantidad':
                try:
                    pets_por_pagina = int(separado[i+1])
                    posicion = i
                    break
                except:
                    return msg.reply('Despues de -c se espera un numero. Ejemplo: -p 10')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        if pets_por_pagina < 1:
            pets_por_pagina = 1
        if pets_por_pagina > 25:
            msg.reply('La cantidad maxima de pets por pagina es 25')

        # -------------- Verificando Interno ----------------
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-solicitud_interna':
                posicion = i
                interno = True
                break
        if posicion != -1:
            separado.pop(posicion)

        username = separado[0]
        if not interno:
            try:
                username = self.get_username(username)
            except:
                return msg.reply('Revise que el usuario este bien escrito')
            
        perfil_name = ''
        if len(separado) > 1:
            perfil_name = separado[1]

        # -------------- Obtencion de datos ----------------
        if not interno:
            try:
                datos, perfil_name, uuid = self.obtener_perfil(username, perfil_name, uuid = True)
            except:
                datos = self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        #open(f'./{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            if interno:
                return 'usuario'
            return msg.reply('Verifica que el Usuario este bien escrito')
        if datos == 'perfil':
            if interno:
                return 'perfil'
            return msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')

        # -------------- Verificcacion de la api de inventario ------------------
        try:
            pets = datos["pets"]
        except:
            if interno:
                return 'verApi'
            else:
                return msg.reply(f'Revise que la API de inventario este activa')

        # -------------- Decodicicacion de datos ----------------
        # open pet_xp_levels.json
        pet_xp_levels = json.loads(open('./json/pet_xp_levels.json', 'r').read())
        pets_data = []
        for pet in pets:
            rareza = pet["tier"].lower()
            xp_pet = pet['exp']
            activo = pet['active']
            if xp_pet < 5000:
                nivel = 1
            else:
                nivel = 100
            candies = pet['candyUsed']
            skin = pet['skin']
            try:
                item = pet['heldItem'].lower().replace('_', ' ')
                item = item.replace('pet item ', '')
                item = item.replace('skill', 'exp')
                item = item.capitalize()
                emoji_item = self.get_emoji_name(item).replace(item, '')
            except:
                item = None
                emoji_item = ''
            for i in range(1, 100):
                if xp_pet >= pet_xp_levels[rareza.replace('mythic', 'legendary')][str(i)] and xp_pet < pet_xp_levels[rareza.replace('mythic', 'legendary')][str(i+1)]:
                    nivel = i
                    break
            try:
                next_level_xp = pet_xp_levels[rareza.replace('mythic', 'legendary')][str(nivel + 1)]
            except:
                next_level_xp = -1
            name = f'[Lvl {nivel}] ' + rareza.capitalize() + ' ' + pet["type"].lower().replace('_', ' ').capitalize() + ' Pet '
            if activo:
                name = self.get_emoji_name(f'_**`{name}`**_')  + ' ' + emoji_item
            else:
                name = self.get_emoji_name(f'{name}')  + ' ' + emoji_item
            
            pets_data.append({
                'nombre': name,
                'nivel': nivel,
                'activo': activo,
                'xp': xp_pet,
                'xp_para_siguiente_nivel': next_level_xp,
                'candies': candies,
                'skin': skin,
                'item': item
            })
        # -------------- Ordenacion de datos ----------------
        pet_activo = []
        pets_mythic = []
        pets_legendary = []
        pets_epic = []
        pets_rare = []
        pets_uncommon = []
        pets_common = []
        for i in range(len(pets_data)):
            pet = pets_data[i]
            if pet['activo']:
                pet_activo = [pets_data[i]]
                pets_data.pop(i)
                break
        
        for pet in pets_data:
            if 'mythic' in pet['nombre'].lower():
                pets_mythic.append(pet)
            elif 'legendary' in pet['nombre'].lower():
                pets_legendary.append(pet)
            elif 'epic' in pet['nombre'].lower():
                pets_epic.append(pet)
            elif 'rare' in pet['nombre'].lower():
                pets_rare.append(pet)
            elif 'uncommon' in pet['nombre'].lower():
                pets_uncommon.append(pet)
            else:
                pets_common.append(pet)
        
            # -------- Ordenando por nivel de alto a bajo --------

        pets_mythic = self.acomodar_lista(pets_mythic, 'nivel')
        pets_legendary = self.acomodar_lista(pets_legendary, 'nivel')
        pets_epic = self.acomodar_lista(pets_epic, 'nivel')
        pets_rare = self.acomodar_lista(pets_rare, 'nivel')
        pets_uncommon = self.acomodar_lista(pets_uncommon, 'nivel')
        pets_common = self.acomodar_lista(pets_common, 'nivel')

        pets_data = pet_activo + pets_mythic + pets_legendary + pets_epic + pets_rare + pets_uncommon + pets_common

        # -------------- Ordenacion de datos ----------------

        
        
        # -------------- Creacion de embed ----------------
        numero_de_pets = len(pets_data)
        mensajes = []
        paginas = int(numero_de_pets / pets_por_pagina) + 1
        color = self.color_aleatorio()
        numero_de_pet = 0
        numero_de_pagina = 1
        embed = discord.Embed(title=f'{username} {perfil_name}', color=color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
        aux = 1
        
        for i in range(numero_de_pets):
            pet = pets_data[i]
            name = f'{aux}.- {pet["nombre"]}'
            value = '```'
            if pet['activo']:
                value += f'Pet Activo\n'
            xp_actual = f'{pet["xp"]:,.0f}'
            
            if pet['xp_para_siguiente_nivel'] != -1:
                xp_siguiente = f'{pet["xp_para_siguiente_nivel"]:,.0f}'
                xp_faltante = f'{pet["xp_para_siguiente_nivel"] - pet["xp"]:,.0f}'
                value += f'XP: {xp_actual}/{xp_siguiente}\n'
                value += f'Falta: {xp_faltante} para el nivel {pet["nivel"] + 1}\n'
            else:
                value += f'XP: {xp_actual}\n'
                value += f'Pet Maxeada\n'
            if pet['candies'] != 0:
                value += f'Candies: {pet["candies"]}\n'
            if pet['skin'] != None:
                value += f'Skin: {pet["skin"]}\n'
            if pet['item'] != None:
                value += f'Item: {pet["item"]}\n'
            value += '```'
            embed.add_field(name=name, value=value, inline=False)
            aux += 1
            if numero_de_pet + 1 == pets_por_pagina:
                mensajes.append(embed)
                numero_de_pet = 0
                numero_de_pagina += 1
                embed = discord.Embed(title=f'{username} {perfil_name}', color=color)
                embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
            numero_de_pet += 1
        if numero_de_pet != 1:
            mensajes.append(embed)
        for i in range(len(mensajes)):
            text = f'Pagina {i + 1}/{len(mensajes)}'
            mensajes[i].set_footer(text=text)
        return mensajes

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'pet': self.pets,
            'pets': self.pets
        }
