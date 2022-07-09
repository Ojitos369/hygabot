import json
import discord
from datetime import datetime

from discord import embeds
from funciones.generales import Generales, Item
class Talismanes(Generales):

    def talismanes(self, msg = '', text = '', datos = False):
        self.config()
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
        
        # -------------- Verificando talismanies por pagina ----------------
        posicion = -1
        talis_por_pagina = 10
        for i in range(len(separado)):
            if separado[i] == '-c' or  separado[i] == '-cantidad':
                try:
                    talis_por_pagina = int(separado[i+1])
                    posicion = i
                    break
                except:
                    return msg.reply('Despues de -c se espera un numero de la lista. Ejemplo: -p 10')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        if talis_por_pagina > 20:
            return msg.reply('La cantidad maxima de talismanes por pagina es 20')
        if talis_por_pagina < 1:
            talis_por_pagina = 1

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
            talismanes_data = datos["talisman_bag"]["data"]
        except:
            if interno:
                return 'verApi'
            else:
                return msg.reply(f'Revise que la API de inventario este activa')

        # -------------- Decodicicacion de datos ----------------
        username = self.for_tsuru(username)
        data = Item.decode_inventory_data(talismanes_data)["i"]
        color = self.color_aleatorio()
        value = ''
        numero_de_talismanes = 0
        mensajes = []
        talis_data = []
        recomb_emoji = self.recomb_item()
        for talisman in data:
            try:
                lore_data = talisman['tag']['display']['Lore']
                lore = lore_data.pop()
                lore = self.remplazar(lore)
                name = self.remplazar(talisman['tag']['display']['Name'])
                name = self.get_emoji_name(name)
                try:
                    recombulado = talisman['tag']['ExtraAttributes']['rarity_upgrades']
                    name = f'{numero_de_talismanes + 1}.- {name}{recomb_emoji}\n'
                except:
                    name = f'{numero_de_talismanes + 1}.- {name}\n'
                numero_de_talismanes += 1
                talis_data.append([name, lore])
            except:
                break
        description = f'Cuenta con {numero_de_talismanes} talismanes'
        talis_en_pagina = 0
        paginas_totales = (numero_de_talismanes // talis_por_pagina) + 1
        pagina = 1
        embed = discord.Embed(title=f'Talismanes de {username}',description=description, color=color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
        embed.set_footer(text=f'Pagina {pagina} de {paginas_totales}')
        for i in range(len(talis_data)):
            name = talis_data[i][0]
            value = f'`{talis_data[i][1]}`'
            embed.add_field(name=name, value=value, inline=False)
            talis_en_pagina += 1
            if talis_en_pagina == talis_por_pagina:
                mensajes.append(embed)
                talis_en_pagina = 0
                pagina += 1
                embed = discord.Embed(title=f'Talismanes de {username}',description=description, color=color)
                embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
                embed.set_footer(text=f'Pagina {pagina} de {paginas_totales}')
        if talis_en_pagina != 0:
            mensajes.append(embed)

        return mensajes

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'talismanes': self.talismanes,
            'talis': self.talismanes,
            'tal': self.talismanes,
            'accesorios': self.talismanes,
            'accesorio': self.talismanes,
            'ac': self.talismanes,
        }