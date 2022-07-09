import json
from do_embeds import do_embed
import pandas as pd
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord import *
from dislash.interactions import *
from discord_components import *
from discord.utils import get
from datetime import datetime
from time import sleep
from slash.generales import Generales, Item

#class Prueba(Generales):
class Prueba(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot

    guardados = {}

    def get_inventario(self, datos):
        inv = datos["inv_contents"]["data"]
        data = Item.decode_inventory_data(inv)["i"]
        items = self.inv_filtro(data)
        return items

    def get_ender_chest(self, datos):
        inv = datos["ender_chest_contents"]["data"]
        data = Item.decode_inventory_data(inv)["i"]
        items = self.inv_filtro(data)
        return items

    def get_wardrobe(self, datos):
        def re_acomodo(data):
            new_data = []
            # Separando en 2 listas
            parte_1 = data[:len(data)//2]
            parte_2 = data[len(data)//2:]
            slots = int(len(parte_1) / 4)
            for i in range(slots):
                new_data.append(parte_1[i])
                new_data.append(parte_1[i + (slots)])
                new_data.append(parte_1[i + 2 * (slots)])
                new_data.append(parte_1[i + 3 * (slots)])
            
            new_data2 = []
            slots = int(len(parte_2) / 4)
            for i in range(slots):
                new_data2.append(parte_2[i])
                new_data2.append(parte_2[i + (slots)])
                new_data2.append(parte_2[i + 2 * (slots)])
                new_data2.append(parte_2[i + 3 * (slots)])
            return new_data, new_data2

        inv = datos["wardrobe_contents"]["data"]
        actual = datos["inv_armor"]["data"]
        data = Item.decode_inventory_data(inv)["i"]

        part1, part2 = re_acomodo(data)
        usando = Item.decode_inventory_data(actual)["i"]
        try:
            usando = self.inv_filtro(usando)
        except:
            usando = []
        try:
            items1 = self.inv_filtro(part1)
        except:
            items1 = []
        try:
            items2 = self.inv_filtro(part2)
        except:
            items2 = []
        usando.reverse()
        for item in usando:
            item['nombre'] += ' - usando'
        totales = usando + items1 + items2
        return totales

    def get_backpack(self, datos):
        data = datos["backpack_contents"]
        backpacks = []
        for i in range(25):
            try:
                inv = data[str(i)]["data"]
                mochila = Item.decode_inventory_data(inv)["i"]
                mochila = self.inv_filtro(mochila)
            except:
                mochila = ()
            
            if len(mochila) > 0:
                backpacks.append(mochila)
        return backpacks

    def filtrar(self, datos, filtro, quitar):
        resultantes = []
        for item in datos:
            encontrado = True
            nombre = item['nombre'].lower()
            filtros = filtro.lower().split(' ')
            for filt in filtros:
                if filt not in nombre:
                    encontrado = False
                    break
            if encontrado and quitar != '':
                quitar = quitar.lower().split(' ')
                for qui in quitar:
                    if qui in nombre:
                        encontrado = False
                        break
            if encontrado:
                resultantes.append(item)

        return resultantes

    def filtrar_mochila(self, datos, filtro, quitar):
        resultantes = {}
        i = 1
        for mochila in datos:
            filtro_mochila = self.filtrar(mochila, filtro, quitar)
            if len(filtro_mochila) > 0:
                resultantes[i] = filtro_mochila
            i += 1
        return resultantes

    async def buscar_in_player(self, msg, uuid, extra_print, filtro, perfil_name = '', quitar = '',):
        datos, perfil_name, uuid, username = self.obtener_perfil('', perfil_name, uuid = True, uuid_key=uuid)
        await msg.edit(content = f'{extra_print}.- Buscando en `{username}`...')
        # -------------- Verificcacion de la api de inventario ------------------
        try:
            inv = datos["inv_contents"]["data"]
        except:
            return False, f'Api de inventario desactivada de {username} en {perfil_name}'

        # -------------- Decodicicacion de datos ----------------
        username = self.for_tsuru(username)
        
        inventario = self.get_inventario(datos)
        ender_chest = self.get_ender_chest(datos)
        wardrobe = self.get_wardrobe(datos)
        backpacks = self.get_backpack(datos)

        # -------------- Filtrando datos ----------------
        inventario = self.filtrar(inventario, filtro, quitar)
        ender_chest = self.filtrar(ender_chest, filtro, quitar)
        wardrobe = self.filtrar(wardrobe, filtro, quitar)
        backpacks = self.filtrar_mochila(backpacks, filtro, quitar)

        # -------------- Creando embeds ----------------
        title = f'Resultados en los items de {username} en {perfil_name}'
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        
        items_totales = 0

        encontrados = {}
        # -------------- Inventario ----------------
        if len(inventario) > 0:
            encontrados['inventario'] = len(inventario)
            items_totales += len(inventario)
        
        # -------------- Ender Chest ----------------
        if len(ender_chest) > 0:
            encontrados['ender_chest'] = len(ender_chest)
            items_totales += len(ender_chest)

        # -------------- Wardrobe ----------------
        if len(wardrobe) > 0:
            encontrados['wardrobe'] = len(wardrobe)
            items_totales += len(wardrobe)

        # -------------- Backpacks ----------------
        if len(backpacks) > 0:
            encontrados['backpacks'] = len(backpacks)
            items_totales += len(backpacks)
        
        if len(encontrados) > 0:
            await msg.edit(content = f'Encontrados {items_totales} en `{username}`')
            encontrados['title'] = title
            encontrados['url'] = url
            return True, encontrados
        else:
            return False, 'Sin resultados para {username} en {perfil_name}'

    @cog_ext.cog_slash(name="buscarguild", description="Hace una busqueda entre los items de todos los miembros de una guild", options=[
        create_option(
            name = 'guild',
            description = 'Nombre de la guild',
            option_type = 3,
            required=True,
        ),
        create_option(
            name = 'filtro',
            description = 'Busqueda a realizar',
            option_type = 3,
            required=True,
        ),
        create_option(
            name = 'quitar',
            description = 'coincidencias a ignorar',
            option_type = 3,
            required=False,
        )
    ])
    async def pruebas(self, msg: SlashContext, guild: str, filtro: str, quitar: str = ''):
        if msg.author.id not in self.developers_ids:
            await msg.reply("Comando disponible solo para beta-tester y desarrollador")
            return
        link_base = 'https://api.hypixel.net/guild'
        inicio = f'{link_base}?key='
        fin = f'&name={guild}'
        hydata = self.consulta(inicio, fin)
        original_msg = msg
        msg = await msg.reply('Buscando...')
        try:
            data = hydata['guild']['members']
        except:
            await msg.edit(content='No se encontro la guild. Verifique que este bien escrita.')
            return
        
        embeds_data = []
        miembros_totales = len(data)
        i = 0
        for miembro in data:
            i += 1
            extra_print = f'{i}/{miembros_totales}'
            uuid = miembro["uuid"]
            try:
                paso, datos = await self.buscar_in_player(msg, uuid, extra_print, filtro, quitar = quitar)
            except:
                paso, datos = False, 'Error'
            if paso:
                for_embed = {}
                for_embed['title'] = datos['title']
                del datos['title']
                for_embed['tumb'] = datos['url']
                del datos['url']
                for_embed['fields'] = []
                for storage, cantidad in datos.items():
                    name = f'En {storage.replace("_"," ").title()}:'
                    value = f'{cantidad} coincidencias'
                    for_embed['fields'].append([name, value, False])
                embeds_data.append(for_embed)
        
        paginas_totales = len(embeds_data)
        if paginas_totales > 1:
            for i in range(paginas_totales):
                text = f'Pagina {i+1} de {paginas_totales}'
                embeds_data[i]['footer'] = text
            embeds = do_embed(embeds_data)
            await msg.edit(content='', embed=embeds[0])
            self.original_msg = original_msg
            user_id = self.original_msg.author.id
            id_mensaje = msg.id
            guardar = {
                'msg_id': id_mensaje,
                'user_id': user_id,
                'embeds': embeds_data,
            }
            await self.guardado_de_embeds(guardar, id_mensaje, msg, paginas_totales)
        else:
            await msg.edit(content=f'Sin resultados para {filtro} en {guild}')
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]
def setup(bot):
    bot.add_cog(Prueba(bot))