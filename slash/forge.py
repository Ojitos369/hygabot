import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from slash.generales import Generales
class Forge(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    def remplazar_forja_name(self, nombre):
        lista = {
            "divan_helmet": "helmet_of_divan",
            "divan_chestplate": "chestplate_of_divan",
            "divan_leggings": "leggings_of_divan",
            "divan_boots": "boots_of_divan",
            "gemstone": "gem",
            "gem": "gemstone",
            "divan_drill": "divans_drill"
        }
        for key_o, value_o in lista.items():
            key = key_o.replace("_", " ")
            value = value_o.replace("_", " ")
            nombre = nombre.replace(key, value)
        return nombre
    
    @cog_ext.cog_slash(name="Forja", description="Muestra los items de la forja", options = [
        create_option(
            name = 'username',
            description = 'Username',
            option_type = 3,
            required=False,
        ),
        create_option(
            name = 'perfil',
            description = 'Nombre del prefil',
            option_type = 3,
            required=False,
        )
    ])
    async def hotm(self, msg: SlashContext, username: str = '', perfil: str = ''):
        self.config()
        uuid = ''
        if username == '':
            id = msg.author.id
            uuid = self.get_verify_user(id)
            username = self.get_username(uuid = uuid)
        if username == '':
            await msg.reply(f'Debes verificar antes la cuenta para poder usar el comando sin especificar username. Utiliza /verificar')
            return
        
        perfil_name = perfil

        msg_original = msg
        msg = await msg.reply("**Obteniendo información...**")
        dropeos_hall = self.dropeo_hall(msg_original)

        # -------------- Obtencion de datos ----------------
        try:
            if uuid != '':
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True, uuid_key=uuid)
            else:
                datos, perfil_name, uuid, username = self.obtener_perfil(username, perfil_name, uuid = True)
        except:
            datos = self.obtener_perfil(username, perfil_name, uuid = True)
        # save datos as json
        #open(f'./info_pruebas/{username}_{perfil_name}.json', 'w').write(json.dumps(datos, indent=4))
        if datos == 'usuario':
            await msg.edit(content = 'Verifica que el Usuario este bien escrito')
            return
        if datos == 'perfil':
            await msg.edit(content = f'{username} no tiene perfil de nombre {perfil_name}')
            return
        username = self.for_tsuru(username)

        # -------------- Obtencion de datos ----------------
        # open json data
        with open('./json/forja_data.json') as data:
            forja_time_data = json.load(data)
        datos_resultado = {}
        try:
            forge_data = datos['forge']['forge_processes']['forge_1']
        except:
            forge_data = {}
        procesos = 0
        try:
            forge_boost = datos['mining_core']['nodes']['forge_time']
        except:
            forge_boost = 0

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
                
                # ----------------- Checando Forge Boost -----------------
                if forge_boost == 20:
                    minutos_en_forja -= minutos_en_forja * 0.3
                elif forge_boost > 10:
                    minutos_en_forja -= minutos_en_forja * 0.195
                elif forge_boost > 1:
                    minutos_en_forja -= minutos_en_forja * 0.15
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
                    tiempo_transucrrido += f'{int(dias)} días, '
                if not (horas == 0 and dias == 0):
                    tiempo_transucrrido += f'{int(horas)}h, '
                if not (minutos == 0 and horas == 0 and dias == 0):
                    tiempo_transucrrido += f'{int(minutos)}m, '
                tiempo_transucrrido += f'{int(segundos)}s'
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
        if dropeos_hall[0]:
                footer = dropeos_hall[1]
                embed.set_footer(text=footer)
        await msg.edit(content = '', embed=embed)
        return

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Forge(bot))
