import json
import discord
from datetime import datetime
from funciones.generales import Generales
class Escencias(Generales):

    def escencias(self, msg = '', text = ''):
        self.config()
        # -------------- Separacion de datos buscando opciones y usuario ----------------
        separado = text.split(' ')
        username = separado[0]
        try:
            perfil_name = separado[1]
        except:
            perfil_name = ''

        # -------------- Obtencion de datos ----------------
        try:
            datos, perfil_name, uuid = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        # open(f'./{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            return msg.reply('Verifica que el Usuario este bien escrito')
        if datos == 'perfil':
            return msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')
    
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
        
        return msg.reply(embed = embed)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'es': self.escencias,
            'escencia': self.escencias,
            'escencias': self.escencias,
        }