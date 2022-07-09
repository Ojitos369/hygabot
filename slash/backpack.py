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
class Backpack(commands.Cog, Generales):
    @cog_ext.cog_slash(name="backpack", description="Muestra las backpacks de un jugador", options = [
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

    async def backpack(self, msg: SlashContext, username: str = '', perfil: str = '', detallar :int = 0):
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
        # open(f'./{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return

        username = self.for_tsuru(username)

        # -------------- Verificcacion de la api de inventario ------------------
        try:
            data = datos["backpack_contents"]
        except:
            await msg.edit(content = f'Revise que la API de inventario este activa en {perfil_name}')
            return

        # -------------- Decodicicacion de datos ----------------
        detallado = False
        regreso_detallado = False
        if detallar != 0:
            detallado = True
        mochilas = 0
        item_actual = 0
        mochila_actual = 0        

        embeds_data = []
        embeds = []
        color = self.color_aleatorio()
        title = f'Backpack de {username} en {perfil_name}'
        url=f'https://crafatar.com/renders/body/{uuid}?size=40'
        
        for i in range(25):
            try:
                inv = data[str(i)]["data"]
                mochila = Item.decode_inventory_data(inv)["i"]
                mochila = self.inv_filtro(mochila)
            except:
                mochila = ()
            if len(mochila) != 0:
                #mochila_actual += 1
                mochila_actual = str(i + 1)
                if detallado:
                    for item in mochila:
                        item_actual += 1
                        if item_actual == detallar:
                            description = f'{item_actual}.- {item["nombre"]} en **Backpack {i+1}**\n'
                            description += f'{item["lore"]}\n'
                            description += f'{item["extra"]}\n'
                            
                            embed = discord.Embed(title=title, description=description, color=color)
                            embed.set_thumbnail(url=url)
                            await msg.edit(content = f'', embed=embed)
                            regreso_detallado = True
                            return
                else:
                    for_embed = {}
                    for_embed['color'] = color
                    for_embed['title'] = title
                    for_embed['tumb'] = url
                    description = f'**Backpack {mochila_actual}**\n'
                    for item in mochila:
                        item_actual += 1
                        description += f'{item_actual}.- {item["nombre"]}\n'
                    for_embed['description'] = description
                    embed = discord.Embed(title=title, description=description, color=color)
                    embed.set_thumbnail(url=url)
                    embeds.append(embed)
                    embeds_data.append(for_embed)

        if detallado and not regreso_detallado:
            await msg.edit(content = f'Numero de item no se encuentra en las backpacks. Revisa la lista entera')
            return

        paginas_totales = len(embeds_data)
        for i in range(paginas_totales):
            text = f'Pagina {i+1} / {paginas_totales}'
            embeds[i].set_footer(text=text)
            embeds_data[i]['footer'] = text
        
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
    bot.add_cog(Backpack(bot))