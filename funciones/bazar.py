import json
from datetime import datetime
import discord
from funciones.generales import Generales

class Bazar(Generales):
    bazar_data = ['', 0]
    fecha_de_actualizacion = ''
    npc_data = {}

    def bazar(self, msg = '', text = '', for_minions = False):
        self.config()
        if len(text) > 0:
            busquedas = text.split()
        else:
            return msg.reply('Ingresa una busqueda valida')

        cantidades_pos = -1
        cantidad = 1
        for i in range(len(busquedas)):
            if busquedas[i] == '-c' or busquedas[i] == '-cantidad':
                try:
                    cantidad = int(busquedas[i + 1])
                except:
                    return msg.reply('Despues de -c va una cantidad. Ejemplo: -c 5')
                cantidades_pos = i
        if cantidades_pos != -1:
            busquedas.pop(cantidades_pos + 1)
            busquedas.pop(cantidades_pos)
        if '*' in busquedas and msg.author.id not in self.developers_ids:
            return msg.reply('Busqueda * solo disponible en desarrollo')
        link_base = f'https://api.hypixel.net/skyblock/bazaar'
        ahora_hora = int(datetime.now().strftime('%H')) * 60
        ahora_minutos = int(datetime.now().strftime('%M'))
        ahora = ahora_hora + ahora_minutos
        if self.bazar_data[0] == '':
            self.bazar_data[0] = int(ahora) + 10
            self.fecha_de_actualizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if abs(int(self.bazar_data[0]) - int(ahora)) > 5:
            primero = f'{link_base}?key='
            segundo = f''
            hydata = self.consulta(primero, segundo)
            self.bazar_data[0] = ahora
            self.bazar_data[1] = hydata
            self.fecha_de_actualizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            hydata = self.bazar_data[1]
        productos = hydata['products']

        # ----------------- Regresarndo datos internos para los minions ----------------- #
        if for_minions:
            return productos
        resultados = []
        numero_de_resultados = 0
        for nombre, datos in productos.items():            
            encontrado = True
            # ----------------- Buscar coincidencias en bazar data ----------------- #
            for busqueda in busquedas:
                if busqueda.lower() not in self.extra_replace(nombre.lower()).lower():
                    encontrado = False
            if busqueda[0] == '*':
                encontrado = True
            try:
                if encontrado:
                    item_name = self.extra_replace(datos['product_id'].lower()).capitalize().replace('_', ' ')
                    item_name = self.get_emoji_name(item_name)
                    insta = datos['quick_status']
                    buy_order = float(datos["sell_summary"][0]['pricePerUnit']) * cantidad
                    sell_order = float(datos["buy_summary"][0]['pricePerUnit']) * cantidad
                    sell_insta = float(insta['sellPrice']) * cantidad
                    buy_insta = float(insta['buyPrice']) * cantidad
                    datos_item = {
                        'buy_order': buy_order,
                        'sell_order': sell_order,
                        'sell_insta': sell_insta,
                        'buy_insta': buy_insta,
                    }
                    resultados.append([item_name, datos_item])
                    numero_de_resultados += 1
            except:
                pass
        
        if numero_de_resultados > 0:
            mensaje = []
            elementos_en_mensaje = 1
            elementos_maximos_por_pagina = 5
            elemento_mostrado = 1
            color = self.color_aleatorio()
            paginas_totales = numero_de_resultados // elementos_maximos_por_pagina + 1
            pagina = 1
            embed = discord.Embed(title = f'Resultado para {" ".join(busquedas)}', color = color)
            for nombre, datos in resultados:
                if cantidad > 1:
                    name = f'{nombre} - x{cantidad}'
                else:
                    name = f'{elemento_mostrado}/{numero_de_resultados}.- {nombre}'
                    elemento_mostrado += 1
                value = '```'
                value += f"Buy Order: " + "{:,.2f}".format(datos['buy_order']) + "\n"
                value += f"Sell Order: " + "{:,.2f}".format(datos['sell_order']) + "\n"
                value += f"flip: """ + "{:,.2f}".format(datos['sell_order'] - datos['buy_order']) + "\n"                
                value += f"\nInsta Buy: " + "{:,.2f}".format(datos['buy_insta']) + "\n"
                value += f"Insta Sell: " + "{:,.2f}".format(datos['sell_insta']) + "\n"
                value += f"flip: " + "{:,.2f}".format(datos['sell_insta'] - datos['buy_insta'])
                value += '```'
                embed.add_field(name = name, value = value, inline = False)
                if elementos_en_mensaje == elementos_maximos_por_pagina:
                    footer = f'Ultima actualizacion: {self.fecha_de_actualizacion}.\n Pagina {pagina}/{paginas_totales}'
                    embed.set_footer(text = footer)
                    mensaje.append(embed)
                    embed = discord.Embed(title = f'Resultado para {" ".join(busquedas)}', color = color)
                    elementos_en_mensaje = 1
                    pagina += 1
                elementos_en_mensaje += 1
        else:
            return msg.reply('No se encontraron resultados')
        
        footer = f'Ultima actualizacion: {self.fecha_de_actualizacion}.\n Pagina {pagina}/{paginas_totales}'
        embed.set_footer(text = footer)
        mensaje.append(embed)
        return mensaje

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]
        
        #open npc_sells.json
        self.funciones = {
            'bz': self.bazar,
            'bazar': self.bazar,
        }
