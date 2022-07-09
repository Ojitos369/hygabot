import json
import discord
from datetime import datetime
from funciones.generales import Generales
class Forge(Generales):
    def remplazar_forja_name(self, nombre):
        lista = {
            "divan_helmet": "helmet_of_divan",
            "divan_chestplate": "chestplate_of_divan",
            "divan_leggings": "leggings_of_divan",
            "divan_boots": "boots_of_divan",
            "gemstone": "gem",
            "gem": "gemstone"
        }
        for key_o, value_o in lista.items():
            key = key_o.replace("_", " ")
            value = value_o.replace("_", " ")
            nombre = nombre.replace(key, value)
        return nombre
    
    def forge(self, msg = '', text = ''):
        self.config()
        # -------------- Separacion de datos buscando opciones y usuario ----------------
        separado = text.split(' ')
        username = separado[0]
        try:
            perfil_name = separado[1]
        except:
            perfil_name = ''
        
        try:
            username = self.get_username(username)
        except:
            return msg.reply('Revise que el usuario este bien escrito')

        # -------------- Obtencion de datos ----------------
        try:
            datos, perfil_name, uuid = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        #open(f'./info_pruebas/{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            return msg.reply('Verifica que el Usuario este bien escrito')
        if datos == 'perfil':
            return msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')
        username = self.for_tsuru(username)

        # -------------- Obtencion de datos ----------------
        # open json data
        with open('./json/forja_data.json') as data:
            forja_time_data = json.load(data)
        datos_resultado = {}
        forge_data = datos['forge']['forge_processes']['forge_1']
        procesos = 0
        for i in range(1, 6):
            try:
                datos_forja = forge_data[f'{i}']
                item = datos_forja['id'].lower().replace('_', ' ')
                item = self.remplazar_forja_name(item)
                inicio = datos_forja['startTime']
                slot = datos_forja['slot']
                tiempo_transucrrido = self.obtener_tiempo_relativo_inverso(inicio)
                nombre_temp = f'{item.lower().replace(" ", "_")}'
                tiempo_total = forja_time_data[f'{nombre_temp}']
                # Obtencion de tiempo faltante o sobrante
                print(tiempo_total)
                tiempo_de_forja_sepadado = tiempo_total.split(', ') # d, h, m
                tiempo_transucrrido_sepadado = tiempo_transucrrido.split(', ') # (d), h, m, s
                minutos_en_forja = 0
                if 'd' in tiempo_total:
                    minutos_en_forja += int(tiempo_de_forja_sepadado[0].replace('d', '')) * 60 * 24 * 60
                    minutos_en_forja += int(tiempo_de_forja_sepadado[1].replace('h', '')) * 60 * 60
                    minutos_en_forja += int(tiempo_de_forja_sepadado[2].replace('m', '')) * 60
                else:
                    minutos_en_forja += int(tiempo_de_forja_sepadado[0].replace('h', '')) * 60 * 60
                    minutos_en_forja += int(tiempo_de_forja_sepadado[1].replace('m', '')) * 60

                minutos_transucrrido = 0
                if 'dia' in tiempo_transucrrido:
                    minutos_transucrrido += int(tiempo_transucrrido_sepadado[0].replace('dias', '').replace('dia', '')) * 60 * 24 * 60
                    minutos_transucrrido += int(tiempo_transucrrido_sepadado[1].replace('h', '')) * 60 * 60
                    minutos_transucrrido += int(tiempo_transucrrido_sepadado[2].replace('m', '')) * 60
                    minutos_transucrrido += int(tiempo_transucrrido_sepadado[3].replace('s', ''))
                else:
                    minutos_transucrrido += int(tiempo_transucrrido_sepadado[0].replace('h', '')) * 60 * 60
                    minutos_transucrrido += int(tiempo_transucrrido_sepadado[1].replace('m', '')) * 60
                    minutos_transucrrido += int(tiempo_transucrrido_sepadado[2].replace('s', ''))
                
                tiempo_faltante = minutos_en_forja - minutos_transucrrido
                if tiempo_faltante < 0:
                    negativo = True
                else:
                    negativo = False
                tiempo_faltante = abs(tiempo_faltante)
                segundos = tiempo_faltante % 60
                minutos = (tiempo_faltante // 60) % 60
                horas = (tiempo_faltante // 60 // 60) % 24
                dias = (tiempo_faltante // 60 // 60 // 24)
                tiempo_transucrrido = ""
                if not dias == 0:
                    tiempo_transucrrido += f'{dias} días, '
                if not (horas == 0 and dias == 0):
                    tiempo_transucrrido += f'{horas}h, '
                if not (minutos == 0 and horas == 0 and dias == 0):
                    tiempo_transucrrido += f'{minutos}m, '
                tiempo_transucrrido += f'{segundos}s'
                datos_resultado[i] = {
                    'item': item,
                    'slot': slot,
                    'tiempo': tiempo_transucrrido,
                    'inicio': inicio,
                    'negativo': negativo
                }
                procesos += 1
            except:
                pass
        # -------------- Creacion del embed ----------------
        title = f'Forja de {username} en {perfil_name}'
        description = f'{procesos} items en forja'
        color = self.color_aleatorio()
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
        for i in range(1, 6):
            if i in datos_resultado:
                item = datos_resultado[i]['item'].capitalize()
                item = self.get_emoji_name(item)
                slot = datos_resultado[i]['slot']
                tiempo = datos_resultado[i]['tiempo']
                inicio = datos_resultado[i]['inicio']
                negativo = datos_resultado[i]['negativo']
                name = f'Slot {i}: {item}'
                value = '```'
                if negativo:
                    value += f'Termino hace: {tiempo.replace("-", "")}\n'
                else:
                    value += f'Listo en: {tiempo}\n'
                value += '```'

                embed.add_field(name=name, value=value, inline=False)
            else:
                name = f'Slot {i}:'
                value = '```'
                value += f'El slot {i} esta vacio'
                value += '```'
                embed.add_field(name=name, value=value, inline=False)
        return msg.reply(embed=embed)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'for': self.forge,
            'forge': self.forge,
            'forja': self.forge
        }