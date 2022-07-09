import requests
import pytz
import json
import time
import discord
import random
import requests
import os
import ast
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from mojang import MojangAPI
from datetime import datetime, timezone, timedelta
from slash.eventos import Evento
from conexion import conexion, ConnectionDB

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

class Generales(Evento):
    o_3695 = 885643862008270858
    o_369 = 673397248427556887
    dfot = 449754781854990346
    jalufo = 618743923912867851
    gearl = 386270777420414977
    ykzj = 458022683611758601
    ferqo = 299039228136783872
    my_guilds_ids = [ 877247888516874251, 883227982527864852, 883615794821488640, 891239816006606899, 892595203238686720, 892595534018281523, 892596025783644240, 892596105139879986, 892644804062773269, 892816516989452358, 892817556484800522, 892820579143540736, 892825970116018237, 892901481215320065, 892936647287648267, 892936727365308426, 905665427101872138, 917529870605639791]
    developers_ids = [o_369, o_3695, dfot, jalufo, gearl, ferqo]
    event_ids = [o_369, gearl, ykzj]
    hypixel_api = ''
    prefijo = ''
    with open('./json/emojis.json') as datos:
        datos = json.load(datos)
    emojis = datos
    apis = ast.literal_eval(os.environ.get('HYPIXEL_APIS', '[]'))
    with open('./json/general_emoji.json') as datos:
        datos = json.load(datos)
    general_emojis = datos
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

    def get_username(self, username = '', uuid = ''):
        self.config()
        try:
            if uuid == '':
                uuid = MojangAPI.get_uuid(username)
            link_base_player = 'https://api.hypixel.net/player'
            primero = f'{link_base_player}?key='
            segundo = f'&uuid={uuid}'
            player = self.consulta(primero, segundo)
            username  = player['player']['displayname']
        except:
            pass
        return username

    def get_emoji_name(self, item_name, just_emoji = False):
        original_name = item_name
        if original_name.lower().replace(' ',' _') in self.emojis_saved:
            if just_emoji:
                return self.emojis_saved[item_name.lower().replace(' ',' _')]['emoji']
            else:
                return self.emojis_saved[item_name.lower().replace(' ',' _')]['name']
        emoji_string = ''
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
        emojis = {}
        for pal in name_aux.split('_'):
            try:
                if pal[0] in self.emojis:
                    emojis.update(self.emojis[pal[0]])
            except:
                pass
        if name_aux in emojis:
            if '[lvl' in item_name.lower() and ']' in item_name.lower():
                item_name = item_name.replace(' pet ', '')
                item_name = item_name.replace(' Pet ', '')
            item_name = emojis[name_aux].split()[0] + ' ' + item_name
            self.emojis_saved[original_name] = item_name
            return item_name
        
        for nombre in emojis.keys():
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
                    emoji_id = emojis[opcion[1]].split(' ')[0]
                    opcional = emoji_id + ' ' + item_name
                    mayor = opcion[0]
                    emoji_string = emoji_id
            if opcional != '':
                item_name = opcional
        if '[lvl' in item_name.lower() and ']' in item_name.lower():
            item_name = item_name.replace(' pet ', '')
            item_name = item_name.replace(' Pet ', '')
        self.emojis_saved[original_name.lower().replace(' ', '_')] = {
            'name': item_name,
            'emoji': emoji_string
        }
        if just_emoji:
            return emoji_string
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
    
    def general_emoji(self, text):
        emojis = self.general_emojis
        text = text.lower().replace(' ', '_')
        if text in emojis:
            return emojis[text].split()[0]
        return ''

    def obtener_perfil(self, username, perfil_name, id = False, uuid = False, uuid_key = ''):
        self.config()
        # ------------- verificar Obtener Perfiles -------------
        if uuid_key == '':
            uuid_key = MojangAPI.get_uuid(username)

        link_base_player = 'https://api.hypixel.net/player'
        primero = f'{link_base_player}?key='
        segundo = f'&uuid={uuid_key}'
        player = self.consulta(primero, segundo)
        try:
            username  = player['player']['displayname']
        except:
            return 'usuario'
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
                last_save = player['profile']['members'][uuid_key]['last_save']
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
            return player['profile']['members'][uuid_key], perfil_name.capitalize(), uuid_key, username
        else:
            return player['profile']['members'][uuid_key], perfil_name.capitalize(), username

    def consulta(self, inicio, fin = ''):
        self.config()
        link_api = f'{inicio}{self.hypixel_api}{fin}'
        res = False
        while not res:
            hydata = requests.get(link_api)
            try:
                hydata = hydata.json()
                res = True
            except:
                pass
        paso = False
        while not paso:
            if 'success' in hydata and 'throttle' not in hydata:
                paso = True
            else:
                print(hydata)
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
        # get current date with pytz
        date_in_utc_0 = datetime.now(pytz.utc)
        date_in_utc_0 = datetime.strptime(date_in_utc_0.strftime('%d-%m-%Y - %H:%M:%S') ,'%d-%m-%Y - %H:%M:%S')
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
            anios = '0'
            if abs(int(dias.split()[0])) > 365:
                anios = int(dias.split()[0]) // 365
                dias = int(dias.split()[0]) % 365
                if dias > 1:
                    dias = f'{dias} dias'
                else:
                    dias = f'{dias} dia'
                diferencia = f'{anios}años, {dias}, {diferencia}'
            else:
                diferencia = f'{dias}, {diferencia}'.replace('day', 'dia')
        return diferencia

    def recomb_item(self):
        return self.emojis['r']['recombobulator_3000'].split(' ')[0]

    def obtener_tiempo_relativo_inverso(self, fecha):
        # get current date with pytz
        date_in_utc_0 = datetime.now(pytz.utc)
        date_in_utc_0 = datetime.strptime(date_in_utc_0.strftime('%d-%m-%Y - %H:%M:%S') ,'%d-%m-%Y - %H:%M:%S')
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
        cantidad = float(str(cantidad).replace(',', ''))
        if cantidad < 0:
            negativo = True
        else:
            negativo = False
        cantidad = abs(cantidad)
        if cantidad >= 1000000000:
            cantidad = f'{cantidad / 1000000000:,.2f}b'
        elif cantidad >= 1000000:
            cantidad = f'{cantidad / 1000000:,.2f}m'
        elif cantidad >= 1000:
            cantidad = f'{cantidad / 1000:,.2f}k'
        else:
            cantidad = f'{cantidad:,.0f}'
        if negativo:
            cantidad = f'-{cantidad}'
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

    def bazar_replace(self, text):
        def formato_lindo(text):
            return text.replace('_', ' ').title()
        text = text.lower().replace(' ', '_')
        replaces_dinamics = {
            "amber_gem": "amber_gemstone",
            "amethyst_gem": "amethyst_gemstone",
            "jade_gem": "jade_gemstone",
            "jasper_gem": "jasper_gemstone",
            "ruby_gem": "ruby_gemstone",
            "sapphire_gem": "sapphire_gemstone",
            "topaz_gem": "topaz_gemstone",
        }
        replaces_fijos = {
            "ink_sack:3": "cocoa_beans",
            "ink_sack:4": "lapis_lazuli",
            "log:1": "spruce_log",
            "log_2:1": "dark_oak_log",
            "log_2": "acacia_log",
            "log:2": "birch_log",
            "log:3": "jungle_log",
            "log": "oak_log",
            "raw_fish:1": "raw_salmon",
            "raw_fish:2": "clownfish",
            "raw_fish:2": "pufferfish"
        }
        for replace in replaces_fijos:
            if text == replace:
                text = replaces_fijos[replace]
                return formato_lindo(text)
        for replace in replaces_dinamics:
            text = text.replace(replace, replaces_dinamics[replace])
        return formato_lindo(text)

    def calculadora(self, operacion, letras = False, numeros = False, entero = False, impresion = False):
        #print(operacion)
        full = True
        if letras or numeros or impresion:
            full = False
        remplazos = {
            'k': ' * 1000',
            'm': ' * 1000000',
            'b': ' * 1000000000'
        }
        op_original = operacion
        operacion = operacion.lower()
        for key, value in remplazos.items():
            operacion = operacion.replace(key, value)
        text = operacion
        try:
            resultado = eval(text)
        except:
            return 'error'
        letra = self.redondear_letras(float(resultado))
        if full:
            if entero:
                resultado = '{:,.0f}'.format(float(resultado)) + f' ({letra})'
            else:
                resultado = '{:,.2f}'.format(float(resultado)) + f' ({letra})'
        elif letras:
            resultado = f'{letra}'
        elif numeros:
            if entero:
                resultado = int(resultado)
            else:
                resultado = float(resultado)
        elif impresion:
            if entero:
                resultado = '{:,.0f}'.format(float(resultado))
            else:
                resultado = '{:,.2f}'.format(float(resultado))
        return resultado

    def get_verify_user(self, id):
        try:
            query = f"SELECT uuid FROM verificados WHERE id = '{id}'"
            userdata = self.query_consulta(query)
            #print(userdata)
            if len(userdata) == 0:
                return ''
            else:
                return userdata[0][0]
        except:
            return ''

    def query_consulta(self, query, db = ''):
        from conexion import conexion, ConnectionDB
        mi_conexion = conexion(db)
        cursor = mi_conexion.cursor()
        cursor.execute(query)
        mi_conexion.commit()
        res = cursor.fetchall()
        mi_conexion.close()
        return res

    def query_ejecutar(self, query, db = ''):
        from conexion import conexion
        mi_conexion = conexion(db)
        cursor = mi_conexion.cursor()
        cursor.execute(query)
        mi_conexion.commit()
        mi_conexion.close()
    
    def fecha_plana(self):
        now = datetime.now()

        segundos = int(datetime.strftime(now, '%s'))
        minutos = int(datetime.strftime(now, '%M')) * 60
        horas = int(datetime.strftime(now, '%H')) * 3600
        dias = int(datetime.strftime(now, '%d')) * 86400
        meses = int(datetime.strftime(now, '%m')) * 2592000
        anios = int(datetime.strftime(now, '%Y')) * 31536000

        ahora = segundos + minutos + horas + dias + meses + anios
        
        return ahora

    def check_button(self, i, b):
            return (i.author == self.original_msg.author or i.author.id in self.developers_ids) and i.message.id == self.msg.id

    async def guardado_de_embeds(self, guardar, id_msg, msg, paginas):
        if paginas > 1:
            open(f'./embeds_data/emb_data.json', 'w').write(json.dumps(guardar, indent=4))
            await msg.channel.send(f'+load {id_msg}')
            await msg.add_reaction('\U000025B6')
            if paginas > 2:
                await msg.add_reaction('⏩')

    async def esperando_boton_embed(self, msg, embeds, data_emb = [], menu = False, abierto = False):
        def check(i, b):
            if abierto:
                return i.message.id == self.msg.id
            return (i.author == self.original_msg.author or i.author.id in self.developers_ids) and i.message.id == self.msg.id
        
        def check_selection(i: discord.Interaction, select_menu):
            return i.author == self.original_msg.author and i.message.id == self.msg.id
        
        ultima = self.fecha_plana()
        esperando = True
        while esperando:
            ahora = self.fecha_plana()
            try:
                val = None
                
                if menu:
                    interaccion, select_menu = await self.bot.wait_for('selection_select', check=check_selection, timeout=2)
                    val = select_menu.values[0]
                else:
                    interaccion, boton = await self.bot.wait_for("button_click", check=check, timeout=2)
                    val = boton.custom_id
                
                val = int(val)
                #print(f'{val}: {type(val)}')
                
                await msg.clear_reactions()
                mensajes = embeds[val]
                try:
                    await interaccion.edit(content = '', embed = mensajes[0])
                except:
                    await interaccion.edit(content = '', embed = mensajes)
                # ------------- Funcion dependiendo del slayer -----------------
                try:
                    embeds_data = data_emb[val]
                except:
                    embeds_data = []
                paginas_totales = len(embeds_data)
                if paginas_totales > 1:
                    user_id = self.original_msg.author.id
                    id_mensaje = msg.id
                    guardar = {
                        'msg_id': id_mensaje,
                        'user_id': user_id,
                        'embeds': embeds_data,
                    }
                    await self.guardado_de_embeds(guardar, id_mensaje, msg, paginas_totales)
                ultima = ahora
            except:
                pass
            
            #print(abs(ahora - ultima))
            if abs(ahora - ultima) > 120:
                try:
                    await self.interaccion.edit(components = [])
                except:
                    await self.msg.edit(components = [])
                return

    def inv_filtro(self, data):
        full_datos = []
        cantidad_original = 0
        cantidad_total = 0
        elementos_per_page = 45
        pagina_actual = 0
        for dato in data:
            cantidad_original += 1
            if "tag" in dato:
                cantidad_total += 1
                cantidad = dato["Count"]
                item_name = self.remplazar(dato["tag"]["display"]["Name"])
                nombre = self.get_emoji_name(item_name)
                if cantidad > 1:
                    nombre += f" - x{cantidad}"
                # ---------- Cambiando nombre para libros encantados ----------
                libro = False
                book_replace = ''
                if item_name.lower() == 'enchanted book':
                    #book_replace = self.remplazar(item_bytes['tag']['display']['Lore'][0])
                    #print(dato)
                    enchants = dato['tag']['ExtraAttributes']['enchantments']
                    for ench, lvl in enchants.items():
                        if len(book_replace) > 200:
                            book_replace += '...'
                            break
                        else:
                            book_replace += f'{ench.capitalize().replace("_"," ")} {lvl}, '
                if book_replace.endswith(', '):
                    book_replace = book_replace[:-2]

                    libro = True

                if nombre != 'SkyBlock Menu (Right Click)':
                    lore = ''
                    full_lore = dato["tag"]["display"]["Lore"]
                    dato_extra = full_lore.pop()
                    dato_extra = self.remplazar(dato_extra)
                    for lor in full_lore:
                        lore += f'{self.remplazar(lor)}\n'
                    extra_datos = dato["tag"]["ExtraAttributes"]
                    # ---------  Recombs ------------
                    try: 
                        if extra_datos['rarity_upgrades'] == 1:
                            lore += f'Item Recombulado\n'
                            nombre += ' ' + self.recomb_item()
                    except:
                        pass
                    # ---------  Potatos Books ------------
                    try:
                        potatos = extra_datos["hot_potato_count"]
                        if potatos > 10:
                            lore += f'Hot potato books: {10}\n'
                            lore += f'Fuming potato books: {potatos - 10}\n'
                        else:
                            lore += f'Hot potato books: {potatos}\n'
                    except:
                        pass
                    # ---------  Gemas ------------
                    try:
                        gemas = extra_datos["gems"]
                        try:
                            lore += f'Gemas Aplicadas: {gemas["UNIVERSAL_0"]} {gemas["UNIVERSAL_0_gem"]}\n'
                        except:
                            lore += f'Gemas Aplicadas:\n'
                            if "JADE_0" in gemas:
                                lore += f'\t{gemas["JADE_0"]} JADE\n'
                            if "AMBER_0" in gemas:
                                lore += f'\t{gemas["AMBER_0"]} AMBER\n'
                            if "SAPPHIRE_0" in gemas:
                                lore += f'\t{gemas["SAPPHIRE_0"]} SAPPHIRE\n'
                            if "AMETHYST_0" in gemas:
                                lore += f'\t{gemas["AMETHYST_0"]} AMETHYST\n'
                            if "TOPAZ_0" in gemas:
                                lore += f'\t{gemas["TOPAZ_0"]} TOPAZ\n'
                    except:
                        pass
                    if libro:
                        nombre = item_name.replace("Enchanted Book", book_replace)
                    if (cantidad_original % elementos_per_page - 1) == 0:
                        pagina_actual += 1
                    full_datos.append(
                        {
                            'nombre': nombre,
                            'lore': lore,
                            'extra': dato_extra,
                            'cantidad_original': cantidad_original,
                            'total': cantidad_total,
                            'pagina_actual': pagina_actual
                        }
                    )
        return full_datos

    async def get_guilds_names(self, client):
        id_channel = 923377233157050398
        bot_data = client.get_channel(id_channel)
        await bot_data.purge(limit=100)
        guild_msg = ""
        i = 0
        for guild in client.guilds:
            if guild.id not in self.my_guilds_ids:
                i += 1
                guild_msg += f"{i}.- {guild.name}\n"
        await bot_data.send(guild_msg)
        await bot_data.edit(name=f'bot_data_{i}')
        
        # get menbers of guild
        guild_id = 923974129600843817
        channel_voice_id = 924491579710930994
        guid = client.get_guild(guild_id)
        channel_voice = client.get_channel(channel_voice_id)
        members_count = len(guid.members)
        name = f'Hygabot: {members_count} miembros'
        await channel_voice.edit(name=name)

    async def not_spam(self, msg, client):
        if msg.channel.id == 924505042424332348:
            await msg.delete()
            user = msg.author
            guild = msg.guild
            # kick user from server
            await user.kick(reason='Spam')
            
            text_channels = guild.text_channels
            for channel in text_channels:
                messages = await channel.history(limit=50).flatten()
                for message in messages:
                    if message.author == user:
                        while True:
                            try:
                                await message.delete()
                                break
                            except:
                                time.sleep(1)

    async def bienvenida(self, member, client):
        #neko = 745106115934683177
        # hygabot = 923974129600843817
        if member.guild.id == 923974129600843817 and not member.bot:
            # channel_neko = 745106115934683180
            # channel_hygabot = 923974130276122626
            channel_id = 923974130276122626
            channel = client.get_channel(channel_id)
            guild = member.guild
            guild_name = guild.name
            user = member
            saludos_1 = ['Hola', 'Mucho gusto', 'Bienvenid@', 'Welcome']
            saludos_2 = ['Que alegrita tenerte en', 'Disfruta mucho de', 'Espero la pases bien en']
            saludo_1 = random.choice(saludos_1)
            saludo_2 = random.choice(saludos_2)
            content = f'{saludo_1} {user.mention}'
            title = f' {saludo_2} {guild_name}'
            color = self.color_aleatorio()
            user_image = member.avatar_url
            img_data = requests.get(user_image).content
            with open('./img/profile.png', 'wb') as handler:
                handler.write(img_data)
            filename = 'profile.png'
            file_path = f"./img/{filename}"
            file = discord.File(file_path, filename=filename)
            img_url = f"attachment://{filename}"
            embed = discord.Embed(title = title, color = color)
            #embed.set_thumbnail(url = user_image)
            embed.set_image(url=img_url)
            
            # verificar_neko = 877023945189130301
            channel_tag_id = 877023945189130301
            channel_tag = client.get_channel(channel_tag_id)
            # tag channel
            name = 'Recuerda checar: '
            value = f'Reglas: {channel_tag.mention}'
            #embed.add_field(name=name, value=value, inline=False)
            await channel.send(content=content, embed=embed, file=file)
            os.system(f'rm {file_path}')
            # neko_role = 924494211666030682
            # default_role 923976553799499776
            role_id = 923976553799499776
            await member.add_roles(guild.get_role(role_id))
        else:
            return
    
    async def cargar_auction(self, ah_data, client):
        channel_id = 924888247828619284
        channel = client.get_channel(channel_id)
        await channel.send('Checando data')
        await ah_data.check_data(channel)
        await channel.send(f'Data al dia')
        