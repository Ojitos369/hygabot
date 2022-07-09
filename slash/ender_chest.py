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
class Ender(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    @cog_ext.cog_slash(name="enderChest", description="Muestra el ender chest de un jugador", options = [
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
            name = 'detallar',
            description = 'Muestra informacion detallada de un item de la lista',
            option_type = 4,
            required=False,
        )
    ])
    async def ender(self, msg: SlashContext, username: str = '', perfil: str = '', detallar :int = 0):
        self.config()
        uuid = ''
        if username == '':
            id = msg.author.id
            uuid = self.get_verify_user(id)
            username = self.get_username(uuid = uuid)
        if username == '':
            await msg.reply(f'Debes verificar antes la cuenta para poder usar el comando sin especificar username. Utiliza /verificar')
            return
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
        #open(f'./info_pruebas/{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return

        # -------------- Verificcacion de la api de inventario ------------------
        try:
            inv = datos["ender_chest_contents"]["data"]
        except:
            await msg.edit(content = f'Revise que la API de inventario este activa en {perfil_name}')
            return

        # -------------- Decodicicacion de datos ----------------
        username = self.for_tsuru(username)
        data = Item.decode_inventory_data(inv)["i"]
        items = self.inv_filtro(data)

        if detallar != 0:
            cantidad_items = len(items)
            if detallar > cantidad_items:
                await msg.edit(content = f'No se cuenta con esta cantidad de item en la lista. Verifica la lista completa')
                return

        # -------------- Creacion de embed ----------------
        numero_item = 1
        elementos_per_page = 45
        color = self.color_aleatorio()
        ec_emoji = self.general_emoji('ender_chest')
        title = f'{ec_emoji} Ender Chest de {username} en {perfil_name}'
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        description = ''
        name = ''
        value = ''
        pagina = 1
        for_embed = {}
        for_embed['title'] = title
        for_embed['tumb'] = url
        for_embed['color'] = color
        respuestas = []

        for item in items:
            if detallar == 0:
                description += f'{numero_item}.- {item["nombre"]}\n'
                if item['cantidad_original'] % elementos_per_page == 0:
                    for_embed['description'] = description
                    embed = discord.Embed(title=title, description=description, color=color)
                    embed.set_thumbnail(url=url)
                    respuestas.append(embed)
                    embeds_data.append(for_embed)
                    for_embed = {}
                    for_embed['title'] = title
                    for_embed['tumb'] = url
                    for_embed['color'] = color
                    description = ''
            elif detallar == numero_item:
                name = item["nombre"]
                value += f'{item["lore"]}\n'
                value += f'{item["extra"]}\n'
                embed = discord.Embed(title=title, color=color)
                embed.add_field(name = name, value = value, inline = False)
                embed.set_thumbnail(url=url)
                await msg.edit(content = '', embed = embed)
                return
            numero_item += 1

        if description != '':
            for_embed['description'] = description
            embed = discord.Embed(title=title, description=description, color=color)
            embed.set_thumbnail(url=url)
            respuestas.append(embed)
            embeds_data.append(for_embed)
            for_embed = {}
            for_embed['title'] = title
            for_embed['tumb'] = url
            for_embed['color'] = color
        drop_res = self.dropeo_hall(original_msg)
        text_drop = ''
        if drop_res[0]:
            text_drop = f'{drop_res[1]}'
        
        paginas_totales = len(embeds_data)
        for i in range(paginas_totales):
            text = f'Pagina {i+1} de {paginas_totales}\n'
            text += f'{text_drop}'
            respuestas[i].set_footer(text = text)
            embeds_data[i]['footer'] = text
        await msg.edit(content = '', embed = respuestas[0])
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
    bot.add_cog(Ender(bot))