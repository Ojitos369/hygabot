import json
import discord
from datetime import datetime
from funciones.generales import Generales
class Novedades(Generales):
    def novedades(self, msg = '', text = ''):
        color = self.color_aleatorio()
        title = f'Novedades del bot'
        description = f'Puedes consultar las novedades con ***`/news`***'
        embed = discord.Embed(title = title, description = description, color = color)

        text = f'Recuerda que puedes enviar sugerencias con "{self.prefijo}sug tu_sugerencia"\n'
        text += f'Todas son leidas y tomadas en cuenta'
        embed.set_footer(text = text)
        return msg.channel.send(embed = embed)
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'novedades': self.novedades,
            'news': self.novedades,
            'new': self.novedades,
        }