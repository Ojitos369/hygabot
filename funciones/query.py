import json
import discord
from datetime import datetime

from discord.embeds import Embed
from slash.generales import Generales
class Query(Generales):

    def query(self, msg = '', text = ''):
        if msg.author.id not in self.developers_ids:
            return
            #return msg.reply(f'Comando solo para uso de desarrollador')
        consulta = False
        ejecutar = False
        database = ''
        if '-c' in text or '-consulta' in text:
            text = text.replace(' -consulta', '').replace(' -c', '')
            consulta = True
        if '-e' in text or '-ejecutar' in text:
            text = text.replace(' -ejecutar', '').replace(' -e', '')
            ejecutar = True
        if not (consulta or ejecutar):
            return msg.reply(f'Especificar el tipo de query (consulta/ejecutar)')
        
        # -- verificar database
        separado = text.split(' ')
        posicion = -1
        i = 0
        for i in range(len(separado)):
            if separado[i] == '-db':
                try:
                    database = separado[i+1]
                    posicion = i
                except:
                    return msg.reply(f'Especificar el nombre de la base de datos')
                break
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)
        text = ' '.join(separado)
        if ejecutar:
            try:
                self.query_ejecutar(text)
                return msg.reply(f'Query ejecutado correctamente')
            except Exception as e:
                return msg.reply(f'Error: {e}')
        if consulta:
            try:
                resultados_con = self.query_consulta(text)
                if len(resultados_con) == 0:
                    return msg.reply(f'No hay resultados')
                salida = ''
                largo = 0
                resultados = []
                color = self.color_aleatorio()
                title = f'{text}'
                for resultado in resultados_con:
                    temp = str(resultado)
                    temp = temp[1:-1]
                    if temp[-1] == ',':
                        temp = temp[:-1]
                    salida += f'{temp}\n'
                    largo += len(temp)
                    if largo > 900:
                        embed = Embed(title=title, description=salida, color=color)
                        resultados.append(embed)
                        salida = ''
                        largo = 0
                if largo > 0:
                    embed = Embed(title=title, description=salida, color=color)
                    resultados.append(embed)
                
                for i in range(len(resultados)):
                    text = f'pagina {i + 1} de {len(resultados)}'
                    resultados[i].set_footer(text=text)
                return resultados
            except Exception as e:
                return msg.reply(f'Error: {e}')

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'query': self.query,
            'qry': self.query,
            'qr': self.query
        }