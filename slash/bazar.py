import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from slash.generales import Generales

class Bazar(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot

    bazar_data = ['', 0]
    fecha_de_actualizacion = ''

    @cog_ext.cog_slash(name="bazar", description="Muestra datos del bazar", options = [
        create_option(
            name = "busqueda",
            description = "Busqueda a realizar",
            option_type = 3,
            required = True,
        ),
        create_option(
            name = "cantidad",
            description = "Cantidad de elementos a evaluar",
            option_type = 4,
            required = False,
        )
    ])
    async def bazar(self, msg: SlashContext, busqueda: str, cantidad: int = 1):
        self.config()
        busquedas = busqueda.split()
        msg_original = msg
        if '*' in busquedas and msg.author.id not in self.developers_ids:
            await msg.reply('Busqueda * solo disponible en desarrollo')
            return

        link_base = f'https://api.hypixel.net/skyblock/bazaar'
        ahora_hora = int(datetime.now().strftime('%H')) * 60
        ahora_minutos = int(datetime.now().strftime('%M'))
        ahora = ahora_hora + ahora_minutos
        msg = await msg.reply('Buscando...')
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
        resultados = []
        numero_de_resultados = 0
        for nombre, datos in productos.items():            
            encontrado = True
            # ----------------- Buscar coincidencias en bazar data ----------------- #
            name = datos['product_id']
            item_name = self.bazar_replace(name)
            for busqueda in busquedas:
                if busqueda.lower() not in item_name.lower():
                    encontrado = False
            if busqueda == '*':
                encontrado = True
            try:
                if encontrado:
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
        dropeos_hall = self.dropeo_hall(msg_original)
        if numero_de_resultados > 0:
            mensaje = []
            elementos_en_mensaje = 1
            elementos_maximos_por_pagina = 5
            elemento_mostrado = 1
            color = self.color_aleatorio()
            paginas_totales = numero_de_resultados // elementos_maximos_por_pagina + 1
            pagina = 1
            embeds_data = []
            for_embed = {}
            title = f'Resultado para {" ".join(busquedas)}'
            embed = discord.Embed(title = title, color = color)
            for_embed['title'] = title
            for_embed['color'] = color
            for_embed['fields'] = []
            for nombre, datos in resultados:
                if cantidad > 1:
                    name = f'{nombre} - x{cantidad}'
                else:
                    name = f'{elemento_mostrado}/{numero_de_resultados}.- {nombre}'
                    elemento_mostrado += 1
                value = '```'
                value += f"Buy Order: " + "{:,.2f}".format(datos['buy_order']) + f"({self.redondear_letras(datos['buy_order'])})\n"
                value += f"Sell Order: " + "{:,.2f}".format(datos['sell_order']) + f"({self.redondear_letras(datos['sell_order'])})\n"
                value += f"flip: """ + "{:,.2f}".format(datos['sell_order'] - datos['buy_order']) + f" ({self.redondear_letras(datos['sell_order'] - datos['buy_order'])})\n"
                value += f"\nInsta Buy: " + "{:,.2f}".format(datos['buy_insta']) + f"({self.redondear_letras(datos['buy_insta'])})\n"
                value += f"Insta Sell: " + "{:,.2f}".format(datos['sell_insta']) + f"({self.redondear_letras(datos['sell_insta'])})\n"
                value += f"flip: " + "{:,.2f}".format(datos['sell_insta'] - datos['buy_insta']) + f" ({self.redondear_letras(datos['sell_insta'] - datos['buy_insta'])})"
                value += '```'
                for_embed['fields'].append([name, value, False])
                embed.add_field(name = name, value = value, inline = False)
                if elementos_en_mensaje == elementos_maximos_por_pagina:
                    footer = f'Ultima actualizacion: {self.fecha_de_actualizacion}.\n Pagina {pagina}/{paginas_totales}'
                    if dropeos_hall[0]:
                        footer += dropeos_hall[1]
                    embed.set_footer(text = footer)
                    mensaje.append(embed)
                    for_embed['footer'] = footer
                    embeds_data.append(for_embed)
                    for_embed = {}
                    for_embed['title'] = title
                    for_embed['color'] = color
                    for_embed['fields'] = []
                    embed = discord.Embed(title = f'Resultado para {" ".join(busquedas)}', color = color)
                    elementos_en_mensaje = 1
                    pagina += 1
                elementos_en_mensaje += 1
        else:
            await msg.edit(content = 'No se encontraron resultados')
            return
        
        footer = f'Ultima actualizacion: {self.fecha_de_actualizacion}.\n Pagina {pagina}/{paginas_totales}'
        if dropeos_hall[0]:
            footer += dropeos_hall[1]
        embed.set_footer(text = footer)
        mensaje.append(embed)
        for_embed['footer'] = footer
        embeds_data.append(for_embed)
        await msg.edit(content = '', embed=mensaje[0])
        user_id = msg_original.author.id
        id_mensaje = msg.id
        guardar = {
            'msg_id': id_mensaje,
            'user_id': user_id,
            'embeds': embeds_data,
        }
        open(f'./embeds_data/emb_data.json', 'w').write(json.dumps(guardar, indent=4))
        await msg.channel.send(f'+load {id_mensaje}')
        if len(embeds_data) > 1:
            await msg.add_reaction('\U000025B6')

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Bazar(bot))