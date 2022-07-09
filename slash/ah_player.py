import json
import pandas as pd
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from mojang import MojangAPI
from slash.generales import Generales, Item

class Ah_player(commands.Cog, Generales):
    @cog_ext.cog_slash(name="auctionPlayer", description="Muestra las auctions de un jugador", options = [
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
        ),
        create_option(
            name = 'detalles',
            description = 'Muestra informacion detallada de los items (si)',
            option_type = 3,
            required=False,
        )
    ])
    async def ah_player(self, msg: SlashContext, username: str = '', perfil: str = '', detalles :str = 'False'):
        self.config()
        uuid = ''
        if username == '':
            id = msg.author.id
            uuid = self.get_verify_user(id)
            username = self.get_username(uuid = uuid)
        if username == '':
            await msg.reply(f'Debes verificar antes la cuenta para poder usar el comando sin especificar username. Utiliza /verificar')
            return
        msg_original = msg
        msg = await msg.reply(f'Cargando...')
        perfil_name = perfil
        link_base = 'https://api.hypixel.net/skyblock/auction'
        perfil_id = self.obtener_perfil(username, perfil_name, id = True)
        primero = f'{link_base}?key='
        segundo = f'&profile={perfil_id}'
        if detalles != 'False':
            extendido = True
        else:
            extendido = False
        try:
            if uuid != '':
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True, uuid_key=uuid)
            else:
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return
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

            #print(f'{elemento["item_name"]}:\n{termino}\n\n')
            if aux < -3:
                mostrar = False
            pasado = False
            if '-' in termino:
                termino = self.obtener_tiempo_relativo_inverso(elemento['end'])
                pasado = True

            if elemento['claimed'] == True:
                mostrar = False

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
            await msg.edit(content = '', embed = embed)
            return

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
        
        drop_res = self.dropeo_hall(msg_original)
        if drop_res[0]:
            text = drop_res[1]
            embed.set_footer(text = text)
        
        await msg.edit(content = '', embed = embed)
        return

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Ah_player(bot))