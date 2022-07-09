import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from slash.generales import Generales

class Info(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="hallInfo", description="Informacion del evento de hallowen")
    async def hall_info(self, msg: SlashContext):
        color = self.color_aleatorio()
        title = f':ghost: Evento de Hallowen :skeleton:'
        description = ''
        description += f'Durante el evento podras encontrar diferentes items que podran ser canjeados\n'
        description += f'\n :jack_o_lantern:Los items pueden salir en cualquier chat mientras se esta platicando con tranquilidad.\n'
        description += f'\n :jack_o_lantern:Tambien podran salir con mayor probabilidad en los slash commands del bot\n'
        description += f'\n :jack_o_lantern:Para canjear los items se puede contactar con <@!{self.event_ids[0]}> o <@!{self.event_ids[1]}>\n'
        description += f'\n :jack_o_lantern:El evento estara disponible durante el mes de Octubre con posibilidad de extenderse\n'
        description += ''
        embed = discord.Embed(title=title, description=description, color=color)

        name = ':skull_crossbones: **Revisa tu inventario** :skull_crossbones: '
        value = f'Puedes utilizar `/hallBag` en la seccion de comandos para revisar los items con los que cuentas y el valor total del mismo'
        embed.add_field(name=name, value=value, inline=False)

        name = f':alien: Valores y posibles encuentros'
        value = f'Para verificar el valor de cada item y los posibles items a encontrar puedes utilizar `/hallValues` en la seccion de comandos'
        embed.add_field(name=name, value=value, inline=False)

        name = f':moneybag: Canje de items'
        value = f'Para canjear los items puedes utilizar `/hallClaim` en la seccion de comandos'
        embed.add_field(name=name, value=value, inline=False)

        text = f'Recuerda estar atento de cada rincon y no dormir con la luz apagada que puedes encontrarte con horribles criaturas apartir de ahora (~°o°)~\n'
        text += f'Evento disponible hasta el 30 de Octubre'
        embed.set_footer(text=text)
        await msg.reply(embed = embed)

def setup(bot):
    bot.add_cog(Info(bot))