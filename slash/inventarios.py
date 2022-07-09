from datetime import datetime
from time import sleep
from mojang import MojangAPI
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from slash.generales import Generales, Item

class Inventario(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    @cog_ext.cog_slash(name="inventario", description="Muestra el inventario de un jugador", options = [
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
    async def inventario(self, msg: SlashContext, username: str = '', perfil: str = '', detallar :int = 0):
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
        data = Item.decode_inventory_data(inv)["i"]
        items = self.inv_filtro(data)

        # -------------- verificar detallado ----------------
        if detallar != 0:
            cantidad_items = len(items)
            if detallar > cantidad_items:
                await msg.edit(content = f'No se cuenta con esta cantidad de item en la lista. Verifica la lista completa')
                return

        # -------------- Creacion de embed ----------------
        numero_item = 1
        color = self.color_aleatorio()
        title = f'Inventario de {username}'
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        description = ''
        name = ''
        value = ''
        for item in items:
            if detallar == 0:
                description += f'{numero_item}.- {item["nombre"]}\n'
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

        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_thumbnail(url=url)
        drop_res = self.dropeo_hall(original_msg)
        if drop_res[0]:
            text = f'{drop_res[1]}'
            embed.set_footer(text=text)

        await msg.edit(content = '', embed = embed)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Inventario(bot))