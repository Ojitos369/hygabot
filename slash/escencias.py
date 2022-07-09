import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from slash.generales import Generales
class Escencias(commands.Cog, Generales):

    @cog_ext.cog_slash(name="escencias", description="Muestra las escencias de un jugador", options = [
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
    async def escencias(self, msg: SlashContext, username: str = '', perfil: str = ''):
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
        msg = await msg.reply("**Cargando...**")
        # -------------- Obtencion de datos ----------------
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

        # -------------- Decodicicacion de datos ----------------
        
        escencias = ["essence_undead",
        "essence_wither",
        "essence_dragon",
        "essence_diamond",
        "essence_gold",
        "essence_ice",
        "essence_spider"]
        color = self.color_aleatorio()
        embed = discord.Embed(title=f'Escencias de {username} en {perfil_name}', color=color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')

        for escencia in escencias:
            try:
                cantidad = datos[escencia]
            except:
                cantidad = 0
            nombre = escencia.replace('_', ' ')
            nombre = self.get_emoji_name(nombre)
            name = f"{nombre.replace('essence ', '')}"
            value = f'`Cantidad: {cantidad:,.0f}`'
            embed.add_field(name=name, value=value, inline=False)
        drop_res = self.dropeo_hall(original_msg)
        if drop_res[0]:
            text = drop_res[1]
            embed.set_footer(text = text)        
        await msg.edit(content = '', embed = embed)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Escencias(bot))