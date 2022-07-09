import json
import discord
from datetime import datetime
from funciones.generales import Generales
class Bu_guild(Generales):

    def bu_guild(self, msg = '', text = ''):
        self.config()
        from funciones.buscar_inv import Busqueda
        busqueda_item = Busqueda()
        separado = text.split(' ')
        filtro = False
        busqueda = ''
        resultados_mostrar = 1

        # ---- Verificar cantidad ----
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-c':
                posicion = i
                try:
                    resultados_mostrar = int(separado[i + 1])
                except:
                    return msg.reply('Falta especificar numero')
                    
        if posicion != -1:
            separado.pop(posicion + 1)
            separado.pop(posicion)

        # ---- Verificar Filtro ----
        posicion = -1
        for i in range(len(separado)):
            if separado[i] == '-f':
                filtro = True
                posicion = i
            if filtro and i > posicion:
                busqueda += separado[i] + ' '

        if posicion != -1:
            separado.pop(posicion)
            separado = separado[:posicion]
        
        if not filtro:
            return msg.reply('No se ha especificado un filtro')

        guild = ' '.join(separado)

        link_base_player = 'https://api.hypixel.net/player'
        link_base = 'https://api.hypixel.net/guild'
        inicio = f'{link_base}?key='
        fin = f'&name={guild}'
        hydata = self.consulta(inicio, fin)
        metrica = hydata['guild']
        users = []
        numero = 1
        encontrados = 0
        for miembro in metrica['members']:
            uuid = miembro["uuid"]
            primero = f'{link_base_player}?key='
            segundo = f'&uuid={uuid}'
            player = self.consulta(primero, segundo)
            username = player["player"]["displayname"].lower()
            print()
            print(f'{numero}.- Revisando en: {username}')
            query = f'{username} -f {busqueda}'
            try:
                encontrado, texto = busqueda_item.busqueda(msg, query, True)
            except:
                encontrado = False
            numero += 1

            if encontrado:
                users.append([username, texto])
                encontrados += 1
                if encontrados == resultados_mostrar:
                    break
        
        color = self.color_aleatorio()
        embed = discord.Embed(title=f'Guild: {guild}', description=f'{busqueda}', color=color)
        for user in users:
            embed.add_field(name=f'{user[0]}', value=f'{user[1]}', inline=False)
        return msg.reply(embed = embed)


    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

        self.funciones = {
            'bg': self.bu_guild
        }