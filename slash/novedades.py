import json
import discord
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dislash.interactions import *
from datetime import datetime
from slash.generales import Generales
class Novedades(commands.Cog, Generales):
    def __init__(self, bot):
        self.bot = bot
    prefijo = '+'

    @cog_ext.cog_slash(name="news", description="Muestra las novedades del bot")
    async def novedades(self, msg: SlashContext):
        color = self.color_aleatorio()
        title = f'Novedades del bot'
        embed = discord.Embed(title = title, color = color)
        #name = f'Lunes, 6 de Septiembre de 2021:\n'
        #value = f'\t•Se agrego el comando novedades. ({self.prefijo}news)\n'
        #value += f'\t•Se agregaron datos de foragin minions\n'
        #value += f'\t•Cambios en nombres de items del bazar\n'
        #value += f'\t•Opcion Anonima en sugerencias (-an)\n'
        #value += f'\t•Opcion para ser contactado (-r)\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f'Jueves, 9 de Septiembre de 2021:\n'
        #value = f'\t•Cambio en el permiso del comando {self.prefijo}clear\n'
        #value += f'\t•El bot ya no funciona en mensaje directo. Solo en servers\n'
        #value += f'\t•El comando {self.prefijo}sug ahora agradece en privado y ya no en el servidor\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f'Viernes, 10 de Septiembre de 2021:\n'
        #value = f'\t•Se agrego el comando de slayers ({self.prefijo}slayer)\n'
        #value += f'\t•Iniciando correcciones de bugs en slayers\n'
        #value += f'\t•Correccion de slayer en perfiles cooperativos\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f'Martes, 14 de Septiembre de 2021:\n'
        #value = ''
        #value += f'\t•Iniciando correcciones de bugs para perfiles cooperativos\n'
        #value += f'\t•Correccion de bugs para perfiles cooperativos en los comandos inventario, wardrobe, ender_chest, backpack y buscar\n'
        #value += f'\t•Ahora para especificar un numero de backpack se debe poner -n/-numero y el numero de la backpack. Ejemplo: -n 2\n'
        #value += f'\t•Eliminado comando suma, queda comando {self.prefijo}calc/{self.prefijo}op\n'
        #value += f'\t•Agregado {self.prefijo}bm\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f'Sabado, 18 de Septiembre de 2021\n'
        #value = ''
        #value += f'\t•Correccion en {self.prefijo}sy\n'
        #value += f'\t•Cambio de app en server\n'
        #value += f'\t•Cambio en api-key\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f'Martes, 21 de Septiembre de 2021\n'
        #value = ''
        #value += f'\t•Iniciando desarrollo de comando corto en {self.prefijo}sy (no sera requerido -s)\n'
        #value += f'\t•Iniciando correcciones de datos en {self.prefijo}ah y {self.prefijo}pah cuando estan en modo subasta\n'
        #value += f'\t•Iniciando nueva impresion de datos en {self.prefijo}pah\n'
        #value += f'\t•__*Cambio en modulo de solicitud de datos a la api de hypixel*__\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Miercoles, 22 de Septiembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Arreglo en comandos afectados por inicios de cambios de ayer` :point_up_2:\n'
        #value += f':small_orange_diamond: `Inicia mejora en impresion de varios comandos` (<:axolote:890258483813957663>)\n'
        #value += f':small_orange_diamond: `-s en "{self.prefijo}slayer" pasa a ser opcion y no requisito`\n'
        #value += f':small_orange_diamond: `Nueva forma de mostrar los datos en "{self.prefijo}slayer"`\n'
        #value += f':small_orange_diamond: `Correccion de bugs en "{self.prefijo}slayer"`\n'
        #value += f':small_orange_diamond: `Nueva forma de mostrar "{self.prefijo}pah"`\n'
        #value += f':small_orange_diamond: `Se agrega opcion -e a "{self.prefijo}pah"`\n'
        #value += f':small_orange_diamond: `Cambio en visualizacion de "{self.prefijo}h"`\n'

        #embed.add_field(name = name, value = value, inline = False)
        
        #name = f':diamond_shape_with_a_dot_inside: Jueves, 23 de Septiembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Se agregaron mas imagenes de items en varios comandos`\n'
        #value += f':small_orange_diamond: `Cambio de impresion en "{self.prefijo}pah"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Viernes, 24 de Septiembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Mas items con imagen`\n'
        #value += f':small_orange_diamond: `Correccion de bugs en comando "{self.prefijo}b"`\n'
        #value += f':small_orange_diamond: `Inicia desarrollo de comando "{self.prefijo}pets"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Sabado, 25 de Septiembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Se agrega comando "{self.prefijo}pets"`\n'
        #value += f':small_orange_diamond: `Cambio en las opciones del comando "{self.prefijo}ah"`\n'
        #value += f':small_orange_diamond: `Primera version de comando "{self.prefijo}tal"`\n'
        #value += f':small_orange_diamond: `Navegacion por reacciones en comandos de mas de una pagina`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Domingo, 26 de Septiembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado comando "{self.prefijo}es"`\n'
        #value += f':small_orange_diamond: `Inicia desarrollo de comando "{self.prefijo}hotm"`\n'
        #value += f':small_orange_diamond: `Inicia desarrollo de forge "{self.prefijo}forge"`\n'
        #value += f':small_orange_diamond: `Primera version del comando "{self.prefijo}hotm"`\n'
        #value += f':small_orange_diamond: `Nueva forma de impresion de tiempo y precio en "{self.prefijo}ah" y {self.prefijo}pah`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Lunes, 27 de Septiembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Se agrego informacion sobre nucleos en segunda pagina "{self.prefijo}hotm"`\n'
        #value += f':small_orange_diamond: `Primera version de comando "{self.prefijo}forge"`\n'
        #value += f':small_orange_diamond: `Inician mejoras en comando "{self.prefijo}tal"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Martes, 28 de Septiembre de 2021\n'  
        #value = ''
        #value += f':small_orange_diamond: `Cambio en forma de mostrar "{self.prefijo}ec" y "{self.prefijo}buscar"`\n'
        #value += f':small_orange_diamond: `Arreglo de bug que no mostraba todas las pets en "{self.prefijo}pet"`\n'
        #value += f':small_orange_diamond: `Correccion de bugs en "{self.prefijo}forge"`\n'

        #embed.add_field(name = name, value = value, inline = False)
        
        #name = f':diamond_shape_with_a_dot_inside: Miércoles, 29 de Septiembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agilizado metodo de obtencion y guardado de emojis (interno)`\n'
        #value += f':small_orange_diamond: `Obtencion automatizada de emojis faltantes (Interno)`\n'
        #value += f':small_orange_diamond: `Aumento de servidores para detalle (Interno)`\n'
        #value += f':small_orange_diamond: `Agregados mas imagenes de items`\n'
        #value += f':small_orange_diamond: `Ahora se muesta ultimo perfil activo y no el primero si no se especifica nombre de perfil`\n'
        #value += f':small_orange_diamond: `Correccion en tiempos de comando "{self.prefijo}pah"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Sabado, 2 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Inicia cambio a compandos slash`\n'
        #value += f':small_orange_diamond: `Los comandos "{self.prefijo}" seguiran funcionando hasta que termine el cambio de todos los comandos anteriores`\n'
        #value += f':small_orange_diamond: `Los nuevos comandos funcionaran con comando slash`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Lunes, 4 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Correccion de busqueda de libros encantados en "/auction_house"`\n'
        #value += f':small_orange_diamond: 🎃\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Martes, 5 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregada pagina 4 a "/hotm"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Miércoles, 6 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregada slash command "/help"`\n'
        #value += f':small_orange_diamond: `Agregadas opciones en la opcion de slayer en "/slayer"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Viernes, 8 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado soporte para operaciones con "k, m, b" en "/operacion"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Lunes, 11 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Arreglo de bug en "/slayer" con slayer maxeada`\n'
        #value += f':small_orange_diamond: `Ahora los items de evento tambien se pueden obtener en mensajes normales y no solo en comandos`\n'
        
        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Martes, 12 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Mas dropeos en evento`\n'
        #value += f':small_orange_diamond: `Comandos de administracion del evento`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Miércoles, 13 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Cambio de comandos pets y talismanes a slash commands`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Jueves, 14 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Cambio de comandos inventario y ender_chest a slash commands`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Sabado, 23 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `slash commands de varias palabras ahora separadas por mayuscula y no con guion bajo (_)\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Lunes, 25 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado slash command "/wardrobe"`\n'
        #value += f':small_orange_diamond: `Se libera el comando "/hallClaim"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Martes, 26 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado slash command "/backpack"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Miércoles, 27 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado slash command "/buscar"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Jueves, 28 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado slash command "/kills"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Domingo, 31 de Octubre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `"/hotm" ahora muestra el Powder en la pagina 4`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Lunes, 1 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Gracias por participar en el evento de Hallowen, los comandos de hallowen serviran unos dias mas`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Miercoles, 3 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado comando "/skills"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Sabado, 6 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado comando "/verificar"`\n'
        #value += f':small_orange_diamond: `Iniciando cambio en comandos slash para agilizar su uso con la verificacion`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Lunes, 8 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Quitados comandos de hallowen`\n'
        #value += f':small_orange_diamond: `Soporte para perks activos de Aatrox en "/slayer"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Martes, 9 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado comando "/item"`\n'
        #value += f':small_orange_diamond: `Empezando a agregar informacion de items"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Miércoles, 10 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregados Refine Ores y necron blades a "/item"`\n'
        
        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Jueves, 11 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregados items de forja hasta hotm 3 a "/item"`\n'
        #value += f':small_orange_diamond: `Agregados items de la lista recibida pendiente a "/item"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Sabado, 13 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Correccion en los tiempos de "/forja" cuando se tiene el perk Quick Forge`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Lunes, 15 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Se agrego guia para vincular discord con hypixel "/guiaverificar"`\n'
        #value += f':small_orange_diamond: `Se agrega comando "/reforje"`\n'
        #value += f':small_orange_diamond: `Se agregan algunos reforjes a "/reforje"`\n'
        #value += f':small_orange_diamond: `Deja de funcionar "{self.prefijo}slayer" se pasa a "/slayer"`\n'
        #value += f':small_orange_diamond: `Agregados reforjes de cañas y espadas en "/reforje"`\n'

        #embed.add_field(name = name, value = value, inline = False)
        
        #name = f':diamond_shape_with_a_dot_inside: Martes, 16 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregado comando "/adios"`\n'
        #value += f':small_orange_diamond: `Mas saludos en "/hola"`\n'
        #value += f':small_orange_diamond: `Agregados reforjes de arcos de blacksmith "/reforje"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Jueves, 18 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Rework de comando "/auctionHouse"`\n'
        #value += f':small_orange_diamond: `"/auctionHouse" ahora muestra datos de pets y enchants y soporte para filtrar por rareza`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Viernes, 19 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Mejora del algoritmo de busqueda en "/item"`\n'
        #value += f':small_orange_diamond: `Agregados items de lista primordial a "/item"`\n'

        #embed.add_field(name = name, value = value, inline = False)

        #name = f':diamond_shape_with_a_dot_inside: Sabado, 20 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregados los items faltantes de forja a "/item"`\n'
        #value += f':small_orange_diamond: `Opcion "quitar" para mejor busqueda en "/item"`\n'
        #value += f':small_orange_diamond: `Agregadas stones para arcos "/reforje"`\n'
#
        #embed.add_field(name = name, value = value, inline = False)
        #
        #name = f':diamond_shape_with_a_dot_inside: Domingo, 28 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Nuevo metodo de navegacion en "/slayer"`\n'
        #value += f':small_orange_diamond: `Nuevo metodo de navegacion en "/hotm"`\n'
        #
        #embed.add_field(name = name, value = value, inline = False)
        #
        #name = f':diamond_shape_with_a_dot_inside: Lunes, 29 de Noviembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Navegacion por botones modularizada (interno)`\n'
        #value += f':small_orange_diamond: `Los botones ahora desaparecen despues de no ser utilizados en 3 minutos`\n'
        #value += f':small_orange_diamond: `Nuevas opciones en "/news"`\n'
        #value += f':small_orange_diamond: `Cambio en impresion de "/skill"`\n'
        #
        #embed.add_field(name = name, value = value, inline = False)
        #
        #name = f':diamond_shape_with_a_dot_inside: Lunes, 6 de Diciembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregados items y reforjes pendientes de lista pendiente`\n'
        #
        #embed.add_field(name = name, value = value, inline = False)
        #
        #name = f':diamond_shape_with_a_dot_inside: Viernes, 10 de Diciembre de 2021\n'
        #value = ''
        #value += f':small_orange_diamond: `Agregados items de lista pendiente`\n'
        #value += f':small_orange_diamond: `/buscarguild mudado a archivo propio`\n'
        #
        #embed.add_field(name = name, value = value, inline = False)
        #
        name = f':diamond_shape_with_a_dot_inside: Miercoles, 22 de Diciembre de 2021\n'
        value = ''
        value += f':small_orange_diamond: `Se libera el bot y se agrega comando /invitar`\n'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f':diamond_shape_with_a_dot_inside: Jueves, 23 de Diciembre de 2021\n'
        value = ''
        value += f':small_orange_diamond: `Cambios en: Nombre, Imagen, /invitar`\n'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f':diamond_shape_with_a_dot_inside: Sabado, 25 de Diciembre de 2021\n'
        value = ''
        value += f':small_orange_diamond: `Agregados comandos /sugerencia y /bug`\n'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f':diamond_shape_with_a_dot_inside: Domingo, 26 de Diciembre de 2021\n'
        value = ''
        value += f':small_orange_diamond: `Primera version de comando /player`\n'
        value += f':small_orange_diamond: `Iniciando nuevo sistema de coleccion de auction house`\n'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f':diamond_shape_with_a_dot_inside: Miercoles, 29 de Diciembre de 2021\n'
        value = ''
        value += f':small_orange_diamond: `Ahora los botones desaparecen en 1 minuto en lugar de 3`\n'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f':diamond_shape_with_a_dot_inside: Viernes, 31 de Diciembre de 2021\n'
        value = ''
        value += f':small_orange_diamond: `Arreglos en  bug de /auctionplayer`\n'
        value += f':small_orange_diamond: `Cambios en replaces de /bazar`\n'
        value += f':small_orange_diamond: `Feliz año nuevo y /feliz2022`\n'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f':diamond_shape_with_a_dot_inside: Lunes, 3 de Enero de 2022\n'
        value = ''
        value += f':small_orange_diamond: `Cambio de navegacion en /slayer y /hotm`\n'
        value += f':small_orange_diamond: `/slayer ahora muesta el numero de cada tier concluido`\n'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f':diamond_shape_with_a_dot_inside: Miercoles, 19 de Enero de 2022\n'
        value = ''
        value += f':small_orange_diamond: `Corrección de bug en /invitar`\n'
        
        embed.add_field(name = name, value = value, inline = False)
        
        name = f':diamond_shape_with_a_dot_inside: Lunes, 30 de Enero de 2022\n'
        value = ''
        value += f':small_orange_diamond: `Corrección y mejora en busqueda de /auctionhouse`\n'
        
        embed.add_field(name = name, value = value, inline = False)

        text = f'Recuerda que puedes enviar sugerencias con "/sugerencia" o reportar algun bug con "/bug"\n'
        text += f'Todas son leidas y tomadas en cuenta'
        dropeos_hall = self.dropeo_hall(msg)
        if dropeos_hall[0]:
            text += dropeos_hall[1]
        embed.set_footer(text = text)
        embed_hoy = discord.Embed(title = 'Ultima Actualizacion', color = color)
        embed_hoy.add_field(name = name, value = value, inline = False)
        embed_hoy.set_footer(text = text)
        
        componentes = [
            {
                "type": 1,
                "components": [
                        {
                            "type": 2,
                            "label": "Ultima actualizacion",
                            "custom_id": "0",
                            "style": 2
                        },
                        {
                            "type": 2,
                            "label": "Lista Extendida",
                            "custom_id": "1",
                            "style": 2
                        }
                ]
            }
        ]
        
        self.original_msg = msg
        msg = await msg.reply(embed = embed_hoy, components = componentes)
        embeds = [embed_hoy, embed]
        self.msg = msg 
        await self.esperando_boton_embed(msg, embeds, abierto = True)

    def config(self, datos = False, n = 0):
        if datos:
            self.hypixel_api = datos['hypixel_api']
        else:
            self.hypixel_api = self.apis[n]

def setup(bot):
    bot.add_cog(Novedades(bot))