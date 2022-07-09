import json
import discord
import pandas as pd
from datetime import datetime
from mojang import MojangAPI
from funciones.generales import Generales, Item

class Ah_player(Generales):
    def ah_player(self, msg = '', text = ''):
        self.config()
        separado = text.split(' ')
        username = separado[0]
        try:
            username = self.get_username(username)
        except:
            return msg.reply('Revise que el usuario este bien escrito')
            
        extendido = False
        # ---- Verificar extendido ----
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-extendido' or separado[i] == '-e':
                posicion = i
                break
        if posicion != -1:
            extendido = True
            separado.pop(posicion)
        try:
            perfil_name = separado[1]
        except:
            perfil_name = ''
        fecha_de_actualizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        link_base = 'https://api.hypixel.net/skyblock/auction'
        perfil_id = self.obtener_perfil(username, perfil_name, id = True)
        primero = f'{link_base}?key='
        segundo = f'&profile={perfil_id}'

        try:
                datos, perfil_name, uuid = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        if datos == 'usuario':
            return msg.reply('Verifica que el Usuario este bien escrito')
        if datos == 'perfil':
            return msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')
        del(datos)

        player = self.consulta(primero, segundo)
        
        try:
            auctions = player['auctions']
            #open(f'./info_pruebas/{username}_auctions.json', 'w').write(json.dumps(auctions, indent = 4))
        except:
            print('debug')
        username = self.for_tsuru(username)
        resultados = 0
        ganancias_totales = 0
        elementos = []
        for elemento in auctions:
            mostrar = True
            termino = self.obtener_tiempo_relativo(elemento['end'])
            dias = termino.split(' ')[0]
            try:
                aux = int(dias)
            except:
                aux = 0

            if aux < -3:
                mostrar = False
            pasado = False
            if '-' in termino:
                termino = self.obtener_tiempo_relativo_inverso(elemento['end'])
                pasado = True
            
            if mostrar:
                item_bytes = Item.decode_inventory_data(elemento['item_bytes']['data'])['i'][0]
                cantidad = item_bytes['Count']
                item_name = elemento['item_name']
                item_name = self.get_emoji_name(item_name)
                if cantidad > 1:
                    item_name += f" - x{cantidad}"

                enbin = 'Auction'
                try:
                    if elemento['bin']:
                        enbin = f'Bin {self.auction_emoji("bin_only")}'
                        precio_actual = elemento['starting_bid']
                except:
                    enbin = 'Auction {self.auction_emoji("auction_only")}'
                    if float(elemento['highest_bid_amount']) != 0:
                        precio_actual = elemento['highest_bid_amount']
                    else:
                        precio_actual = elemento['starting_bid']
                lore = self.remplazar(elemento['item_lore'])
                tier = elemento['tier']
                tier_emoji = self.auction_emoji(f'{tier}-in')
                item_name = f'{item_name} {tier_emoji}'
                tier += f' {tier_emoji}'
                try:
                    if len(elemento['claimed_bidders'][0]) > 2:
                        reclamado = 'Vendido'
                    else:
                        reclamado = 'No Vendido'
                except:
                    reclamado = 'No Vendido'
                try:
                    if len(elemento['claimed_bidders'][0]) > 2:
                        ganancias = elemento['highest_bid_amount']
                        ganancias_totales += ganancias
                        ganancias = '{:,.2f}'.format(float(ganancias))
                    else:
                        ganancias = 0
                        ganancias_totales += 0
                except:
                    ganancias = 0
                    ganancias_totales += 0
                elemento_actual = {
                    'name': item_name,
                    'bin': enbin,
                    'end': termino,
                    'lore': lore,
                    'tier': tier,
                    'claimed': reclamado,
                    'precio': '{:,.2f}'.format(float(precio_actual)),
                    'ganacias': ganancias
                }
                elementos.append(elemento_actual)
                resultados += 1
        
        color = self.color_aleatorio()
        embed = discord.Embed(title = f'Auctions de {username} en {perfil_name.capitalize()}', colour = color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
        if resultados == 0:
            name = f'`Sin auctions activas`'
            value = f'Ganancias: 0'
            embed.add_field(name = name, value = value, inline = False)
            return msg.reply(embed = embed)


        for elemento in elementos:
            cantidad_baja = self.redondear_letras(elemento['precio'])

            if elemento["claimed"] != 'Vendido':
                if pasado:
                    name = f'\n~~{elemento["name"]}~~'
                else:
                    name = f'\n{elemento["name"]}'
                value = ''
                if extendido:
                    value += f'{elemento["lore"]}\n'
                    value += f'Tier: {elemento["tier"]}\n'
                    if pasado:
                        value += f'Termino hace: **{elemento["end"]}** {self.auction_emoji("auction_duration")}\n'
                    else:
                        value += f'Termina en: **{elemento["end"]}** {self.auction_emoji("auction_stats")}\n'
                    value += f'Tipo: {elemento["bin"]}\n'
                    value += f'Estado: ***{elemento["claimed"]}***\n'
                    value += f'`Precio Actual: {elemento["precio"]} ({cantidad_baja})\n`'
                else:
                    value += f'Precio Actual: **{elemento["precio"]} ({cantidad_baja})**\n'
                    if pasado:
                        value += f'Termino hace: **{elemento["end"]}** {self.auction_emoji("auction_duration")}\n'
                    else:
                        value += f'Termina en: **{elemento["end"]}** {self.auction_emoji("auction_duration")}\n'
                embed.add_field(name = name, value = value, inline = False)

        for elemento in elementos:
            if elemento["claimed"] == 'Vendido':

                name = f'\n__**{elemento["name"]}**__'
                value = ''
                #value += '```'
                if extendido:
                    value += f'```{elemento["lore"]}\n'
                    value += f'Tier: {elemento["tier"]}\n'
                    value += f'Precio Actual: {elemento["precio"]} ({cantidad_baja})\n'
                    if pasado:
                        value += f'Termino hace: **{elemento["end"]}** {self.auction_emoji("auction_duration")}\n'
                    else:
                        value += f'Terminaba en: {elemento["end"]} {self.auction_emoji("auction_duration")}\n'
                    value += f'Tipo: {elemento["bin"]}\n'
                    value += f'Estado: {elemento["claimed"]}\n'
                    value += f'Ganancia: {elemento["ganacias"]}\n```'
                else:
                    value += f'```Vendido: {elemento["ganacias"]} ({self.redondear_letras(elemento["ganacias"])})```'
                #value += '```'
                embed.add_field(name = name, value = value, inline = False)
        ganancias_totales = '{:,.2f}'.format(float(ganancias_totales))
        embed.add_field(name = 'Ganancia total:', value = f'{self.auction_emoji("claim_all_auctions")}`{ganancias_totales} ({self.redondear_letras(ganancias_totales)})`', inline = True)
        
        footer = f'Fecha de actualizacion en el server: {fecha_de_actualizacion}'
        #embed.set_footer(text = footer)
        
        return msg.reply(embed = embed)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'pah': self.ah_player,
            'playerah': self.ah_player,
        }