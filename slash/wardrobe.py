from datetime import datetime
from time import sleep
from mojang import MojangAPI
import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from slash.generales import Generales, Item

class Wardrobe(commands.Cog, Generales):
    
    def re_acomodo(self, data):
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

    @cog_ext.cog_slash(name="wardrobe", description="Muestra el wardrobe de un jugador", options = [
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
    async def wardrobe(self, msg: SlashContext, username: str = '', perfil: str = '', detallar :int = 0):
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
        #open(f'./{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return

        # -------------- Verificcacion de la api de inventario ------------------
        try:
            inv = datos["wardrobe_contents"]["data"]
            actual = datos["inv_armor"]["data"]
        except:
            await msg.edit(content = f'Revise que la API de inventario este activa en {perfil_name}')
            return

        # -------------- Decodicicacion de datos ----------------
        username = self.for_tsuru(username)
        data = Item.decode_inventory_data(inv)["i"]
        #open(f'./info_pruebas/{username}_wardrobe.json', 'w').write(json.dumps(data, indent=4))
        part1, part2 = self.re_acomodo(data)
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
        totales = len(data) + len(usando)

        if detallar == 0:
            detallado = False
        else:
            detallado = True
        inventario = ''

        if detallado:
            if detallar > totales:
                await msg.edit(content = f'{username} no tiene {detallar} items en su wardrobe. Revisa la lista completa')
                return
            largo_usando = len(usando)
            largo_1 = len(items1)
            largo_2 = len(items2)
            if detallar <= largo_usando:
                item = usando[detallar - 1]
            else:
                detallar -= largo_usando
                if detallar <= largo_1:
                    item = items1[detallar - 1]
                else:
                    detallar -= largo_1
                    item = items2[detallar - 1]
        
            nombre = item['nombre']
            lore = item['lore']
            extra = item['extra']
            inventario += f'{nombre}\n'
            inventario += f'\n{lore}\n'
            inventario += f'{extra}\n'
            
            color = self.color_aleatorio()
            wd_emoji = self.general_emoji('wardrobe')
            title = f"{wd_emoji} {username}'s Wardrobe en {perfil_name}"
            description = inventario
            url = f'https://crafatar.com/renders/body/{uuid}?size=40'
            embed = discord.Embed(title=title, description=description, color=color)
            embed.set_thumbnail(url=url)
            await msg.edit(content = '', embed = embed)
            return
        
            for item in usando:
                nombre = item['nombre']
                inventario += f'{nombre} - usando\n'

        embeds_data = []
        embeds = []
        color = self.color_aleatorio()
        wd_emoji = self.general_emoji('wardrobe')
        title = f"{wd_emoji} {username}'s Wardrobe en {perfil_name}"
        description = ''
        url = f'https://crafatar.com/renders/body/{uuid}?size=40'

        # Pagina de Usando
        if len(usando) > 0:
            for item in usando:
                nombre = item['nombre']
                description += f'{nombre} - usando\n'
            embed = discord.Embed(title=title, description=description, color=color)
            embed.set_thumbnail(url=url)
            embeds.append(embed)
            for_embed = {}
            for_embed['title'] = title
            for_embed['description'] = description
            for_embed['tumb'] = url
            for_embed['color'] = color
            embeds_data.append(for_embed)
        
        # Pagina de Parte 1
        if len(items1) > 0:
            description = ''
            for item in items1:
                nombre = item['nombre']
                description += f'{nombre}\n'
            embed = discord.Embed(title=title, description=description, color=color)
            embed.set_thumbnail(url=url)
            embeds.append(embed)
            for_embed = {}
            for_embed['title'] = title
            for_embed['description'] = description
            for_embed['tumb'] = url
            for_embed['color'] = color
            embeds_data.append(for_embed)

        # Pagina de Parte 2
        if len(items2) > 0:
            description = ''
            for item in items2:
                nombre = item['nombre']
                description += f'{nombre}\n'
            embed = discord.Embed(title=title, description=description, color=color)
            embed.set_thumbnail(url=url)
            embeds.append(embed)
            for_embed = {}
            for_embed['title'] = title
            for_embed['description'] = description
            for_embed['tumb'] = url
            for_embed['color'] = color
            embeds_data.append(for_embed)
        paginas_totales = len(embeds_data)
        for i in range(paginas_totales):
            text = f'pagina {i+1} / {paginas_totales}'
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
        await msg.add_reaction('\U000025B6')

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Wardrobe(bot))