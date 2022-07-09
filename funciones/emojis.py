import json
import discord
from datetime import datetime
from funciones.generales import Generales
class Emojis(Generales):
    def remplazos_emoji(self, texto):
        remplazos = {
            "divan_helmet": "helmet_of_divan",
            "divan_chestplate": "chestplate_of_divan",
            "divan_leggings": "leggings_of_divan",
            "divan_boots": "boots_of_divan",
        }
        for key, value in remplazos.items():
            texto = texto.replace(key, value)
        return texto

    def emoji(self, msg = '', text = '', client = ''):
        separado = text.split(' ')
        # ---------- Verificar remplazo ----------
        posicion = -1
        remplazar = False
        for i in range(len(separado)):
            if '-r' == separado[i]:
                remplazar = True
                posicion = i
                break
        if posicion != -1:
            separado.pop(posicion)
        
        # ---------- Verificar nombre ----------
        posicion = -1
        for i in range(len(separado)):
            if '-n' == separado[i]:
                try:
                    nombre_archivo = separado[i+1]
                    posicion = i
                    break
                except:
                    return msg.reply('Despues de -n debes especificar nombre')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        else:
            nombre_archivo = 'emojis'        
        if msg.author.id not in self.developers_ids:
            return msg.reply("Just bot's developers can use this command.")
        texto = ' '.join(separado)
        if len(texto) > 1:
            return msg.reply('Revisa el comando')
        print(msg.author.id)
        with open(f'./json/{nombre_archivo}.json', 'r') as datos:
            datos = json.load(datos)
        emojis = datos
        guild = msg.guild
        emojisg = guild.emojis
        data = []
        repetidos = 0
        for emoji in emojisg:
            data.append([emoji.name, emoji.id])
        respuesta = ''
        agregados = ''
        respuesta = ''
        agregados = 0
        for emoji in data:
            nombre = emoji[0]
            id = emoji[1]
            key = self.remplazos_emoji(nombre)
            if key not in emojis:
                emojis[key] = f'<:{nombre}:{id}> {guild}'
                agregados += 1
            else:
                if remplazar:
                    emojis[nombre] = f'<:{nombre}:{id}> {guild}'
                    respuesta += f'Quitar {nombre} de {guild}.\n'
                else:
                    respuesta += f'{nombre} ya está en {guild}.\n'
                repetidos += 1
        respuesta += f'Se agregaron {agregados} emojis'
        respuesta += f'\nSe evitaron {repetidos} emojis repetidos'
        #save json with identation of 4
        with open(f'./json/{nombre_archivo}.json', 'w') as outfile:
            json.dump(emojis, outfile, indent=4)
        self.ordenar(text=nombre_archivo)
        return msg.reply(respuesta)

    def delete_emoji(self, msg = '', text = '', client = ''):
        if '-r' in text:
            remplazar = True
        else:
            remplazar = False
        o_3695 = 885643862008270858
        o_369 = 673397248427556887
        developers_ids = [o_369, o_3695]
        if msg.author.id not in developers_ids:
            return msg.reply("Just bot's developers can use this command.")
        guild = msg.guild
        emojisg = guild.emojis
        acciones = []
        borrados = 0
        for emoji in emojisg:
            acciones.append(emoji.delete())
            borrados += 1
        acciones.append(msg.reply(f'Borrados {borrados}'))
        mensajes = {
            'borrar': True,
            'not_embed': True,
            'respuesta': acciones
        }
        return mensajes

    def ordenar(self, msg='', text = ''):
        if text != '':
            nombre_archivo = text
        with open(f'./json/{nombre_archivo}.json', 'r') as datos:
            datos = json.load(datos)
        emojis = datos

        key_list_order = {}
        help_list = []
        # ordenar por key
        for key in emojis.keys():
            help_list.append(key)
        help_list.sort()
        for key in help_list:
            key_list_order[key] = emojis[key]

        with open(f'./json/{nombre_archivo}.json', 'w') as outfile:
            json.dump(key_list_order, outfile, indent=4)
        try:
            return msg.reply('Ordenados')
        except:
            return
    
    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'em': self.emoji,
            'ema': self.ordenar
        }
        pendientes = {
            'cem':self.delete_emoji,
            'rmem': self.delete_emoji,
            'rem': self.delete_emoji,
        }
