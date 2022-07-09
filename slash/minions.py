import discord
import json
from minions.minions import crear_minions
from datetime import datetime
from discord import embeds
from funciones.generales import Generales
from funciones.bazar import Bazar
class Minions(Generales):
    bazar = Bazar()

    def verificar_mayor(self, minion, maximos, bazar, horas, fuel):
        for i in range(len(maximos)):
            if minion.datos(horas, fuel, bazar)['ganancias'] > maximos[i].datos(horas, fuel, bazar)['ganancias']:
                actual = maximos[i]
                maximos[i] = minion
                maximos = self.verificar_mayor(actual, maximos, bazar, horas, fuel)
                break
            else:
                if i == len(maximos) - 1 and len(maximos) < 5:
                    maximos.append(minion)
        return maximos

    def best_minion(self, msg = '', text = ''):
        lvl = 11
        slayers = True
        separado = text.split(' ')
        horas = 24
        fuel = 0
        posicion = -1
        # ----- Revisar Opcion de slayers -----
        for i in range(len(separado)):
            if separado[i].lower() == '-ss' or separado[i].lower() == '-sinslayer' or separado[i].lower() == '-sinslayers':
                slayers = False
                separado.pop(i)
                break

        # ----- Revisar Opcion de horas -----
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-t' or separado[i] == '-time':
                try:
                    horas = int(separado[i + 1])
                    posicion = i
                    break
                except:
                    return msg.reply('La opcion -t requiere un numero de horas despues. Ejemplo: -t 24')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        if horas < 1:
            horas =  1

        # ----- Revisar Opcion de fuel -----
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-m' or separado[i] == '-mejora':
                try:
                    fuel = int(separado[i + 1])
                    posicion = i
                    break
                except:
                    return msg.reply('La opcion -m requiere el porcentaje de mejora. Ejemplo: -f 25')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        else:
            fuel = 0
        fuel = fuel / 100
        if fuel < 0:
            fuel = 0

        # ----- Revisar Opcion de lvl -----
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-l' or separado[i] == '-level' or separado[i] == '-lvl':
                try:
                    lvl = int(separado[i + 1])
                    posicion = i
                    break
                except:
                    return msg.reply('La opcion -l requiere un nivel despues. Ejemplo: -l 11')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        if lvl > 12:
            return msg.reply(f"No hay minions de nivel {lvl}")
        if lvl < 1:
            lvl = 1
        lvl -= 1
        text = ' '.join(separado)
        maximos = []
        minions = crear_minions(slayers)
        bazar = self.bazar.bazar(text = 'consulta para minions', for_minions = True)
        for minion in minions:
            if lvl < len(minion):
                esclavo = minion[lvl]
                datos = esclavo.datos(horas, fuel, bazar)
                if len(maximos) < 1:
                    maximos.append(esclavo)
                else:
                    maximos = self.verificar_mayor(esclavo, maximos, bazar, horas, fuel)
        color = self.color_aleatorio()
        embed = discord.Embed(title = f'Mejores minions nivel {lvl + 1} en {horas} horas', color = color)

        ele = 1
        for minion in maximos:
            datos = minion.detalles(horas, fuel, bazar)
            name = self.extra_replace(f"{ele}.- {datos['name']}")
            value = self.extra_replace(datos['value'])
            embed.add_field(name = name, value = value, inline = False)
            ele += 1
        return msg.reply(embed = embed)

    def minion(self, msg = '', text = ''):
        if text == '':
            return msg.reply('No se ha especificado un minion')

        separado = text.split(' ')
        horas = 24
        fuel = 0

        # ----- Revisar Opcion de horas -----
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-t' or separado[i] == '-time':
                try:
                    horas = int(separado[i + 1])
                    posicion = i
                    break
                except:
                    return msg.reply('La opcion -t requiere un numero de horas despues. Ejemplo: -t 24')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        if horas < 1:
            horas =  1

        # ----- Revisar Opcion de fuel -----
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-m' or separado[i] == '-mejora':
                try:
                    fuel = int(separado[i + 1])
                    posicion = i
                    break
                except:
                    return msg.reply('La opcion -m requiere el porcentaje de mejora. Ejemplo: -f 25')
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        else:
            fuel = 0
        fuel = fuel / 100
        if fuel < 0:
            fuel = 0


        text = ' '.join(separado)
        minions = crear_minions()
        bazar = self.bazar.bazar(text = 'consulta para minions', for_minions = True)
        mensaje = []
        encontrados = 0
        for minion in minions:
            dato = minion[0].datos(horas, fuel, bazar)
            if text.lower() in dato['name'].lower():
                encontrados += 1
        if encontrados == 0:
            return msg.reply(f'No se encontraron resultados')

        en_minion = 0
        for minion in minions:
            dato = minion[0].datos(horas, fuel, bazar)
            #print(f'En minion: {dato["name"]}')
            #print(f'Con texto: {text}')
            if text.lower() in dato['name'].lower():
                en_minion += 1
                color = self.color_aleatorio()
                embed = discord.Embed(title = f'{en_minion}/{encontrados}.- {dato["name"]} Minions', color = color)
                for level in minion:
                    dato = level.datos(horas, fuel, bazar)
                    detalles = level.detalles(horas, fuel, bazar)
                    #name = f'{dato["name"]} Minion - Level : {dato["nivel"]}'
                    name = f"{self.extra_replace(detalles['name'])}"
                    value = self.extra_replace(detalles['value'])
                    embed.add_field(name = name, value = value, inline = False)
                mensaje.append(msg.reply(embed = embed))
        return mensaje

    def config(self, datos = False, n = 0):
        self.funciones = {
            'best': self.best_minion,
            'bm': self.best_minion,
            'best_minion': self.best_minion,
            'best_minions': self.best_minion,
            'minion': self.minion,
            'minions': self.minion,
            'm': self.minion,
        }
