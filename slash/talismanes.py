import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from slash.generales import Generales, Item
class Talismanes(commands.Cog, Generales):

    @cog_ext.cog_slash(name="talismanes", description="Muestra los talismanes", options = [
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
        )
    ])
    async def talismanes(self, msg: SlashContext, username: str = '', perfil: str = ''):
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
        talis_por_pagina = 10
        
        msg = await msg.reply("**Cargando...**")
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
        username = self.for_tsuru(username)

        # -------------- Verificcacion de la api de inventario ------------------
        try:
            talismanes_data = datos["talisman_bag"]["data"]
        except:
            await msg.edit(content = f'Revise que la API de inventario este activa')
            return

        # -------------- Decodicicacion de datos ------------------
        data = Item.decode_inventory_data(talismanes_data)["i"]
        color = self.color_aleatorio()
        value = ''
        numero_de_talismanes = 0
        mensajes = []
        talis_data = []
        recomb_emoji = self.recomb_item()        
        for talisman in data:
            try:
                lore_data = talisman['tag']['display']['Lore']
                lore = lore_data.pop()
                lore = self.remplazar(lore)
                name = self.remplazar(talisman['tag']['display']['Name'])
                name = self.get_emoji_name(name)
                try:
                    recombulado = talisman['tag']['ExtraAttributes']['rarity_upgrades']
                    name = f'{numero_de_talismanes + 1}.- {name}{recomb_emoji}\n'
                except:
                    name = f'{numero_de_talismanes + 1}.- {name}\n'
                numero_de_talismanes += 1
                talis_data.append([name, lore])
            except:
                break
        ac_emoji = self.general_emoji('accesorios')
        title = f'{ac_emoji} Talismanes de {username} en {perfil_name}'
        description = f'Cuenta con {numero_de_talismanes} talismanes'
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'
        talis_en_pagina = 0
        paginas_totales = (numero_de_talismanes // talis_por_pagina) + 1
        pagina = 1
        drop_event = self.dropeo_hall(original_msg)
        embed = discord.Embed(title=title,description=description, color=color)
        embed.set_thumbnail(url=url)
        text = f'Pagina {pagina} de {paginas_totales}'
        if drop_event[0]: text += f'{drop_event[1]}'
        embed.set_footer(text=text)

        for_embed = {}
        for_embed['title'] = title
        for_embed['description'] = description
        for_embed['tumb'] = url
        for_embed['color'] = color
        for_embed['footer'] = text
        for_embed['fields'] = []
        for i in range(len(talis_data)):
            name = talis_data[i][0]
            value = f'`{talis_data[i][1]}`'
            embed.add_field(name=name, value=value, inline=False)
            for_embed['fields'].append([name, value, False])
            talis_en_pagina += 1
            if talis_en_pagina == talis_por_pagina:
                mensajes.append(embed)
                embeds_data.append(for_embed)
                talis_en_pagina = 0
                pagina += 1
                embed = discord.Embed(title=f'Talismanes de {username}',description=description, color=color)
                embed.set_thumbnail(url=url)
                text =f'Pagina {pagina} de {paginas_totales}'
                if drop_event[0]: text += f'{drop_event[1]}'
                embed.set_footer(text=text)

                for_embed = {}
                for_embed['title'] = title
                for_embed['description'] = description
                for_embed['tumb'] = url
                for_embed['color'] = color
                for_embed['footer'] = text
                for_embed['fields'] = []
        if talis_en_pagina != 0:
            mensajes.append(embed)
            embeds_data.append(for_embed)
        
        await msg.edit(content = '', embed = mensajes[0])
        user_id = original_msg.author.id
        id_mensaje = msg.id
        guardar = {
            'msg_id': id_mensaje,
            'user_id': user_id,
            'embeds': embeds_data,
        }
        open(f'./embeds_data/emb_data.json', 'w').write(json.dumps(guardar, indent=4))
        await msg.channel.send(f'+load {id_mensaje}')
        await msg.add_reaction('\U000025B6')

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Talismanes(bot))
