import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from discord.utils import get
from datetime import datetime
from os import replace, sys
from verificar import get_mochila
from time import sleep
from datetime import datetime, timedelta
from slash.generales import Generales

class Claim(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot

    def quitar_items(self, items_disponibles, cantidad_quitar):
        def transformar_cantidades(cantidad):
            if 'k' in cantidad:
                cantidad = cantidad.replace('k', '')
                cantidad = float(cantidad) * 1000
            elif 'm' in cantidad:
                cantidad = cantidad.replace('m', '')
                cantidad = float(cantidad) * 1000000
            else:
                cantidad = float(cantidad)
            return cantidad
        dropeos_hallowen = {
            'voidgloom': 1000000,
            'sven': 500000,
            'tarantula': 100000,
            'revenant': 50000,
            'esqueleto': 10000,
            'calabaza': 1000,
        }
        cantidad_quitar = transformar_cantidades(cantidad_quitar)
        acumulado = 0
        items_a_quitar = {}
        buscando = True
        while buscando:
            for item in dropeos_hallowen:

                if acumulado < cantidad_quitar:
                    cantidad_item_actual = 0
                    if item in items_disponibles:
                        cantidad_items_disponible = items_disponibles[item]
                    else:
                        cantidad_items_disponible = 0
                    agregando = True
                    while agregando and cantidad_items_disponible > 0:
                        print(cantidad_items_disponible)
                        if (acumulado + dropeos_hallowen[item] <= cantidad_quitar) and cantidad_items_disponible > 0:
                            cantidad_item_actual += 1
                            acumulado += dropeos_hallowen[item]
                        else:
                            agregando = False
                        cantidad_items_disponible -= 1
                    if cantidad_item_actual > 0:
                        items_a_quitar[item] = cantidad_item_actual
                else:
                    buscando = False
                    break
        print(items_a_quitar)
        return items_a_quitar
    
    @cog_ext.cog_slash(name="hallClaim", description="Reclama recompensas del evento (cooldown de 24 horas) cantidad minima 500k", options=[
        create_option(
            name = 'username',
            description = 'Usuario de Hypixel',
            option_type = 3,
            required=True
        ),
        create_option(
            name = 'item',
            description = 'coins/items',
            option_type = 3,
            required=True,
            choices = [
                {
                    'value': 'coins',
                    'name': 'coins'
                },
                {
                    'value': 'god potion',
                    'name': 'god potion'
                }
            ]
        ),
        create_option(
            name = 'cantidad',
            description = 'Cantidad a cambiar. Acepta abreviaciones (k / m)',
            option_type = 3,
            required=True
        )
    ])
    async def hall_claim(self, msg: SlashContext, username: str, item: str, cantidad: str):
        #if msg.author.id not in self.developers_ids:
        #    await msg.reply('Comando en mantenimiento')
        #    return
        if msg.guild.id == 831264016101802064:
            user_roles = msg.author.roles
            tiene = False
            for rol in user_roles:
                rol_id = rol.id
                if rol_id == 880473504519176272:
                    tiene = True
            
            # get from guil by rol id
            role_buscado = get(msg.guild.roles, id=880473504519176272)
            rol_name = role_buscado.name.replace('@', '')

            if not tiene:
                await msg.reply(f'Requieres de rol {rol_name} para poder reclamar los cambios')
                return

        try:
            username = self.get_username(username)
        except:
            pass
        
        cantidad = cantidad.replace(',','')
        cantidad = cantidad.replace(' ','')
        if item == 'coins':
            claim_coins = self.calculadora(f'{cantidad} + 0', numeros = True)
            if claim_coins < 500000:
                await msg.reply(f'Cantidad minima 500k')
                return
        elif item == 'god potion':
            cantidad_pedida = self.calculadora(f'{cantidad} + 0', numeros = True)
            if cantidad_pedida < 2:
                await msg.reply(f'Cantidad minima 2')
                return
        original_msg = msg
        msg = await msg.reply(f'Leyendo inventario... ')

        try:
            datos, perfil_name, uuid = self.obtener_perfil(username, '', uuid = True)
        except:
            datos = self.obtener_perfil(username, '', uuid = True)
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return
        
        # --------- Verificar que tenga al menos 24h de ultima peticion ----------
        user_id = original_msg.author.id
        query = f"SELECT  * FROM cambios WHERE user_id = '{user_id}'"
        peticiones = self.query_consulta(query)
        # ---- checando ahora ----
        ahora = self.fecha_plana()

        cooldown = False
        diferencia = 0
        if len(peticiones) > 0:
            for peticion in peticiones:
                fecha = peticion[5]
                diferencia = ahora - fecha
                if  diferencia < 86400:
                    cooldown = True
                    # convertir direfencia a horas minutos segundos
                    diferencia = timedelta(seconds = diferencia)
                    diferencia = str(diferencia).split('.')[0]
                    diferencia = diferencia.split(':')
                    diferencia = diferencia[0] + 'h ' + diferencia[1] + 'm ' + diferencia[2] + 's'
                    diferencia = diferencia.replace('-1 day, ', '')
                    print(diferencia)
                    break
        if original_msg.author.id in self.developers_ids and cooldown:
            cooldown = False
        if cooldown:
            await msg.edit(content = f'Comando en cooldown. Vuelve a intentar en {diferencia}')
            return
        mochila = get_mochila(user_id, user_id)
        coins = 0
        god_potion = 0
        description = ''
        items_disponibles = {}

        if len(mochila) == 0:
            coins = 0
            god_potion = 0
        else:
            for items in mochila:
                nombre = items[2]
                cantidad_item = items[3]
                item_value = self.dropeos_hallowen[nombre]["valor"]
                items_disponibles[nombre] = cantidad_item
                if self.dropeos_hallowen[nombre]['valor'] != None:
                    val = f'{item_value} * {cantidad_item}'
                    res = self.calculadora(val, numeros = True)
                    coins += res
                else:
                    if nombre == 'god_potion':
                        god_potion += cantidad_item

        if item == 'coins':
            claim_coins = self.calculadora(f'{cantidad} + 0', numeros = True)
            if coins < claim_coins:
                await msg.edit(content = f'No tienes suficientes coins para reclamar')
                return
            else:
                coins -= claim_coins
                description = f'Se han congelado {cantidad} de coins. Pronto se entregaran a {username}'
                quitar = self.quitar_items(items_disponibles, cantidad)
                for elemento in quitar:
                    nueva_cantidad = items_disponibles[elemento] - quitar[elemento]
                    query = f"UPDATE mochila SET cantidad={nueva_cantidad} where id='{user_id}_{elemento}'"
                    print(query)
                    self.query_ejecutar(query)
                query = f"INSERT INTO cambios (id, user_id, username, item, cantidad, date_peticion) VALUES ('{msg.id}', '{user_id}', '{username}',1 , '{claim_coins}', {ahora})"
                print(query)
                self.query_ejecutar(query)
        elif item == 'god potion':
            cantidad_pedida = self.calculadora(f'{cantidad} + 0', numeros = True)
            cantidad_pedida = int(cantidad_pedida)
            cantidad_disponible = 0
            if 'god_potion' in items_disponibles:
                cantidad_disponible = items_disponibles['god_potion']
            if cantidad_disponible < cantidad_pedida:
                await msg.edit(content = f'No tienes suficientes god potions para reclamar')
                return
            else:
                cantidad_disponible -= cantidad_pedida
                description = f'Se han congelado {cantidad_pedida} de god potions. Pronto se entregaran a {username}'
                nueva_cantidad = items_disponibles['god_potion'] - cantidad_pedida
                query = f"UPDATE mochila SET cantidad={nueva_cantidad} where id='{user_id}_god_potion'"
                print(query)
                self.query_ejecutar(query)
                query = f"INSERT INTO cambios (id, user_id, username, item, cantidad, date_peticion) VALUES ('{msg.id}', '{user_id}', '{username}',2 , '{cantidad_pedida}', {ahora})"
                print(query)
                self.query_ejecutar(query)
        color = self.color_aleatorio()
        title = f'Cambiando {cantidad} de {item}'
        embed = discord.Embed(title=title, description=description, color=color)
        text = f'id de peticion: {msg.id}'
        embed.set_footer(text=text)
        await msg.edit(content = '', embed = embed)
        # get channel data from id 899655472360083476
        channel = self.bot.get_channel(899655472360083476)
        # Channel pruebas 902340796169199686
        # channel = self.bot.get_channel(902340796169199686)
        title = f'Entregar a {username}'
        embed = discord.Embed(title=title, color=color)
        name = f'{item}'
        value = f'{cantidad}'
        embed.add_field(name=name, value=value, inline=False)
        name = f'Peticion id'
        value = f'{msg.id}'
        embed.add_field(name=name, value=value, inline=False)
        await channel.send(content = f'peticion id: {msg.id}',embed = embed)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Claim(bot))