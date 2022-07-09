from datetime import datetime
from time import sleep
from mojang import MojangAPI
import requests
import json
import discord
import pandas as pd
from funciones.generales import Generales, Item

class Inventarios(Generales):
    def inventario(self, msg, text, datos = None):
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
        # open(f'./{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
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
            inv = datos["inv_contents"]["data"]
        except:
            if interno:
                return 'verApi'
            else:
                return msg.reply(f'Revise que la API de inventario este activa en {perfil_name}')

        # -------------- Decodicicacion de datos ----------------
        username = self.for_tsuru(username)
        data = Item.decode_inventory_data(inv)["i"]
        inventario = ''
        total = []
        numero_items = 1
        totales = 0
        for dato in data:
            if "tag" in dato:
                nombre = self.remplazar(dato["tag"]["display"]["Name"])
                if nombre != 'SkyBlock Menu (Right Click)':
                    totales += 1

        
        numero_busqueda = False
        for i in range(1, totales + 1):
            if i == numero_item:
                numero_busqueda = True
        if not numero_busqueda and numero_item != 0:
            return msg.reply(f'Revisa que el numero de item existe con "{self.prefijo}inv {username}"')
        if numero_item == 0: detallado = False

        # -------------- Agregado de datos a una lista ----------------
        full_datos = []
        for dato in data:
            if numero_item == 0:
                aux = numero_items
            else:
                aux = numero_item
            if "tag" in dato:
                cantidad = dato["Count"]
                item_name = self.remplazar(dato["tag"]["display"]["Name"])
                item_name = self.get_emoji_name(item_name)
                if cantidad > 1:
                    item_name += f" - x{cantidad}"
                nombre = item_name
                if nombre != 'SkyBlock Menu (Right Click)':
                    if numero_items == aux:
                        lore = ''
                        full_lore = dato["tag"]["display"]["Lore"]
                        dato_extra = full_lore.pop()
                        dato_extra = self.remplazar(dato_extra)
                        for lor in full_lore:
                            lore += f'{self.remplazar(lor)}\n'
                        extra_datos = dato["tag"]["ExtraAttributes"]
                        try: 
                            if extra_datos['rarity_upgrades'] == 1:
                                lore += f'Item Recombulado\n'
                                nombre += ' ' + self.recomb_item()
                        except:
                            pass
                        try:
                            lore += f'Hot potato books: {extra_datos["hot_potato_count"]}\n'
                        except:
                            pass
                        try:
                            gemas = extra_datos["gems"]
                            try:
                                lore += f'Gemas Aplicadas: {gemas["UNIVERSAL_0"]} {gemas["UNIVERSAL_0_gem"]}\n'
                            except:
                                lore += f'Gemas Aplicadas:\n'
                                if "JADE_0" in gemas:
                                    lore += f'\t{gemas["JADE_0"]} JADE\n'
                                if "AMBER_0" in gemas:
                                    lore += f'\t{gemas["AMBER_0"]} AMBER\n'
                                if "SAPPHIRE_0" in gemas:
                                    lore += f'\t{gemas["SAPPHIRE_0"]} SAPPHIRE\n'
                                if "AMETHYST_0" in gemas:
                                    lore += f'\t{gemas["AMETHYST_0"]} AMETHYST\n'
                                if "TOPAZ_0" in gemas:
                                    lore += f'\t{gemas["TOPAZ_0"]} TOPAZ\n'
                        except:
                            pass
                        if detallado:
                            # ------- Agregado de datos al item en detalle --------
                            color = self.color_aleatorio()
                            embed = discord.Embed(title = f'{numero_items}/{totales}.- {nombre}', description = f'```{lore}```', color = color)
                            embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
                            embed.add_field(name = 'Tipe', value = f'```{dato_extra}```', inline = False)
                            total.append(msg.reply(embed = embed))
                            inventario += f'{nombre}\n'
                        elif interno:
                            full_datos.append(
                                {
                                    'nombre': nombre,
                                    'lore': lore,
                                    'extra': dato_extra
                                }
                            )
                        else:
                            # ------- Agregado Items sin detalle --------
                            inventario += f'{numero_items}.- {nombre}\n'
                    numero_items += 1
        # -------------- Regreso para peticion interna ---------------
        if interno:
            return full_datos
        # -------------- Regresando en general ----------------
        if not detallado:
            color = self.color_aleatorio()
            embed = discord.Embed(title = f"{username}'s Inventory", description = inventario, color = color)
            embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
            total = msg.reply(embed = embed)
        
        return total

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]
        self.funciones = {
            'inventario': self.inventario,
            'inventory': self.inventario,
            'i': self.inventario,
            'inv': self.inventario
        }