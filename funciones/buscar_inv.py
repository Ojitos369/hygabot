import json
import discord
from datetime import datetime

from requests import api
from funciones.generales import Generales
from funciones.inventarios import Inventarios
from funciones.ender_chest import Ender
from funciones.backpack import Backpack
from funciones.wardrobe import Wardrobe
class Busqueda(Generales):
    datos_actualizacion = {}
    full_inventarios = {}
    def busqueda(self, msg = '', text = '', intrno = False):
        return msg.reply(f'Comando en reparacion')
        self.config()
        separado = text.split()
        perfil_name = ''
        posicion = -1
        numero_item = 0
        filtro = ''
        filtrando = False
        detallado = False
        avanzada = False
        inv = Inventarios()
        end = Ender()
        bp = Backpack()
        wd = Wardrobe()

        # -------------- Verificando Detallado ----------------
        for i in range(len(separado)):
            if separado[i] == '-d' or  separado[i] == '-detalles' or  separado[i] == '-detallado':
                try:
                    numero_item = int(separado[i+1])
                    posicion = i
                    detallado = True
                    break
                except:
                    return msg.reply('Despues de -d se espera un numero de la lista. Ejemplo: -d 1')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)

        # verificando Perfil y usuaario
        username = separado.pop(0)
        if not interno:
            try:
                username = self.get_username(username)
            except:
                return msg.reply('Revise que el usuario este bien escrito')
            
        try:
            if separado[1] == '-f' or separado[1] == '-filtro' or separado[1] == '-filtrar':
                perfil_name = f' {separado.pop(0)}'
        except:
            return msg.reply('Se debe ingresar un filtro de busqueda. Ejemplo: -f sword')

        # -------------- Verificando Filtro ----------------
        try:
            for i in range(len(separado)):
                if separado[i] == '-f' or separado[i] == '-filtro' or separado[i] == '-filtrar':
                    separado.pop(i)
                    filtrando = True
                    break
        except:
            return msg.reply('Se debe ingresar un filtro de busqueda. Ejemplo: -f sword')

        # -------------- Verificando Busqueda Avanzada ----------------
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-ba' or separado[i] == '-avanzada' or separado[i] == '-a' or separado[i] == '-avanzado':
                posicion = i
                avanzada = True
                break
        if posicion != -1:
            separado.pop(posicion)
        
        if not filtrando:
            return msg.reply('Debe ingresar un filtro de busqueda valido despues de -f. Ejemplo: -f spirit')
        
        if not interno:
            try:
                username = self.get_username(username)
            except:
                return msg.reply('Revise que el usuario este bien escrito')
        
        datos, perfil_name, uuid= self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        #open(f'./{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            if interno:
                return 'usuario'
            return msg.reply('Verifica que el Usuario este bien escrito')
        if datos == 'perfil':
            if interno:
                return 'perfil'
            return msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')
        
        busqueda = f'{username}{perfil_name} -solicitud_interna'

        # -------------- Verificando Quitar ----------------
        posicion = -1
        quitar = []
        agregar_a_quitar = False
        for i in range(len(separado)):
            if separado[i].lower() == '-q' or separado[i].lower() == '-quitar':
                posicion = i
                agregar_a_quitar = True
            if agregar_a_quitar and posicion != i:
                quitar.append(separado[i])
        if posicion != -1:
            separado = separado[:posicion]
        
        filtro = ' '.join(separado)
        if len(filtro) < 2:
            return msg.reply('Intenta con una busqueda mas extensa')


        if username in self.datos_actualizacion:
            ahora = int(datetime.now().strftime('%M'))
            if abs(self.datos_actualizacion[f'{username}_{perfil_name}'.lower()]['hora'] - ahora) > 5:
                items_totales = []
                # -------------- Verificando api de inventario ----------------
                inv_data = inv.inventario(msg = msg, text = busqueda, datos = datos)
                if inv_data == 'verApi' and not interno:
                    return msg.reply(f'Revise que la API de inventario este activa')
                if inv_data == 'verApi' and interno:
                    return False, None
                if inv_data == 'usuario':
                        return msg.reply('Verifica que el Usuario este bien escrito')
                if inv_data == 'perfil' and not interno:
                    return msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')
                # -------------- Obteniendo inventario ----------------
                items_totales.append(inv_data)
                # -------------- Obteniendo Ender Chest ----------------
                items_totales.append(end.ender_chest(msg = msg, text = busqueda, datos = datos))
                # -------------- Obteniendo Wardrobe ----------------
                items_totales.append(wd.wardrobe(msg = msg, text = busqueda, datos = datos))
                # -------------- Obteniendo Backpack ----------------
                for i in range(20):
                    busqueda_temporal = busqueda + f' -n {i}'
                    resultado = bp.backpack(msg = msg, text = busqueda_temporal, datos = datos)
                    if not resultado:
                        pass
                    else:
                        items_totales.append(resultado)
                # -------------- save resultados as json file ----------------
                guardar = {'info': items_totales}
                self.full_inventarios[f'{username}_{perfil_name}'.lower()] = guardar
            else:
                # -------------- load resultados from json file ----------------
                items_totales = self.full_inventarios[f'{username}_{perfil_name}'.lower()]['info']
        else:
            ahora = int(datetime.now().strftime('%M'))
            self.datos_actualizacion[f'{username}_{perfil_name}'.lower()] = {'hora': ahora}
            items_totales = []
            # -------------- Verificando api de inventario ----------------
            inv_data = inv.inventario(msg = msg, text = busqueda, datos = datos)
            if inv_data == 'verApi' and not interno:
                return msg.reply(f'Revise que la API de inventario este activa')
            if inv_data == 'verApi' and interno:
                return False, None
            if inv_data == 'usuario':
                    return msg.reply('Verifica que el Usuario este bien escrito')
            if inv_data == 'perfil' and not interno:
                return msg.reply(f'{username} no tiene perfil de nombre {perfil_name}')
            # -------------- Obteniendo inventario ----------------
            items_totales.append(inv_data)
            # -------------- Obteniendo Ender Chest ----------------
            items_totales.append(end.ender_chest(msg = msg, text = busqueda, datos = datos))
            # -------------- Obteniendo Wardrobe ----------------
            items_totales.append(wd.wardrobe(msg = msg, text = busqueda, datos = datos))
            # -------------- Obteniendo Backpack ----------------
            for i in range(20):
                busqueda_temporal = busqueda + f' -n {i}'
                resultado = bp.backpack(msg = msg, text = busqueda_temporal, datos = datos)
                if not resultado:
                    pass
                else:
                    items_totales.append(resultado)
            # -------------- save resultados as json file ----------------
            guardar = {'info': items_totales}
            self.full_inventarios[f'{username}_{perfil_name}'.lower()] = guardar
        numero_de_resultados = 0
        for almacenamiento in items_totales:
            numero_de_resultados += len(almacenamiento)
        
        # -------------- Filtrando Busqueda ----------------
        username = self.for_tsuru(username)
        lista_de_items = []
        encontrados = 0
        if filtrando:
            filtro = filtro.lower().split()
            i = 0
            for almacenamiento in items_totales:
                lista_de_items.append([])
                for item in almacenamiento:
                    encontrado = True
                    if avanzada:
                        for busqueda in filtro:
                            if busqueda.lower() not in item['nombre'].lower() and busqueda.lower() not in item['lore'].lower():
                                encontrado = False
                        if encontrado:
                            for quit in quitar:
                                if quit.lower() in item['nombre'].lower() or quit.lower() in item['lore'].lower():
                                    encontrado = False
                    else:
                        for busqueda in filtro:
                            if busqueda not in item['nombre'].lower():
                                encontrado = False
                        if encontrado:
                            for quit in quitar:
                                if quit.lower() in item['nombre'].lower():
                                    print(f'Se Quito {item["nombre"]}')
                                    encontrado = False
                    if encontrado:
                        encontrados += 1
                        lista_de_items[i].append(item)
                i += 1
            if encontrados == 0 and not interno:
                return msg.reply(f'No se encontraron resultados entre los items de {username} en {perfil_name}')
        else:
            lista_de_items = items_totales
        
        if interno:
            if encontrados == 0:
                print(f'No se encontraron resultados entre los items de {username} en {perfil_name}')
                return False, None
            else:
                print(f'Se encontraron {encontrados} resultados entre los items de {username} en {perfil_name}')
                return True, f'Se encontraron {encontrados} resultados entre los items de {username} en {perfil_name}'

        if detallado:
            if numero_item not in range(1, numero_de_resultados + 1):
                return msg.reply('Este numero no esta en la lista. Intenta con un numero valido')
            else:
                i_almacenamiento = 1
                datos_item = []
                en_item = 1
                for almacenamiento in lista_de_items:
                    if numero_item in range(en_item, en_item + len(almacenamiento)):
                        for item in almacenamiento:
                            if numero_item == en_item:
                                datos_item.append([i_almacenamiento, item])
                            en_item += 1
                    else:
                        en_item += len(almacenamiento)
                    i_almacenamiento += 1
                if datos_item:
                    for dato_item in datos_item:
                        id_almacenamiento, datos = int(dato_item[0]) + 1, dato_item[1]
                        if id_almacenamiento == 1:
                            almacenamiento = 'Inventario'
                        elif id_almacenamiento == 2:
                            almacenamiento = 'Ender Chest'
                        elif id_almacenamiento == 3:
                            almacenamiento = 'Wardrobe'
                        else:
                            almacenamiento = f'Backpack {id_almacenamiento - 4}'
                        color = self.color_aleatorio()
                        if id_almacenamiento == 1:
                            embed = discord.Embed(title=f'Resultado en: {almacenamiento}. Pagina {datos["pagina"]}', color=color)
                        else:
                            embed = discord.Embed(title=f'Resultado en: {almacenamiento}', color=color)                        
                        embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
                        name = datos['nombre']
                        value = '```'
                        value += datos['lore']
                        value += f'Tipo: {datos["extra"]}'
                        value += '```'
                        embed.add_field(name = name, value = value, inline = False)
                    return msg.reply(embed = embed)
        else:
            id_almacenamiento = 0
            en_item = 1
            mensajes = []
            color = self.color_aleatorio()
            for almacenamiento in lista_de_items:
                resultados = ''
                if id_almacenamiento == 0:
                    name = 'Inventario:'
                elif id_almacenamiento == 1:
                    name = 'Ender Chest'
                elif id_almacenamiento == 2:
                    name = 'Wardrobe'
                else:
                    name = f'BackPack {id_almacenamiento - 2}:'
                if len(almacenamiento) != 0:
                    embed = discord.Embed(title=f'Resultados en {name} de {username} en {perfil_name} ', color=color)
                    embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}?size=40')
                if id_almacenamiento == 1:
                    name = 'Ender Chest Pagina 1'
                for item in almacenamiento:
                    if id_almacenamiento == 1:
                        if item["pagina"] > int(name.split()[-1]):
                            resultados += f'{en_item}.- {item["nombre"]}\n'
                            embed.add_field(name = name, value = resultados, inline = False)
                            name = f'Ender Chest Pagina {item["pagina"]}'
                            resultados = ''
                        else:
                            resultados += f'{en_item}.- {item["nombre"]}\n'
                    else:
                        resultados += f'{en_item}.- {item["nombre"]}\n'
                    en_item += 1
                if len(almacenamiento) != 0:
                    if resultados != '':
                        embed.add_field(name = name, value = resultados, inline = False)
                        mensajes.append(embed)
                id_almacenamiento += 1
            return mensajes

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'buscar': self.busqueda,
            'busqueda': self.busqueda,
            'b': self.busqueda,
        }