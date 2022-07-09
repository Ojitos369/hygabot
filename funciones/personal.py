import json
import discord
from datetime import datetime
from slash.generales import Generales
class Personal(Generales):
    def personal(self, msg = '', text = ''):
        if msg.author.id not in self.developers_ids:
            return
        return
    
    def short_emojis(self, msg = '', text = ''):
        with open('./json/emojis.json') as datos:
            emojis = json.load(datos)
        
        new = {}
        for item, emoji in emojis.items():
            palabras = item.replace('_', ' ')
            for palabra in palabras.split():
                if palabra[0] in new:
                    new[palabra[0]][item] = emoji
                else:
                    new[palabra[0]] = {item: emoji}
        
        with open('./json/emojis.json', 'w') as datos:
            json.dump(new, datos, indent=4)
        return msg.reply(f'Acomodado emoji')


    def short_items(self, msg = '', text = ''):
        if msg.author.id not in self.developers_ids:
            return
        
        def replaces(text):
            replaces = {
                '§': '',
                ' ': '_',
                'á': 'a',
                'é': 'e',
                'í': 'i',
                'ó': 'o',
                'ú': 'u',
                'aatrox_batphone': 'maddox_batphone',
                'hydra1': 'water_hydra',
                'aatrox_phone_number': "maddox's_phone_number",
                'spiders_den_top_travel_scroll': "travel_scroll_to_spider's_den_top_of_nest",
                'ghost_boots': 'ghostly_boots',
                'nether_brick_item': 'nether_brick',
            }
            for replace in replaces:
                text = text.replace(replace, replaces[replace])
            return text
        
        with open('./info_pruebas/pruebas.json') as datos:
            items_data = json.load(datos)
        items = items_data['items']
        items_dic = {}
        names = []
        count = 0
        for item in items:
            id = item['id']
            id = replaces(id.lower())
            name = item['name']
            name = replaces(name.lower())
            if id != name:
                count += 1
                print('-'*20)
                print(f'Count: {count}\n')
                print(f'id: {id}\nname: {name}')
                print('-'*20)
            items_dic[id] = item
            names.append(id)
        
        items_order = {}
        letters_numers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for letter in letters_numers:
            items_order[letter] = {}
        names.sort()
        for name in names:
            letra = name[0].lower()
            items_order[letra][name] = items_dic[name]
        
        with open('./info_pruebas/pruebas.json', 'w') as datos:
            json.dump({'items': items_order}, datos, indent=4)
        return msg.reply('en personal')

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'per': self.personal,
            's_i': self.short_items,
            's_e': self.short_emojis,
        }