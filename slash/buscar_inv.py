import json
from datetime import datetime
from time import sleep
from mojang import MojangAPI
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from slash.generales import Generales, Item
class Buscar(commands.Cog, Generales):
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

    @cog_ext.cog_slash(name="buscar", description="Busca en los items de un jugador", options = [
        create_option(
            name = 'busqueda',
            description = 'Filtro de busqueda',
            option_type = 3,
            required=True,
        ),
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
            name = 'excluir',
            description = 'Quitar resultados que coincidan',
            option_type = 3,
            required=False,
        ),
        create_option(
            name = 'detallar',
            description = 'Muestra informacion detallada de un item de la lista',
            option_type = 4,
            required=False,
        )
    ])
    async def buscar(self, msg: SlashContext, busqueda: str, username: str = '', perfil: str = '', excluir: str = '', detallar: int = 0):
        self.config()
        uuid = ''
        if username == '':
            id = msg.author.id
            uuid = self.get_verify_user(id)
            username = self.get_username(uuid = uuid)
        if username == '':
            await msg.reply(f'Debes verificar antes la cuenta para poder usar el comando sin especificar username. Utiliza /verificar')
            return
        filtro = busqueda.lower()
        quitar = excluir.lower()
        if detallar == 0:
            detalle = False
        else:
            detalle = True
        perfil_name = perfil
        original_msg = msg
        embeds_data = []
        msg = await msg.reply("***Cargando...***")
        try:
            if uuid != '':
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True, uuid_key=uuid)
            else:
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        # open(f'./{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return

        # -------------- Verificcacion de la api de inventario ------------------
        try:
            inv = datos["inv_contents"]["data"]
        except:
            await msg.edit(content = f'Revise que la API de inventario este activa en {perfil_name}')
            return

        # -------------- Decodicicacion de datos ----------------
        username = self.for_tsuru(username)
        
        # -------------- Verificando ultima actualizacion ----------------
        ahora = self.fecha_plana()
        save_clave = f'{username}_{perfil_name}'
        actualizar = True
        if save_clave in self.guardados:
            ultima_actualizacion = self.guardados[save_clave]['ultima_actualizacion']
        else:
            ultima_actualizacion = 0
        if abs(ahora - ultima_actualizacion) > 300:
            actualizar = True
        
        if not actualizar:
            inventario = self.guardados[save_clave]['inventario']
            ender_chest = self.guardados[save_clave]['ender_chest']
            wardrobe = self.guardados[save_clave]['wardrobe']
            backpacks = self.guardados[save_clave]['backpacks']
        else:
            inventario = self.get_inventario(datos)
            ender_chest = self.get_ender_chest(datos)
            wardrobe = self.get_wardrobe(datos)
            backpacks = self.get_backpack(datos)
            self.guardados[save_clave] = {
                'inventario': inventario,
                'ender_chest': ender_chest,
                'wardrobe': wardrobe,
                'backpacks': backpacks,
                'ultima_actualizacion': ahora
            }

        # -------------- Filtrando datos ----------------
        inventario = self.filtrar(inventario, filtro, quitar)
        ender_chest = self.filtrar(ender_chest, filtro, quitar)
        wardrobe = self.filtrar(wardrobe, filtro, quitar)
        backpacks = self.filtrar_mochila(backpacks, filtro, quitar)

        # -------------- Creando embeds ----------------
        embeds_data = []
        embeds = []
        color = self.color_aleatorio()
        title = f'Resultados en los items de {username} en {perfil_name}'
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        
        numero_de_item = 1
        item_elegido = ''
        det_original = detallar
        if detalle:
            cantidad_inventario = len(inventario)
            if detallar in range(1, cantidad_inventario + 1):
                for item in inventario:
                    if numero_de_item == detallar:
                        item_elegido = item
                        break
                    numero_de_item += 1
            else:
                detallar -= cantidad_inventario
                cantidad_ec = len(ender_chest)
                if detallar in range(1, cantidad_ec + 1):
                    for item in ender_chest:
                        if numero_de_item == detallar:
                            item_elegido = item
                            break
                        numero_de_item += 1
                else:
                    detallar -= cantidad_ec
                    cantidad_wa = len(wardrobe)
                    if detallar in range(1, cantidad_wa + 1):
                        for item in wardrobe:
                            if numero_de_item == detallar:
                                item_elegido = item
                                break
                            numero_de_item += 1
                    else:
                        detallar -= cantidad_wa
                        for n in backpacks:
                            bag = backpacks[n]
                            cantidad_ba = len(bag)
                            if detallar in range(1, cantidad_ba + 1):
                                for item in bag:
                                    if numero_de_item == detallar:
                                        item_elegido = item
                                        break
                                    numero_de_item += 1
                                break
                            else:
                                detallar -= cantidad_ba
                                numero_de_item += cantidad_ba
        
        if detalle:
            if item_elegido == '':
                await msg.edit(content = f'No se encontro el item {det_original} por favor revisa la lista completa')
                return
            item = item_elegido
            name = item['nombre']
            value = ''
            value += f'{item["lore"]}\n'
            value += f'{item["extra"]}\n'
            embed = discord.Embed(title=title, color=color)
            embed.set_thumbnail(url=url)
            embed.add_field(name=name, value=value, inline=False)
            await msg.edit(content = '', embed = embed)
            return


        # -------------- Inventario ----------------
        if len(inventario) > 0:
            name = f'En inventario: '
            value = ''
            for item in inventario:
                value += f'{numero_de_item}.- {item["nombre"]}\n'
                numero_de_item += 1

            for_embed = {}
            for_embed['title'] = title
            for_embed['color'] = color
            for_embed['tumb'] = url
            description = f'**{name}**\n'
            description += f'\n{value}'
            for_embed['description'] = description
            embed = discord.Embed(title=title, description = description, color=color)
            embed.set_thumbnail(url=url)
            embeds.append(embed)
            embeds_data.append(for_embed)
        
        # -------------- Ender Chest ----------------
        if len(ender_chest) > 0:
            pagina_actual = 1
            
            value = ''
            for item in ender_chest:
                if item['pagina_actual'] != pagina_actual and value != '':
                    for_embed = {}
                    for_embed['title'] = title
                    for_embed['color'] = color
                    for_embed['tumb'] = url
                    name = f'En ender chest en pagina {pagina_actual}: '
                    description = f'**{name}**\n'
                    description += f'\n{value}'
                    for_embed['description'] = description
                    embed = discord.Embed(title=title, description = description, color=color)
                    embed.set_thumbnail(url=url)
                    embeds.append(embed)
                    embeds_data.append(for_embed)
                    value = ''
                    pagina_actual = item['pagina_actual']
                value += f'{numero_de_item}.- {item["nombre"]}\n'
                numero_de_item += 1
            if value != '':
                for_embed = {}
                for_embed['title'] = title
                for_embed['color'] = color
                for_embed['tumb'] = url
                name = f'En ender chest en pagina {pagina_actual}: '
                description = f'**{name}**\n'
                description += f'\n{value}'
                for_embed['description'] = description
                embed = discord.Embed(title=title, description = description, color=color)
                embed.set_thumbnail(url=url)
                embeds.append(embed)
                embeds_data.append(for_embed)

        # -------------- Wardrobe ----------------
        if len(wardrobe) > 0:
            for_embed = {}
            for_embed['title'] = title
            for_embed['color'] = color
            for_embed['tumb'] = url
            for_embed['fields'] = []
            value = ''
            for item in wardrobe:
                value += f'{numero_de_item}.- {item["nombre"]}\n'
                numero_de_item += 1
            name = f'En wardrobe: '
            description = f'**{name}**\n'
            description += f'\n{value}'
            for_embed['description'] = description
            embed = discord.Embed(title=title, description = description, color=color)
            embed.set_thumbnail(url=url)
            embeds.append(embed)
            embeds_data.append(for_embed)

        # -------------- Backpacks ----------------
        if len(backpacks) > 0:
            for n in backpacks:
                mochila = backpacks[n]
                value = ''
                for item in mochila:
                    value += f'{numero_de_item}.- {item["nombre"]}\n'
                    numero_de_item += 1
                if value  != '':
                    for_embed = {}
                    
                    for_embed['title'] = title
                    for_embed['color'] = color
                    for_embed['tumb'] = url
                    #for_embed['fields'] = []
                    description = ''
                    description += f'**En Backpack {n}: **\n'
                    description += f'\n{value}'
                    #for_embed['fields'].append([name, value, False])
                    for_embed['description'] = description
                    embed = discord.Embed(title=title, description = description, color=color)
                    embed.set_thumbnail(url=url)
                    embeds.append(embed)
                    embeds_data.append(for_embed)
        
        paginas_totales = len(embeds)
        for i in range(paginas_totales):
            text = f'Pagina {i+1}/{paginas_totales}'
            embeds[i].set_footer(text=text)
            embeds_data[i]['footer'] = text
        
        if paginas_totales == 0:
            await msg.edit(content = f'No se encontraron resultados para {username} en {perfil_name}')
            return
        
        await msg.edit(content = '', embed = embeds[0])
        user_id = original_msg.author.id
        id_mensaje = msg.id
        guardar = {
            'msg_id': id_mensaje,
            'user_id': user_id,
            'embeds': embeds_data,
        }
        open(f'./embeds_data/emb_data.json', 'w').write(json.dumps(guardar, indent=4))
        await msg.channel.send(f'+load {id_mensaje}')
        if paginas_totales > 1:
            await msg.add_reaction('\U000025B6')



    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Buscar(bot))
