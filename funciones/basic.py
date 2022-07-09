import json
import discord
import pandas as pd
from datetime import datetime
from os import sys
from time import sleep
from funciones.generales import Generales, Item

class Basicos(Generales):
    last_ah_update = ''
    auction_items = [{} for i in range(100)]
    fecha_de_actualizacion = ''
    
    def hola(self, msg, text):
        import random
        n = random.randint(1, 5)
        try:
            emoji = self.emojis[f'hola_{n}']
        except:
            emoji = '👋'
        return msg.channel.send('Hola, ' + msg.author.mention + ' ' + emoji)

    def operacion(self, msg, text):
        try:
            resultado = eval(text)
        except:
            return msg.reply('No se pudo realizar la operacion')
        resultado = '{:,.2f}'.format(float(resultado))
        color = self.color_aleatorio()
        embed = discord.Embed(title=f'{text}', description=f'Resultado: {resultado}', color = color)
        return msg.reply(embed=embed)

    def limpiar(self, msg = '', text = ''):
        self.config()
        admin = msg.author.guild_permissions.administrator
        if not admin:
            return msg.reply('No tienes permisos para usar este comando')
        ahora = datetime.strptime(datetime.now().strftime('%d-%m-%Y %H:%M:%S'), '%d-%m-%Y %H:%M:%S')
        texto = text.split()
        dias = int(texto.pop())
        guild = ' '.join(texto)
        link_base_player = 'https://api.hypixel.net/player'
        link_base = 'https://api.hypixel.net/guild'
        inicio = f'{link_base}?key='
        fin = f'&name={guild}'
        hydata = self.consulta(inicio, fin)
        metrica = hydata['guild']
        cantidad = 0
        color = self.color_aleatorio()
        embed = discord.Embed(title=f'Limpiando {guild} el {ahora}', description=f'Limpieza de {dias} dias', color = color)
        miembro_cantidad = 0
        for miembro in metrica['members']:
            total = 0
            for valor in miembro['expHistory'].values():
                total += float(valor)
            uuid = miembro["uuid"]
            primero = f'{link_base_player}?key='
            segundo = f'&uuid={uuid}'
            player = self.consulta(primero, segundo)
            try:
                fecha = int(player['player']['lastLogin'])
                ultima_conexion = self.obtener_tiempo_relativo(fecha)
                offline_days = abs(int(ultima_conexion.split(' ')[0]))
                if offline_days >= dias:
                    cantidad += 1
                    value = '```'
                    value += f'Rank: {miembro["rank"]}\n'
                    value += f'Tiempo sin conectarse: {str(self.obtener_tiempo_relativo(fecha)).replace("-", "")}\n'
                    value += '```'
                    embed.add_field(name=f'\n{cantidad}.- Player: {player["player"]["displayname"]}', value=value, inline = False)
                    #print(f'en {cantidad} {miembro_cantidad}/{largo_metrica}')
            except:
                pass
            miembro_cantidad += 1
        embed.set_footer(text = f'{cantidad} Miembros sin conectarse en los ultimos {dias} dias')
        return msg.reply(embed=embed)

    def auction(self, msg = '', text = ''):
        self.config()
        text = self.correccion_opciones(text)
        separado = text.split()
        solo_bin = False
        posicion = 0
        detallado = False
        item_detallado = 0
        mostrar_res = 1
        solo_auction = False
        avanzada = False
        #print(f'separado: {separado}')
        # -------------- Verificando Busqueda ----------------
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-b' or separado[i] == '-buscar' or  separado[i] == '-busqueda':
                try:
                    if separado[i + 1].lower() == 'bin':
                        solo_bin = True
                        filtro = True
                        posicion = i
                        break
                    elif separado[i + 1].lower() == 'auction' or separado[i + 1].lower() == 'ah' or separado[i + 1].lower() == 'au':
                        solo_auction = True
                        filtro = True
                        posicion = i
                        break
                    else:
                        return msg.reply(f'Verifica que el comando este bien escrito "{self.prefijo}help ah"')
                except:
                    return msg.reply('Despues de -d se espera un numero de la lista. Ejemplo: -d 1')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
            
        # -------------- Verificando Detallado ----------------
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-d' or  separado[i] == '-detalles' or  separado[i] == '-detallado':
                try:
                    item_detallado = int(separado[i+1])
                    posicion = i
                    detallado = True
                    break
                except:
                    return msg.reply('Despues de -d se espera un numero de la lista. Ejemplo: -d 1')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)

        # -------------- Verificando Busqueda Avanzada ----------------
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-ba' or separado[i] == '-avanzada' or separado[i] == '-a' or separado[i] == '-avanzado':
                posicion = i
                avanzada = True
                break
        if posicion != -1:
            separado.pop(posicion)

        text = ' '.join(separado)
        texto = text.split()
        
        # -------------- Verificando cantidad por pagina ----------------
        resultados_por_pagina = 9
        posicion = -1
    
        for i in range(len(texto)):
            if texto[i] == '-c' or texto[i] == '-cantidad':
                try:
                    resultados_por_pagina = int(texto[i+1])
                    posicion = i
                    break
                except:
                    return msg.reply('Despues de -c se espera un numero cantidad. Ejemplo: -c 15')
        if posicion != -1:
            texto.pop(posicion + 1)
            texto.pop(posicion)
        if resultados_por_pagina > 25:
            return msg.reply('La cantidad maxima de opciones por pagina es 25')
        if resultados_por_pagina < 1:
            resultados_por_pagina = 1
        resultados_por_pagina += 1

        # -------------- Verificando Quitar ----------------
        posicion = -1
        quitar = ''
        agregar_a_quitar = False
        for i in range(len(texto)):
            if texto[i].lower() == '-q' or texto[i].lower() == '-quitar':
                posicion = i
                agregar_a_quitar = True
            if agregar_a_quitar and posicion != i:
                quitar += f'{texto[i]} '
        if posicion != -1:
            texto = texto[:posicion]
        
        texto = ' '.join(texto)

        if texto and len(texto) > 0:
            tx = texto.lower().split()
            busquedas = tx
        else:
            return msg.reply('Por favor introduce un elemento de busqueda')
        if busquedas[0] == '*' and msg.author.id not in self.developers_ids:
            return msg.reply('Esta busqueda solo esta disponible para desarrollo')
        link_base = 'https://api.hypixel.net/skyblock/auctions'
        paginas_totales = 1000
        pagina = 0
        resultados = 0
        paginando = True
        elementos = []
        ahora_hora = int(datetime.now().strftime('%H')) * 60
        ahora_minutos = int(datetime.now().strftime('%M'))
        ahora_dia = int(datetime.now().strftime('%d')) * 60 * 24
        ahora = ahora_hora + ahora_minutos + ahora_dia
        fecha_ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.last_ah_update == '':
            self.last_ah_update = int(ahora) + 10
            self.fecha_de_actualizacion = fecha_ahora
        igualar = False

        # ----- Verificando si es necesario hacer una nueva busqueda -----
        if abs(int(self.last_ah_update) - int(ahora)) > 5:
            actualizar_datos_ah = True
        else:
            actualizar_datos_ah = False

        if actualizar_datos_ah:
            for i in range(len(self.auction_items)):
                self.auction_items[i] = ''

        # ----- Obteniendo y filtrando data -----
        while paginando and pagina < paginas_totales:
            try:
                if actualizar_datos_ah:
                    primero = link_base + '?key='
                    segundo = f'&page={pagina}'
                    hydata = self.consulta(primero, segundo)
                    self.last_ah_update = ahora
                    self.auction_items[pagina] = hydata
                    igualar = True
                else:
                    hydata = self.auction_items[pagina]
                metrica = hydata['auctions']

                for elemento in metrica:
                    encontrado = True
                    item_bytes = Item.decode_inventory_data(elemento['item_bytes'])['i'][0]
                    cantidad = item_bytes['Count']
                    if cantidad > 1:
                        item_name = f"{elemento['item_name']} - x{cantidad}"
                    else:
                        item_name = elemento['item_name']

                    # ----------- Filtrando busqueda -----------
                    if busquedas[0] != '*' and not avanzada:
                        for busqueda in busquedas:
                            if busqueda.lower() not in item_name.lower():
                                encontrado = False
                        if encontrado:
                            for quit in quitar.split():
                                if quit.lower() in item_name.lower():
                                    encontrado = False
                    else:
                        encontrado = True
                    if avanzada:
                        item_bytes = Item.decode_inventory_data(elemento['item_bytes'])['i'][0]
                        cantidad = item_bytes['Count']
                        if cantidad > 1:
                            item_name = f"{elemento['item_name']} - x{cantidad}"
                        else:
                            item_name = elemento['item_name']
                        item_name = self.remplazar(item_name)
                        lore = self.remplazar(elemento['item_lore'])
                        extra_datos = item_bytes['tag']["ExtraAttributes"]
                        try: 
                            if extra_datos['rarity_upgrades'] == 1:
                                lore += f'Item Recombulado\n'
                                item_name += ' ' + self.recomb_item()
                        except:
                            pass
                        try:
                            lore += f'Hot potato books: {extra_datos["hot_potato_count"]}\n'
                        except:
                            pass
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
                        for busqueda in busquedas:
                            if (busqueda.lower() not in item_name.lower() and busqueda.lower() not in lore.lower()):
                                encontrado = False
                        if encontrado:
                            for quit in quitar.split():
                                if quit.lower() in item_name.lower() or quit.lower() in lore.lower():
                                    encontrado = False
                    if solo_bin:
                        try:
                            if elemento['bin']:
                                pass
                        except:
                            encontrado = False
                    if solo_auction:
                        try:
                            if elemento['bin']:
                                encontrado = False
                        except:
                            pass
                    
                    # ----------- Decodificando encontrado -----------
                    if encontrado:
                        item_bytes = Item.decode_inventory_data(elemento['item_bytes'])['i'][0]
                        if item_name in self.emojis_saved:
                            item_name = self.emojis_saved[item_name]
                        else:
                            em = self.get_emoji_name(item_name)
                            if em != '':
                                self.emojis_saved[item_name] = em
                                item_name = em

                        enbin = 'Auction'
                        try:
                            if elemento['bin']:
                                enbin = f'Bin'
                                precio_actual = elemento['starting_bid']
                        except:
                            enbin = f'Auction'
                            if float(elemento['highest_bid_amount']) != 0:
                                precio_actual = elemento['highest_bid_amount']
                            else:
                                precio_actual = elemento['starting_bid']

                        lore = self.remplazar(elemento['item_lore'])
                        extra_datos = item_bytes['tag']["ExtraAttributes"]
                        # Recomb
                        try: 
                            if extra_datos['rarity_upgrades'] == 1:
                                lore += f'Item Recombulado\n'
                                item_name += ' ' + self.recomb_item()
                        except:
                            pass
                        # Potatps books
                        try:
                            lore += f'Hot potato books: {extra_datos["hot_potato_count"]}\n'
                        except:
                            pass
                        # Gemas
                        try:
                            gemas = extra_datos["gems"]
                            lore += f'Gema Aplicada: {gemas["UNIVERSAL_0"]} {gemas["UNIVERSAL_0_gem"]}\n'
                        except:
                            pass
                        fin_temp = elemento['end']
                        termino = self.obtener_tiempo_relativo(fin_temp)
                        tier = elemento['tier']
                        tier_emoji = self.auction_emoji(f'{tier}-in')
                        item_name = f'{item_name} {tier_emoji}'
                        elemeto_actual = {
                            "item": item_name,
                            "modo": enbin,
                            "vendedor": elemento['auctioneer'],
                            "lore": lore,
                            "rareza": tier,
                            "tier_emoji": tier_emoji,
                            "claimed": elemento['claimed'],
                            "precio": float(precio_actual),
                            "termina": termino,
                            "categoria": elemento['category'],
                            "pagina": pagina + 1,
                            "resultado": resultados
                        }
                        elementos.append(elemeto_actual)
                        resultados += 1
                pagina += 1
            except:
                paginando = False
        if igualar:
            self.fecha_de_actualizacion = fecha_ahora

        df = pd.DataFrame(elementos)

        try:
            m_df = df.sort_values(by=['precio'])
        except:
            return msg.reply('No se encontraron resultados')
        cambios = {}
        for precio in m_df['precio']:
            cambios[precio] = '{:,.0f}'.format(float(precio))
        m_df['precio'] = m_df['precio'].map(cambios)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)

        #print(m_df)

        mensajes = []
        venta_emojis = {"Bin": self.auction_emoji("bin_only"), "Auction": self.auction_emoji("auction_only")}
        precio_emojis = {"Bin": self.auction_emoji("submit_bid"), "Auction": self.auction_emoji("starting_bid_or_item_price")}

        opciones_por_pagina = 0
        aux = 1
        pagina_actual = 1
        if detallado and item_detallado > len(m_df.index):
            bus = " ".join(busquedas)
            return msg.reply(f'Solo se encontraron {len(m_df.index)} resultados para esta busqueda')
        paginas_disponibles = (len(m_df.index) // (resultados_por_pagina - 1)) + 1
        if mostrar_res > paginas_disponibles:
            return msg.reply(f'Solo se encontraron {paginas_disponibles} paginas de resultados')
        color = self.color_aleatorio()
        texto = " ".join(busquedas)
        serch_emoji = self.auction_emoji('search')
        title = f'{serch_emoji} Resultados a "{texto}" '
        if solo_bin:
            bin_emoji = self.auction_emoji("bin_only")
            title += f'{bin_emoji}'
        elif solo_auction:
            auction_emoji = self.auction_emoji("auction_only")
            title += f'{auction_emoji}'
        else:
            all_emoji = self.auction_emoji("show_all")
            title += f'{all_emoji}'

        embed = discord.Embed(title=title, description = f'Pagina {mostrar_res} / {paginas_disponibles}', color = color)
        for i in m_df.index:
            cantidad_baja = self.redondear_letras(m_df["precio"][i])
            if detallado:
                if aux == item_detallado:
                    print('entro a detallado')
                    link_base_player = 'https://api.hypixel.net/player'
                    primero = f'{link_base_player}?key='
                    segundo = f'&uuid={m_df["vendedor"][i]}'
                    player = self.consulta(primero, segundo)
                    player_name = player["player"]["displayname"]
                    color = self.color_aleatorio()
                    embed = discord.Embed(title=f'{aux}.- {m_df["item"][i]}', description = f'```{m_df["lore"][i]}```', color = color)
                    nombre = f'Vendedor: {player_name}'
                    value = '```'
                    value += f'Rareza: {m_df["rareza"][i]}\n'
                    value += f'Modo: {m_df["modo"][i]}\n'
                    value += f'Precio: {m_df["precio"][i]} ({cantidad_baja})\n'
                    value += f'Termina en: {m_df["termina"][i]}\n'
                    value += '```'
                    embed.add_field(name=f'{nombre}', value=value)
                    footer = f'Ultima actualizacion: {self.fecha_de_actualizacion}'
                    embed.set_footer(text = footer)
                    return msg.reply(embed = embed)
            else:
                if aux % resultados_por_pagina == 0:
                    pagina_actual += 1
                nombre = f'{aux}/{resultados}.- {m_df["item"][i]}'
                value = ''
                value += f'`Rareza: {m_df["rareza"][i]}` {m_df["tier_emoji"][i]}\n'
                value += f'`Modo: {m_df["modo"][i]}` \n'
                value += f'`Precio: {m_df["precio"][i]} ({cantidad_baja})` {precio_emojis[m_df["modo"][i]]}\n'
                value += f'`Termina en: {m_df["termina"][i]}` {self.auction_emoji("auction_stats")}\n'
                value += ''
                embed.add_field(name=f'{nombre}', value=value)
                opciones_por_pagina += 1
                if opciones_por_pagina == resultados_por_pagina - 1:
                    footer = f'Resultados Totales para la busqueda: {resultados}\n'
                    footer += f'Ultima actualizacion: {self.fecha_de_actualizacion}\n'
                    footer += f'Pagina {mostrar_res} de {paginas_disponibles}'
                    embed.set_footer(text = footer)
                    mensajes.append(embed)
                    mostrar_res += 1
                    embed = discord.Embed(title=f'Resultados a "{texto}" ', description = f'Pagina {mostrar_res} / {paginas_disponibles}', color = color)
                    opciones_por_pagina = 0
            aux += 1
        if opciones_por_pagina > 0:
            footer = f'Resultados Totales para la busqueda: {resultados}\n'
            footer += f'Ultima actualizacion: {self.fecha_de_actualizacion}\n'
            footer += f'Pagina {mostrar_res} de {paginas_disponibles}'
            embed.set_footer(text = footer)
            mensajes.append(embed)
        mensajes.append(embed)
        return mensajes

    def invitar(self, msg, text):
        link = 'https://discord.com/api/oauth2/authorize?client_id=876992671284076546&permissions=8&scope=bot'
        yt = 'https://www.youtube.com/channel/UCt8_k3luF9gAek76rgjv4CA'
        dc = 'https://discord.gg/GvpR7tdmfW'
        color = self.color_aleatorio()
        #embed = discord.Embed(title=f'GDGABOT Invite Link', description=f'Gracias por invitar. Te Invitamos a seguirnos tambien en: ', color = 0x00ff00, url=link)
        embed = discord.Embed(title=f'GDGABO 97', description=f'Sigue y unete a: ', color = color)

        ''' title = f'Invite GDGABOT'
        description = f'[Bot]({link})'
        embed.add_field(name=title, value=description, inline = False) '''

        title = f'YouTube GDGABO97'
        description = f'[YouTube]({yt})'
        embed.add_field(name=title, value=description, inline = False)

        title = f"GDGABO97's Server"
        description = f'[Discord]({dc})'
        embed.add_field(name=title, value=description, inline = False)
        return msg.channel.send(embed = embed)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'hola': self.hola,
            'clean': self.limpiar,
            'c': self.limpiar,
            'clear': self.limpiar,
            'limpiar': self.limpiar,
            'ah': self.auction,
            'a': self.auction,
            'auction': self.auction,
            'auctions': self.auction,
            'invite': self.invitar,
            'invitar': self.invitar,
            'op': self.operacion,
            'operacion': self.operacion,
            'cal': self.operacion,
            'calc': self.operacion,
            'calcular': self.operacion,
        }
