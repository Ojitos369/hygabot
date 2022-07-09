import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from slash.generales import Generales

class Help(commands.Cog, Generales):

    @cog_ext.cog_slash(name="help", description="Muestra las novedades del bot")
    async def help(self, msg: SlashContext):
        color = self.color_aleatorio()
        title = f'Lista de comandos'
        description = '```Escribe "/" y selecciona el comando para informacion mas detallada y argumentos posibles```'
        embed = discord.Embed(title=title, description=description, color = color)
        dropeos_hall = self.dropeo_hall(msg)
        if dropeos_hall[0]:
            text = dropeos_hall[1]
            embed.set_footer(text = text)

        emoji = self.general_emoji('cash')
        name = f'{emoji} Economia'
        value = ''
        value += '\n`auctionHouse`: *Muestra items de la auction house*\n'
        value += '\n`auctionPlayer`: *Muestra auctions de un jugador*\n'
        value += '\n`bazar`: *Muestra informacion de los item en el bazar*\n'
        value += ''
        embed.add_field(name=name, value=value, inline=False)

        emoji = self.general_emoji('skyblock')
        emoji2 = self.general_emoji('perfil')
        name = f'{emoji} Perfiles {emoji2}'
        value = ''
        value += '\n`escencias`: *Cantidad de escencias de cada tipo*\n'
        value += '\n`forja`: *Muestra los items en la forja*\n'
        value += '\n`hotm`: *Informacion sobre hotm*\n'
        value += '\n`slayer`: *Informacion sobre slayers*\n'
        value += '\n`talismanes`: *Muestra los talismanes*\n'
        value += '\n`pets`: *Muestra los pets*\n'
        value += '\n`inventario`: *Muestra el inventario un jugador*\n'
        value += '\n`enderChest`: *Muestra el ender chest de un jugador*\n'
        value += '\n`wardrobe`: *Muestra las armaduras de un jugador*\n'
        value += '\n`backpack`: *Muestra las backpacks de un jugador*\n'
        value += '\n`buscar`: *Busca entre los items de un jugador*\n'
        value += '\n`kills`: *Kills acumuladas*\n'
        value += '\n`skills`: *Datos de las skills de un jugador*\n'
        value += ''
        embed.add_field(name=name, value=value, inline=False)

        name = 'Extras'
        value = ''
        value += '\n`help`: *es este comando*\n'
        value += '\n`limpiar (admin)`\n'
        value += '\n`news`: *Novedades del bot*\n'
        value += '\n`invitar`: *Link para invitar el bot :3*\n'
        value += '\n`operacion`: *Realiza calculos*\n'
        value += '\n`Verificar`: *Te verifica con tu usuario de minecraft*\n'
        value += '\n`item`: *Muestra informacion de items que coincidan*\n'
        value += '\n`reforje`: *Muestra la informacion de los reforges que coincidan*\n'
        value += '\n`sugerencia`: *Ayudanos a mejorar el bot enviando tus ideas*\n'
        value += '\n`bug`: *Ayudanos a mejorar el bot reportandos sus fallos*\n'
        value += ''
        embed.add_field(name=name, value=value, inline=False)

        await msg.reply(embed = embed)

def setup(bot):
    bot.add_cog(Help(bot))