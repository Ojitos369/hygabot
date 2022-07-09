import json
import discord
from datetime import datetime
from slash.generales import Generales
class Pruebas(Generales):

    def pruebas(self, msg = '', text = ''):
        if msg.author.id not in self.developers_ids:
            return
        
        
        
        self.config()
        partes = text.split(' ')
        if partes[0] != '':
            base = partes[0]
        else:
            base = 'https://api.hypixel.net/resources/skyblock/items'
            #base = 'https://api.hypixel.net/resources/skyblock/skills'
            #base = 'https://api.hypixel.net/resources/skyblock/collections'
        base += '?key='
        if len(partes) > 1:
            partes.pop(0)
            segundo = ' '.join(partes)
        else:
            segundo = ''
        data = self.consulta(base, segundo)
        # save data as pruebas.json
        open('./info_pruebas/pruebas.json', 'w').write(json.dumps(data, indent=4))
        #print(data)

        return msg.channel.send('Guardado data')

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'p': self.pruebas
        }