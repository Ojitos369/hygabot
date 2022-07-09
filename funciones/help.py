import json
import discord
from discord import embeds
from funciones.basic import Generales
from slash.generales import Generales

class Help(Generales):

    def help(self, msg = '', text = ''):
        if len(text.split()) == 0:
            color = self.color_aleatorio()
            embed = discord.Embed(title=f'Lista de comandos', description=f'parametros entre [] son obligatorios, parametros entre () son opcionales.\nDisfruta :3', color = color)

            #----------- HELP --------------------
            title = f'\n{self.prefijo}help'
            description = f"```Muestra la lista de comandos disponibles: {self.prefijo}h / {self.prefijo}help```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- CLEAR --------------------
            title = f'\n{self.prefijo}clear [nombre de la guild] [dias sin conectarse]'
            description = f"```Lista los miembros que no se han conectado en los dias establecidos: {self.prefijo}h c / {self.prefijo}h clear```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- AH --------------------
            title = f'\n{self.prefijo}ah [item] (opciones)'
            description = f"```Realiza consulta a la auction house: {self.prefijo}h ah / {self.prefijo}h auction```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- Player AH --------------------
            title = f'\n{self.prefijo}pah [usuario] (perfil) (opciones)'
            description = f"```Muestra las auctions del usuario: {self.prefijo}h pah / {self.prefijo}h playerAh```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- BZ --------------------
            title = f'\n{self.prefijo}bz [item] (opciones)'
            description = f"```Realiza consulta al bazar: {self.prefijo}h bz / {self.prefijo}h bazar```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- INV --------------------
            title = f'\n{self.prefijo}inv [usuario] (perfil) (opciones)'
            description = f"```Muestra el Inventario de los usuarios: {self.prefijo}h inv```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- Backpack --------------------
            title = f'\n{self.prefijo}backpack [usuario] (perfil) (opciones)'
            description = f"```Muestra las backpacks de los usuarios: {self.prefijo}h backpack```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- EC --------------------
            title = f'\n{self.prefijo}ec [usuario] (perfil) (opciones)'
            description = f"```Muestra el Inventario de los usuarios: {self.prefijo}h ender_chest / {self.prefijo}h ec```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- WD --------------------
            title = f'\n{self.prefijo}wd [usuario] (perfil) (opciones)'
            description = f"```Muestra las armaduras de los usuarios: {self.prefijo}h wd```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- BUSCAR --------------------
            title = f'\n{self.prefijo}b [usuario] (perfil) [-f busqueda] (opciones)'
            description = f"```Busca en el inventario, las backpacks, el ender chest y las armaduras del usuario items que coincidan con la busqueda: {self.prefijo}h b```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- SLAYER --------------------
            title = f'\n{self.prefijo}slayer [usuario] (perfil) (-s tipo_slayer)'
            description = f"```Muestra datos de la slayer consultada\n"
            description += f"Ejemplo:\n\t{self.prefijo}sy gearl972\n\t{self.prefijo}slayer gearl97 -s rev\n"
            description += f"Alias: '{self.prefijo}sy', '{self.prefijo}slayer, '{self.prefijo}slayers```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- TALISMANES --------------------
            # Alias: talismanes, talis, tal, accesorios, accesorio, ac
            title = f'\n{self.prefijo}tal [usuario] (perfil)'
            description = f"```Muestra los talismanes del usuario:\n"
            description += f"Alias: '{self.prefijo}talismanes', '{self.prefijo}talis', '{self.prefijo}tal', '{self.prefijo}accesorios', '{self.prefijo}accesorio', '{self.prefijo}ac'```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- ESCENCIAS --------------------
            title = f'\n{self.prefijo}es [usuario] (perfil)'
            description = f"```Muestra las escencias del usuario\n"
            description += f"Alias: '{self.prefijo}es', '{self.prefijo}escencia', '{self.prefijo}escencias'```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- HTOM --------------------
            title = f'\n{self.prefijo}htom [usuario] (perfil)'
            description = f"```Muestra datos de hotm```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- Forja --------------------
            title = f'\n{self.prefijo}for [usuario] (perfil)'
            description = '```'
            description += f"Muestra items de la forja\n"
            description += f"Alias: '{self.prefijo}for', '{self.prefijo}forja', '{self.prefijo}forge'```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- Best Minions --------------------
            title = f'\n{self.prefijo}bm (opciones) *Los precios pueden variar'
            description = f"```Muestra los mejores minions en determinado tiempo: {self.prefijo}h bm```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- Minions --------------------
            title = f'\n{self.prefijo}m [nombre] (opciones)  *Los precios pueden variar'
            description = f"```Muestra detalles de un minion por niveles: {self.prefijo}h bm```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- Pets --------------------
            title = f'\n{self.prefijo}pet [usuario] (perfil)'
            description = f"```Muestra los pets del usuario\n"
            description += f"Alias: {self.prefijo}pet, {self.prefijo}pets```"
            embed.add_field(name=title, value=description, inline = False)

            #----------- HOLA --------------------
            title = f'\n{self.prefijo}hola'
            description = '```Se educado y saluda ;)```\n'
            embed.add_field(name=title, value=description, inline = False)

            #----------- INVITE --------------------
            title = f'\n{self.prefijo}invite'
            description = '```Muestra el link de invitación'
            description += '\nAlias: invite, invitar```\n'
            embed.add_field(name=title, value=description, inline = False)

            #----------- Recomendacion --------------------
            title = f'\n{self.prefijo}rec [Mensaje] (opciones)'
            description = '```Envia Recomendaciones o sugerencias al desarrollador. {self.prefijo}h rec'
            description += '\nAlias: rec, sug, sugerencia, sugerencias, sugerir, recomendacion, recomendaciones```\n'
            embed.add_field(name=title, value=description, inline = False)

            #----------- Operacion --------------------
            title = f'\n{self.prefijo}op [Operacion a realizar]'
            description = '```Realiza operaciones. Acepta los simbolos: suma(+), resta(-), division(/), multiplicacion(*). Permite agrupaciones con ()'
            description += '\nAlias: op, operacion, cal, calc, calcular```'
            embed.add_field(name=title, value=description, inline = False)

            #----------- Novedades --------------------
            title = f'\n{self.prefijo}news'
            description = '```Muestra los ultimos cambios en el bot'
            description += '\nAlias: novedades, news, new```'
            embed.add_field(name=title, value=description, inline = False)

            return msg.channel.send(embed = embed)
        else:
            text = f'help_{text}'
            if text in self.funciones:
                return self.funciones[text](msg, text)
            else:
                return msg.channel.send(f'Revise que el comando este bien escrito. Verifique los comandos con {self.prefijo}help')

    def clear(self, msg, text = ''):
        titulo = f'{self.prefijo}clear [Nombre de la Guild] [Dias sin conectarse]'
        description = f'Lista los miembros que no se han conectado en los dias establecidos'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)
        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre de la guild a ser limpiada\n'
        value += f'Requerido: Dias sin conectarse\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = ''
        value += f'{self.prefijo}clear latam op 7 \n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}c", "{self.prefijo}clear", "{self.prefijo}clean", "{self.prefijo}limpiar"'
        embed.add_field(name=name, value=value, inline = False)

        embed.set_footer(text=f'El comando puede llegar a tardar dependiendo del numero de miembros')

        return msg.channel.send(embed = embed)

    def auction(self, msg, text = ''):
        titulo = f'{self.prefijo}ah [item] (opciones)'
        description = f'Realiza consulta a la auction house. Funciona solo con las iniciales en caso de no conocer la escritura correcta'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre del item a buscar\n'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-d / -detallado / -detalles [numero de la lista]: Muestra los detalles del item especificado de la lista obtenida\n'
        value += f'-b / -busqueda [bin / ah, au, auction]: '
        value += f'Filtra en la busqueda solo los elementos de ese tipo de venta:\n'
        value += f'-a / -ba / -avanzada / -avanzado: Realiza una busqueda en los detalles de los items, no solo en el nombre (Usar en casos especificos ya que tarda en regresar una respuesta)\n'
        value += f'-c / -cantidad: Numero de items a mostrar por pagina. Default 9. Maximo 25\n'
        value += f'-q / -quitar: Quita los resultados que incluyan el filtro\n'
        value += ''
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = ''
        value += f'{self.prefijo}ah gia swor\n'
        value += f'{self.prefijo}auction hyperion -d 1\n'
        value += f'{self.prefijo}ah god pot -b bin\n'
        value += f'{self.prefijo}a spirit -b auction -d 10'
        value += f'{self.prefijo}ah ancien reforg -a'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}a", "{self.prefijo}ah", "{self.prefijo}auction", "{self.prefijo}auctions"'
        embed.add_field(name=name, value=value, inline = False)

        footer = f'Los resultados son mostrados del elemento mas barato al mas caro\n'
        footer += f'Cada 5 minutos se actualizan los datos por lo que puede llegar a tardar'
        embed.set_footer(text=footer)

        return msg.channel.send(embed = embed)

    def player_auction(self, msg, text = ''):
        titulo = f'{self.prefijo}pah [usuario] (perfil) (opciones)'
        description = f'Muestra las auctions activas del player'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre del usuario\n'
        value += f'Opcional: Nombre del perfil\n'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-e/-extendido: Muestra los detalles de los items en venta\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = ''
        value += f'{self.prefijo}pah gearl97\n'
        value += f'{self.prefijo}playerAh gearl97\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}pah", "{self.prefijo}playerAh"'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def bazar(self, msg, text = ''):
        titulo = f'{self.prefijo}bz [item] (opciones)'
        description = f'Muestra los item que coincidan con la busqueda\n'
        description += f'Muestra insta sell, insta buy, sell order, buy order y el flip posible en cada caso'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Busqueda a realizar\n'
        value += f'\tFunciona solo con las iniciales en caso de no conocer la escritura correcta'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-c / -cantidad [cantidad de items a evaluar]'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = f'{self.prefijo}bz mutan\n'
        value += f'{self.prefijo}bazar fin gem -c 10'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}bz", "{self.prefijo}bazar"'
        embed.add_field(name=name, value=value, inline = False)

        footer = f'Los datos del bazar son actualizados cada 5 minutos\n'
        embed.set_footer(text=footer)

        return msg.channel.send(embed = embed)

    def inventario(self, msg, text = ''):
        titulo = f'{self.prefijo}inv [Usuario] (perfil) (opciones)'
        description = f'Muestra el inventario de un usuario\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre de Usuario\n'
        value += f'Opcional: Nombre del perfil\n'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-d / -detallado / -detalles [numero de la lista]: Muestra los detalles del item especificado de la lista obtenida\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = f'{self.prefijo}inv gearl97\n'
        value += f'{self.prefijo}inventory gearl97 -d 3'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}i", "{self.prefijo}inv", "{self.prefijo}inventory", "{self.prefijo}inventario"'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def wardrobe(self, msg, text = ''):
        titulo = f'{self.prefijo}wd [Usuario] (perfil) (opciones)'
        description = f'Muestra las armaduras de un usuario\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre de Usuario\n'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-d / -detallado / -detalles [numero de la lista]: Muestra los detalles del item especificado de la lista obtenida\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = f'{self.prefijo}wd gearl97\n'
        value += f'{self.prefijo}wardrobe gearl97 -d 3'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}wd", "{self.prefijo}wardrobe"'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def ender_chest(self, msg, text = ''):
        titulo = f'{self.prefijo}ec [Usuario] (perfil) (opciones)'
        description = f'Muestra el Ender Chest de un usuario\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre de Usuario\n'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-d / -detallado / -detalles [numero de la lista]: Muestra los detalles del item especificado de la lista obtenida\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = f'{self.prefijo}ec gearl97\n'
        value += f'{self.prefijo}ender_chest gearl97 -d 3'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}ec", "{self.prefijo}ender_chest"'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def backpack(self, msg, text = ''):
        titulo = f'{self.prefijo}bp [Usuario] (perfil) (opciones)'
        description = f'Muestra el inventario de un usuario\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre de Usuario\n'
        value += f'Opcional: Perfil\n'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-d / -detallado / -detalles [numero de la lista]: Muestra los detalles del item especificado de la lista obtenida\n'
        value += f'-n / -numero: Especifica el numero de backpack a revisar (Por defecto la 1)\n'	
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = f'{self.prefijo}bp gearl97\n'
        value += f'{self.prefijo}backpack gearl97 5 -d 3'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}bp", "{self.prefijo}backpack"'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def buscar(self, msg, text = ''):
        titulo = f'{self.prefijo}b [Usuario] (perfil) [-f busqueda] (opciones)'
        description = f'Busca en el inventario, las backpacks, el ender chest y las armaduras del usuario items que coincidan con la busqueda\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre de Usuario\n'
        value += f'Requerido: -f/-filtro/-filtrar busqueda a realizar\n'
        value += f'\tFunciona solo con las iniciales en caso de no conocer la escritura correcta'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-d / -detallado / -detalles [numero de la lista]: Muestra los detalles del item especificado de la lista obtenida\n'
        value += f'-a / -ba / -avanzada / -avanzado: Realiza una busqueda en los detalles de los items, no solo en el nombre (Usar en casos especificos ya que tarda en regresar una respuesta)'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = f'{self.prefijo}b gearl97 -f flux\n'
        value += f'{self.prefijo}buscar gearl97 wither -d 3'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}b", "{self.prefijo}buscar", "{self.prefijo}busqueda"'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def best_minions(self, msg, text = ''):
        titulo = f'{self.prefijo}bm (opciones)'
        description = f'Muestra los mejores minios en un tiempo determinado\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-t / -tiempo [tiempo en horas]: El tiempo a evaluar de los minions. (Default 24 horas)\n'
        value += f'-l / -level / -lvl: Evalua a un nivel especifico. (Default nivel 11)\n'
        value += f'-ss / -sinSalyer / -sinSlayers: Los minions evaluados no incluirean a los minios de slayers\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = f'{self.prefijo}bm -t 2\n'
        value += f'{self.prefijo}best_minions -t 4 -l 7\n'
        value += f'{self.prefijo}best_minion -l 9 -ss\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}bm", "{self.prefijo}best", "{self.prefijo}best_minions", "{self.prefijo}best_minion"'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def minions(self, msg, text = ''):
        titulo = f'{self.prefijo}m [nombre] (opciones)'
        description = f'Muestra detalles de un minion en todos sus niveles\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Nombre del minion. Acepta parte del nombre en casi de no conocerlo completo\n'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-t / -tiempo [tiempo en horas]: El tiempo a evaluar de los minions. (Default 24 horas)\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Ejemplos'
        value = f'{self.prefijo}m revena\n'
        value += f'{self.prefijo}minion snow -t 4\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}m", "{self.prefijo}minion", "{self.prefijo}minions"'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def recomendacion(self, msg, text = ''):
        titulo = f'{self.prefijo}rec [mensaje] (opciones)'
        description = f'Envia Recomendaciones o sugerencias al desarrollador\n'
        description += f'El mensaje sera eliminado una vez enviado para mantenerlo privado\n'
        color = self.color_aleatorio()
        embed = discord.Embed(title=titulo, description=description, color = color)

        name = 'Argumentos'
        value = ''
        value += f'Requerido: Mensaje a enviar\n'
        value += f'Opcional: Opciones acontinuacion mostradas:'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Opciones'
        value = ''
        value += f'-an: La sugerencia sera anonima\n'
        value += f'-r: Se indica que se espera respuesta\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Alias'
        value = f'"{self.prefijo}sug", "{self.prefijo}sugerencia", "{self.prefijo}sugerencias", "{self.prefijo}sugerir", "{self.prefijo}recomendacion", "{self.prefijo}recomendaciones"\n'
        embed.add_field(name=name, value=value, inline = False)

        return msg.channel.send(embed = embed)

    def evento(self, msg, text =''):
        if msg.author.id not in self.event_ids:
            return msg.reply('No tienes permiso para usar este comando')
        color = self.color_aleatorio()
        title = 'Comandos para el evento de Hallowen'
        embed = discord.Embed(title=title, color = color)

        name = 'Confirmar entrega'
        value = f'{self.prefijo}hall_e / {self.prefijo}hall_entregado / {self.prefijo}hall_entrega  id_peticion\n'
        value += f'Ejemplo: {self.prefijo}hall_e 899665021611704380'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Verificar el estado de una peticion'
        value = f'{self.prefijo}hall_status  id_peticion\n'
        value += f'Ejemplo: {self.prefijo}hall_status 899665021611704380'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Revisar inventario de algun usuario'
        value = f'{self.prefijo}event_inv tag\n'
        value += f'Ejemplo: {self.prefijo}event_inv @Nombre#0000'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Revisiar peticiones pendientes'
        value = f'{self.prefijo}hall_pendiente\n'
        embed.add_field(name=name, value=value, inline = False)

        name = 'Revisar peticiones de un usuario'
        value = f'{self.prefijo}hall_user  tag\n'
        value += f'Ejemplo: {self.prefijo}hall_user @Nombre#0000'
        embed.add_field(name=name, value=value, inline = False)
        return msg.reply(embed = embed)


    def config(self):
        self.funciones = {
            'help': self.help,
            'h': self.help,
            'help_clear': self.clear,
            'help_c': self.clear,
            'help_clean': self.clear,
            'help_limpiar': self.clear,
            'help_a': self.auction,
            'help_ah': self.auction,
            'help_auction': self.auction,
            'help_auctions': self.auction,
            'help_bz': self.bazar,
            'help_bazar': self.bazar,
            'help_i': self.inventario,
            'help_inv': self.inventario,
            'help_inventario': self.inventario,
            'help_inventory': self.inventario,
            'help_pah': self.player_auction,
            'help_playerah': self.player_auction,
            'help_bm': self.best_minions,
            'help_best_minions': self.best_minions,
            'help_best': self.best_minions,
            'help_best_minion': self.best_minions,
            'help_minions': self.minions,
            'help_m': self.minions,
            'help_minion': self.minions,
            'help_wd': self.wardrobe,
            'help_wardrobe': self.wardrobe,
            'help_ender_chest': self.ender_chest,
            'help_ec': self.ender_chest,
            'help_backpack': self.backpack,
            'help_bp': self.backpack,
            'help_buscar': self.buscar,
            'help_b': self.buscar,
            'help_busqueda': self.buscar,
            'help_rec': self.recomendacion,
            'help_sug': self.recomendacion,
            'help_sugerencia': self.recomendacion,
            'help_sugerencias': self.recomendacion,
            'help_sugerir': self.recomendacion,
            'help_recomendacion': self.recomendacion,
            'help_recomendaciones': self.recomendacion,
            'help_evento': self.evento,
            'help_event': self.evento,
        }
