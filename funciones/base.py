import json
import discord
from datetime import datetime
from slash.generales import Generales
class Name(Generales):

    def name(self, msg = '', text = ''):
        self.config()
        return msg.channel.send('Hola desde name')

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'name': self.name
        }