import json
import discord
from datetime import datetime
from discord.embeds import Embed
from slash.generales import Generales
from verificar import consulta, ejecutar, get_mochila
class Claim(Generales):

    def claim(self, msg = '', text = ''):
        if msg.author.id not in self.event_ids:
            return msg.reply('No tienes permisos para usar este comando.')
        self.config()
        separado = text.replace(',', '').split(' ')
        id = 0
        for palabra in separado:
            if '<@!' in palabra:
                pal = palabra.replace('<@!', '').replace('>', '')
                id = int(pal)
        # for items:
        # calabaza, esqueleto, god_pot, revenant, tarantula, sven, voidgloom
        items = {
            'calabaza': 0,
            'esqueleto': 0,
            'god_pot': 0,
            'revenant': 0,
            'tarantula': 0,
            'sven': 0,
            'voidgloom': 0
        }
        for i in range(len(separado)):
            if separado[i] in items:
                try:
                    items[separado[i]] = int(separado[i+1])
                except:
                    return msg.reply(f'Ingresa una canatidad para {separado[i]}')
        mochila = get_mochila(id, id)
        fallos = ''
        correctos = ''
        dh = self.dropeos_hallowen
        for item in mochila:
            item_name = item[2]
            cantidad = item[3]
            if item_name in items:
                if items[item_name] > 0:
                    if items[item_name] > cantidad:
                        if int(cantidad) > 999:
                            cantidad = self.calculadora(f'{cantidad} + 0')
                        fallos += f'Solo tiene {cantidad} {dh[item_name]["emoji"]}\n'
                    else:
                        correctos += f'Se han reclamado {items[item_name]} {dh[item_name]["emoji"]}\n'
                        cantidad -= items[item_name]
                        query = f"UPDATE mochila SET cantidad = {cantidad} WHERE user_id = '{id}' and item_id = '{item_name}'"
                        ejecutar(query)
        color = self.color_aleatorio()
        embed = discord.Embed(title = 'Reclamos', description = f'{fallos}\n{correctos}', color = color)
        return msg.reply(embed = embed)

    def inv(self, msg = '', text = ''):
        if msg.author.id not in self.event_ids:
            return msg.reply('No tienes permisos para usar este comando.')
        self.config()
        text = msg.content.replace('+event_inv ', '')
        separado = text.replace(',', '').split(' ')
        id = 0
        for palabra in separado:
            if '<@!' in palabra:
                pal = palabra.replace('<@!', '').replace('>', '')
                id = int(pal)
            if '<@' in palabra:
                pal = palabra.replace('<@', '').replace('>', '')
                id = int(pal)
            if len(palabra) == 18:
                id = int(palabra)
        if id == 0:
            for palabra in separado:
                if len(palabra) == 18:
                    try:
                        id = int(palabra)
                    except:
                        pass
        if id == 0:
            return msg.reply('Recuerda hacer tag al user o poner la id')
        mochila = get_mochila(id, id)
        color = self.color_aleatorio()
        title = f'Inventario de hallowen'
        description = f'<@!{id}>:\n'
        valor = '0'
        value_items = ''
        if len(mochila) == 0:
            description += 'Inventario Vacio'
        else:
            for item in mochila:
                nombre = item[2]
                cantidad = item[3]
                item_value = self.dropeos_hallowen[nombre]["valor"]
                if self.dropeos_hallowen[nombre]['valor'] != None:
                    val = f'{item_value} * {cantidad}'
                    res = self.calculadora(val, letras = True)
                    description += f'{self.dropeos_hallowen[nombre]["emoji"]} x{cantidad}\t|\t({res})\n'
                    valor += f'+{val}'
                else:
                    description += f'{self.dropeos_hallowen[nombre]["emoji"]} x{cantidad}\n'
                    value_items += f'{nombre.replace("_", " ").capitalize()}  x{cantidad}\n'
        valor = self.calculadora(valor)
        embed = discord.Embed(title=title, description=description, color=color)
        name = f'Cantidad en coins: '
        value = f'{valor}'
        embed.add_field(name=name, value=value, inline=False)
        if value_items != '':
            name = f'Items: '
            value = f'{value_items}'
            embed.add_field(name=name, value=value, inline=False)
            
        query = f"SELECT  * FROM cambios WHERE user_id = '{id}'"
        peticiones = self.query_consulta(query)
        if len(peticiones) > 0:
            pendiente = ''
            pendiente_cantidad = '0'
            pendiente_items = 0
            entregado = ''
            entregado_cantidad = '0'
            entregado_items = 0
            for pet in peticiones:
                if pet[7] == 'pendiente':
                    if pet[3] == 1:
                        operacion = f'{pendiente_cantidad}  + {pet[4]}'
                        pendiente_cantidad = self.calculadora(operacion, letras = True)
                    elif pet[3] == 2:
                        pendiente_items += pet[4]
                else:
                    if pet[3] == 1:
                        operacion = f'{entregado_cantidad}  + {pet[4]}'
                        entregado_cantidad = self.calculadora(operacion, letras = True)
                    elif pet[3] == 2:
                        entregado_items += pet[4]
            if pendiente_cantidad != '0':
                pendiente = f'Coins: {pendiente_cantidad}\n'
            if pendiente_items != 0:
                pendiente += f'God Potion: {pendiente_items}\n'
            if pendiente != '':
                name = f'Cambios pendientes por entregar:'
                value = f'{pendiente}'
                embed.add_field(name=name, value=value, inline=False)
            if entregado_cantidad != '0':
                entregado = f'Coins: {entregado_cantidad}\n'
            if entregado_items != 0:
                entregado += f'God Potion: {entregado_items}\n'
            if entregado != '':
                name = f'Entregados:'
                value = f'{entregado}'
                embed.add_field(name=name, value=value, inline=False)
        return msg.reply(embed=embed)
    
    def gasto_total(self, msg = '', text = ''):
        if msg.author.id not in self.event_ids:
            return msg.reply('No tienes permisos para usar este comando.')
        self.config()
        query = f"SELECT * FROM mochila ORDER BY item_id"
        items = consulta(query)
        coins = '0'
        items_value = {}
        for item in items:
            nombre = item[2]
            cantidad = item[3]
            valor = self.dropeos_hallowen[nombre]["valor"]
            user_id = item[1]
            if int(user_id) not in self.event_ids:
                print(user_id)
                if valor != None:
                    val = f'{valor} * {cantidad}'
                    res = self.calculadora(val, letras = True)
                    coins += f'+{res}'
                else:
                    if nombre in items_value:
                        items_value[nombre] += cantidad
                    else:
                        items_value[nombre] = cantidad
        items_gasto = ''
        for item, cantidad in items_value.items():
            items_gasto += f'\n{item} x{cantidad}'
        coins = self.calculadora(coins)
        color = self.color_aleatorio()
        title = f'Gasto total de items'
        embed = discord.Embed(title=title, description=items_gasto, color=color)
        name = f'Cantidad en coins: '
        value = f'{coins}'
        embed.add_field(name=name, value=value, inline=False)
        if items_gasto != '':
            name = f'Items: '
            value = f'{items_gasto}'
            embed.add_field(name=name, value=value, inline=False)
        return msg.reply(embed=embed)

    def entregado(self, msg = '', text = ''):
        if msg.author.id not in self.event_ids:
            return msg.reply(f'No tienes permiso para utilizar este comando')

        query = f"SELECT * FROM cambios WHERE id='{text}'"
        print(f'antes de consulta')
        datos = consulta(query)
        print(f'despues de consulta')
        if len(datos) == 0:
            return msg.reply('Sin coincidencias. Revise que el id este bien escrito')
        estado = datos[0][7]
        if estado != 'pendiente':
            return msg.reply('Esta peticion ya fue entregada')
        entrego = msg.author.id
        ahora = datetime.now()
        fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
        query = f"UPDATE cambios SET entrego = '{entrego}', date_entrega = '{fecha}', estado = 'entregado' WHERE id = '{text}'"
        ejecutar(query)
        return msg.reply('Peticion entregada')

    def status(self, msg = '', text = ''):
        if msg.author.id not in self.event_ids:
            return msg.reply(f'No tienes permiso para utilizar este comando')

        query = f"SELECT * FROM cambios WHERE id='{text}'"
        print(f'antes de consulta')
        datos = consulta(query)
        print(f'despues de consulta')
        if len(datos) == 0:
            return msg.reply('Sin coincidencias. Revise que el id este bien escrito')
        datos = datos[0]
        peticion_id = datos[0]
        username = datos[2]
        item_id = datos[3]
        query = f"SELECT * FROM items_cambio WHERE id={item_id}"
        item = consulta(query)[0][1]        
        cantidad = datos[4]
        estado = datos[7]
        entrego = datos[8]
        entregado = False
        if estado != 'pendiente':
            entregado = True
        
        color = self.color_aleatorio()
        if not entregado:
            title = (':warning: Esta peticion esta pendiente')
        else:
            title = (f':white_check_mark: Este cambio fue entregado')
        description = f'Datos de peticion\n'
        if entregado:
            description += f'Entregado por: <@!{entrego}>\n'
        description += f'Id de peticion: {peticion_id}\n'
        description += f'Entregar a: {username}\n'
        description += f'Item: {item}\n'
        if int(cantidad) > 999:
            cantidad = self.calculadora(f'{cantidad} + 0')
        description += f'Cantidad: {cantidad}'

        embed = discord.Embed(title=title, description=description, color=color)
        return msg.reply(embed=embed)

    def pendientes(self, msg = '', text = ''):
        if msg.author.id not in self.event_ids:
            return msg.reply(f'No tienes permiso para utilizar este comando')
        query = f"SELECT * FROM cambios WHERE estado = 'pendiente'"
        datos = consulta(query)
        if len(datos) == 0:
            return msg.reply('No hay peticiones pendientes :partying_face: ')
        color = self.color_aleatorio()
        title = f'Peticiones pendientes'
        embed = discord.Embed(title=title, color=color)
        for dato in datos:
            name = f'id peticion: {dato[0]}'
            value = f'utiliza "+hall_status {dato[0]}" para informacion mas detallada'
            embed.add_field(name=name, value=value, inline=False)
        return msg.reply(embed=embed)

    def user(self, msg = '', text = ''):
        if msg.author.id not in self.event_ids:
            return msg.reply(f'No tienes permiso para utilizar este comando')
        separado = text.split(' ')
        id = 0
        for palabra in separado:
            if '<@!' in palabra:
                pal = palabra.replace('<@!', '').replace('>', '')
                id = int(pal)
            if '<@' in palabra:
                pal = palabra.replace('<@', '').replace('>', '')
                id = int(pal)
        if id == 0:
            for palabra in separado:
                if len(palabra) == 18:
                    try:
                        id = int(palabra)
                    except:
                        pass
        if id == 0:
            return msg.reply('Recuerda hacer tag al user o poner la id')
        query = f"SELECT * FROM cambios WHERE user_id='{str(id)}'"
        datos = consulta(query)
        if len(datos) == 0:
            return msg.reply(f'<@!{id}> no ha realizado peticiones de cambio aun')
        color = self.color_aleatorio()
        title = f'Peticiones de cambios realizadas'
        description = f'Peticiones de <@!{id}>'
        embed = discord.Embed(title=title, description=description, color=color)
        name = f'Peticiones totales: {len(datos)}'
        value = ''
        for dato in datos:
            id_peticion = dato[0]
            item_id = dato[3]
            query = f"SELECT * FROM items_cambio WHERE id={item_id}"
            item = consulta(query)[0][1]
            cantidad = dato[4]
            estado = dato[7]
            value += f'\nid de peticion: {id_peticion}\n'
            value += f'Item: {item}\n'
            if int(cantidad) > 999:
                cantidad = self.calculadora(f'{cantidad} + 0')
            value += f'Cantidad: {cantidad}\n'
            if estado == 'pendiente':
                value += f'Estado: ***{estado.upper()}***\n'
            else:
                value += f'Estado: *{estado}*\n'
        embed.add_field(name=name, value=value, inline=False)
        return msg.reply(embed=embed)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'claim': self.claim,
            'event_inv': self.inv,
            'gasto_total': self.gasto_total,
            'hall_e': self.entregado,
            'hall_entregado': self.entregado,
            'hall_entrega': self.entregado,
            'hall_status': self.status,
            'hall_pendientes': self.pendientes,
            'hall_pendiente': self.pendientes,
            'hall_user': self.user,
        }
