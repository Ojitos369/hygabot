import os


import os
import ast
import requests
import json
import discord
from mojang import MojangAPI
from datetime import datetime, timezone, timedelta

class Item:
    def decode_inventory_data(raw, unzip=True):
        from base64 import b64decode as one
        from gzip import decompress as two
        from io import BytesIO as three
        from struct import unpack
        import io
        """Takes a raw string representing inventory data.
        Returns a json object with the inventory's contents"""

        raw = three(two(one(raw))) if unzip else raw# Unzip raw string from the api
        raw = io.BytesIO(raw) if isinstance(raw, bytes) else raw
        def read(_type, length):
            if _type in 'chil':
                return int.from_bytes(raw.read(length), byteorder='big')
            if _type == 's':
                return raw.read(length).decode('utf-8')
            return unpack('>' + _type, raw.read(length))[0]

        def parse_list():
            subtype = read('c', 1)
            payload = []
            for _ in range(read('i', 4)):
                parse_next_tag(payload, subtype)
            return payload

        def parse_compound():
            payload = {}
            while parse_next_tag(payload) != 0:     # Parse tags until we find an endcap (type == 0)
                pass  # Nothing needs to happen here
            return payload

        payloads = {
            1: lambda: read('c', 1),  # Byte
            2: lambda: read('h', 2),  # Short
            3: lambda: read('i', 4),  # Int
            4: lambda: read('l', 8),  # Long
            5: lambda: read('f', 4),  # Float
            6: lambda: read('d', 8),  # Double
            7: lambda: raw.read(read('i', 4)),    # Byte Array
            8: lambda: read('s', read('h', 2)),     # String
            9: parse_list,    # List
            10: parse_compound,     # Compound
            11: lambda: [read('i', 4) for _ in range(read('i', 4))],  # Int Array
            12: lambda: [read('l', 8) for _ in range(read('i', 4))]     # Long Array
        }

        def parse_next_tag(dictionary, tag_id=None):
            if tag_id is None:    # Are we inside a list?
                tag_id = read('c', 1)
                if tag_id == 0:     # Is this the end of a compound?
                    return 0
                name = read('s', read('h', 2))

            payload = payloads[tag_id]()
            if isinstance(dictionary, dict):
                dictionary[name] = payload
            else:
                dictionary.append(payload)

        raw.read(3)     # Remove file header (we ingore footer)
        root = {}
        parse_next_tag(root)
        return root

class Generales:
    o_3695 = 885643862008270858
    o_369 = 673397248427556887
    developers_ids = [o_369, o_3695]
    hypixel_api = ''
    prefijo = ''
    with open('./json/emojis.json') as datos:
        datos = json.load(datos)
    emojis = datos
    with open('./json/datos.json') as datos:
        datos = json.load(datos)
    apis = ast.literal_eval(os.environ.get('HYPIXEL_APIS', '[]'))
    api_used = 0
    funciones = {}
    emojis_saved = {}
    numeros = {
            0: ':zero:',
            1: ':one:',
            2: ':two:',
            3: ':three:',
            4: ':four:',
            5: ':five:',
            6: ':six:',
            7: ':seven:',
            8: ':eight:',
            9: ':nine:'
        }

    def for_tsuru(self, username):
        return username

    def get_username(self, username):
        self.config()
        uuid = MojangAPI.get_uuid(username)
        link_base_player = 'https://api.hypixel.net/player'
        primero = f'{link_base_player}?key='
        segundo = f'&uuid={uuid}'
        player = self.consulta(primero, segundo)
        username = player['player']['displayname']
        # save player as json
        #open (f'./{username}_player.json', 'w').write(json.dumps(player, indent=4))
        return username

    def get_emoji_name(self, item_name):
        original_name = item_name
        if original_name in self.emojis_saved:
            return self.emojis_saved[item_name]
        if '[lvl' in item_name.lower() and ']' in item_name.lower() and 'pet' not in item_name.lower():
            item_name += ' pet '
        remplazos = {
            "-": "_",
            " ": "_",
            "'": "",
            "gemsotne": "gem",
            "gem": "gemstone"
        }
        name_aux = item_name.lower()
        for key, value in remplazos.items():
            name_aux = name_aux.replace(key, value)
        opciones = []
        if name_aux in self.emojis:
            if '[lvl' in item_name.lower() and ']' in item_name.lower():
                item_name = item_name.replace(' pet ', '')
                item_name = item_name.replace(' Pet ', '')
            item_name = self.emojis[name_aux].split()[0] + ' ' + item_name
            self.emojis_saved[original_name] = item_name
            return item_name
        for nombre in self.emojis.keys():
            esta = True
            nombre_separado = nombre.split('_')
            no_coincidencias = 0
            name_separado = nombre.split('_')
            for nombre_separado in name_separado:
                if nombre_separado not in name_aux:
                    esta = False
                    break
                no_coincidencias += 1
            if esta:
                opciones.append([no_coincidencias, nombre])
        if len(opciones) > 0:
            mayor = 0
            opcional = ''
            for opcion in opciones:
                if opcion[0] > mayor:
                    emoji_id = self.emojis[opcion[1]].split(' ')[0]
                    opcional = emoji_id + ' ' + item_name
                    mayor = opcion[0]
            if opcional != '':
                item_name = opcional
        if '[lvl' in item_name.lower() and ']' in item_name.lower():
            item_name = item_name.replace(' pet ', '')
            item_name = item_name.replace(' Pet ', '')
        self.emojis_saved[original_name] = item_name
        return item_name

    def auction_emoji(self, name):
        flexible = False
        name = name.lower()
        if '-in' in name:
            name = name.replace('-in', '')
            flexible = True
        name = name.replace(' ', '_')
        with open(f'./json/auction_data.json', 'r') as datos:
            datos = json.load(datos)
        emoji = ''
        if flexible:
            for key, value in datos.items():
                if name in key or key in name:
                    emoji = value.split()[0]
                    break
        else:
            try:
                emoji = datos[name].split()[0]
            except:
                pass
        return emoji
    
    def obtener_perfil(self, username, perfil_name, id = False, uuid = False):
        self.config()
        # ------------- verificar Obtener Perfiles -------------
        uuid = MojangAPI.get_uuid(username)

        link_base_player = 'https://api.hypixel.net/player'
        primero = f'{link_base_player}?key='
        segundo = f'&uuid={uuid}'
        player = self.consulta(primero, segundo)
        
        try:
            profiles = player['player']['stats']['SkyBlock']['profiles']
        except:
            print(player['cause'])
            return 'usuario'
        keys = []
        for key in profiles.keys():
            keys.append(key)
            # ------------- verificarificando si se especifico el perfil ----------------
        verificado = False
        if perfil_name == '':
            ultima_actualizacion = 0
            for key in profiles.keys():
                link_base_player = 'https://api.hypixel.net/skyblock/profile'
                primero = f'{link_base_player}?key='
                segundo = f'&profile={key}'
                player = self.consulta(primero, segundo)
                last_save = player['profile']['members'][uuid]['last_save']
                temp_perfil_name = profiles[key]['cute_name']
                if last_save > ultima_actualizacion:
                    ultima_actualizacion = last_save
                    perfil_name = temp_perfil_name
                    perfil_id = key
            verificado = True
        
        if not verificado:
            perfil_correcto = False
            for key in profiles.keys():
                if profiles[key]['cute_name'].lower() == perfil_name.lower():
                    perfil_correcto = True
                    perfil_id = key
                    break
            if not perfil_correcto:
                return 'perfil'

        link_base_player = 'https://api.hypixel.net/skyblock/profile'
        primero = f'{link_base_player}?key='
        segundo = f'&profile={perfil_id}'
        player = self.consulta(primero, segundo)
        if id:
            return perfil_id
        if uuid:
            return player['profile']['members'][uuid], perfil_name.capitalize(), uuid
        else:
            return player['profile']['members'][uuid], perfil_name.capitalize()

    def consulta(self, inicio, fin = ''):
        link_api = f'{inicio}{self.hypixel_api}{fin}'
        hydata = requests.get(link_api).json()
        paso = False
        while not paso:
            if 'success' in hydata and 'throttle' not in hydata:
                paso = True
            else:
                n = (self.api_used + 1) % len(self.apis)
                self.api_used = n
                self.config(n = n)
                link_api = f'{inicio}{self.hypixel_api}{fin}'
                hydata = requests.get(link_api).json()
                paso = False
        return hydata
    
    def convertir_fecha(self, fecha):
        return datetime.strptime(datetime.fromtimestamp(fecha // 1000.0).strftime('%d-%m-%Y') ,'%d-%m-%Y')
    
    def convertir_fecha_completa(self, fecha):
        return datetime.strptime(datetime.fromtimestamp(fecha // 1000.0).strftime('%d-%m-%Y - %H:%M:%S') ,'%d-%m-%Y - %H:%M:%S')

    def obtener_tiempo_relativo(self, fecha):
        date_in_utc_0 = datetime.utcnow()
        date_in_utc_0 = date_in_utc_0 #- timedelta(hours=5)
        fecha_completa = self.convertir_fecha_completa(fecha)
        diferencia = fecha_completa - date_in_utc_0
        diferencia = str(diferencia).split(',')
        if len(diferencia) > 1:
            dias = diferencia[0]
            tiempo = diferencia[1].replace(' ', '').split(':')
        else:
            dias = '0'
            tiempo = diferencia[0].replace(' ', '').split(':')
        horas = str(tiempo[0])
        minutos = str(tiempo[1])
        segundos = f'{float(tiempo[2]):,.0f}'
        diferencia = f'{horas}h, {minutos}m, {segundos}s'
        if dias != '0':
            diferencia = f'{dias}, {diferencia}'.replace('day', 'dia')
        return diferencia

    def recomb_item(self):
        return self.emojis['recombobulator_3000'].split(' ')[0]

    def obtener_tiempo_relativo_inverso(self, fecha):
        date_in_utc_0 = datetime.utcnow()
        date_in_utc_0 = date_in_utc_0 #- timedelta(hours=5)
        fecha_completa = self.convertir_fecha_completa(fecha)
        diferencia = date_in_utc_0 - fecha_completa
        diferencia = str(diferencia).split(',')
        if len(diferencia) > 1:
            dias = diferencia[0]
            tiempo = diferencia[1].replace(' ', '').split(':')
        else:
            dias = '0'
            tiempo = diferencia[0].replace(' ', '').split(':')
        horas = str(tiempo[0])
        minutos = str(tiempo[1])
        segundos = f'{float(tiempo[2]):,.0f}'
        diferencia = f'{horas}h, {minutos}m, {segundos}s'
        if dias != '0':
            diferencia = f'{dias}, {diferencia}'.replace('day', 'dia')
        return diferencia

    def redondear_letras(self, cantidad):
        cantidad = float(cantidad.replace(',', ''))
        if cantidad >= 1000000000:
            cantidad = f'{cantidad / 1000000000:,.2f}b'
        elif cantidad >= 1000000:
            cantidad = f'{cantidad / 1000000:,.2f}m'
        elif cantidad >= 1000:
            cantidad = f'{cantidad / 1000:,.2f}k'
        else:
            cantidad = f'{cantidad:,.0f}'
        return cantidad

    def color_aleatorio(self):
        import random
        colour = random.randint(0, 0xFFFFFF)
        return colour

    def remplazar(self, item):
        new = ''
        n = 0
        while n < len(item):
            if item[n] == '§':
                n += 1
            else:
                new += item[n]
            n += 1
        return new
    
    def correccion_opciones(self, item):
        ''' opciones = ['-d ', '-b ', '-detalles ', '-detallado ', '-busqueda ', '-buscar ']
        for opc in opciones:
            if opc in item:
                item = item.replace(opc, opc[:-1])
                item = item.replace(opc[:-1], opc) '''
        return item

    def revisar(self, text):
        self.config()
        self.prefijo = text.split(' ')[0]
        largo_prefijo = len(self.prefijo)
        text = text[(largo_prefijo + 1):]
        actividad = text.split()[0].lower()
        if actividad in self.funciones:
            return True
        else:
            return False

    def accion(self, msg, text, client):
        self.config()
        self.prefijo = text.split(' ')[0]
        largo_prefijo = len(self.prefijo)
        text = text[(largo_prefijo + 1):]
        actividad = text.split()[0].lower()
        recomendados = ['recomendaciones', 'recomendacion', 'sugerencia', 'sugerencias', 'sugerir', 'sug', 'rec', 'em']
        if actividad in self.funciones:
            if actividad not in recomendados:
                return self.funciones[f'{actividad}'](msg = msg, text = text[(len(actividad) + 1):])
            else:
                return self.funciones[f'{actividad}'](msg = msg, text = text[(len(actividad) + 1):], client = client)
            """ try:
                if actividad not in recomendados:
                    return self.funciones[f'{actividad}'](msg = msg, text = text[(len(actividad) + 1):])
                else:
                    return self.funciones[f'{actividad}'](msg = msg, text = text[(len(actividad) + 1):], client = client)
            except:
                return msg.channel.send(f'Revise que el comando este bien escrito. Verifique los comandos con {self.prefijo}help') """
        else:
            return msg.channel.send(f'Revise que el comando este bien escrito. Verifique los comandos con {self.prefijo}help')
    
    def extra_replace(self, text):
        text = text.lower().replace(' ', '_')
        text = text.replace('Ink_sack:3', 'Cocoa beans')
        text = text.replace('Ink_sack:4', 'Lapis lazuli')
        text = text.replace('log:1', 'Spruce Log')
        text = text.replace('log_2:1', 'Dark Oak Log')
        text = text.replace('log_2', 'Acacia Log')
        text = text.replace('log:2', 'Birch Log')
        text = text.replace('log:3', 'Jungle Log')
        if text == 'log':
            text = text.replace('log', 'Oak Log')
        text = text.replace('_', ' ').capitalize()
        return text
class Full:
    def execute(self, msg, text, actions, prefijo, client):
        encontrada = False
        for action in actions:
            if action.revisar(text):
                res = action.accion(msg, text, client)
                encontrada = True
                break
        if encontrada:
            return res
        
