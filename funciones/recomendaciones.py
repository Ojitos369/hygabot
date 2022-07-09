import json
import discord
from datetime import datetime
from funciones.generales import Generales
class Recomendaciones(Generales):

    def recomendaciones(self, msg = '', text = '', client = ''):
        anonimo = False
        contactar = False
        separado = text.split(' ')
        # ------------ Comprobar anonimo ------------ #
        for i in range(len(separado)):
            if separado[i] == '-an':
                anonimo = True
                separado.pop(i)
                break
        # ------------ Comprobar contactar ------------ #
        for i in range(len(separado)):
            if separado[i] == '-r':
                contactar = True
                separado.pop(i)
                break

        text = ' '.join(separado)
        user = client
        #ojitos_id = '673397248427556887'
        autor = msg.author
        autor_id = autor.id
        color = self.color_aleatorio()
        if anonimo:
            title = f'Recomendacion Anonima'
        else:
            title = f'Recomendacion de {autor}'

        if contactar:
            title += ' SE ESPERA CONTACTO'

        embed = discord.Embed(title = title, description = text, color = color)
        mensajes = []
        mensajes.append(user.send(embed = embed))
        mensajes.append(msg.author.send(f'Comentario enviado <@{autor_id}>. Gracias por tu aporte'))
        mensaje = {
            'borrar': True,
            'respuesta': mensajes,
            'not_embed': True
        }
        return  mensaje

    def config(self, datos = False, n = 0):
        self.funciones = {
            'recomendaciones': self.recomendaciones,
            'recomendacion': self.recomendaciones,
            'sugerencia': self.recomendaciones,
            'sugerencias': self.recomendaciones,
            'sugerir': self.recomendaciones,
            'sug': self.recomendaciones,
            'rec': self.recomendaciones
        }