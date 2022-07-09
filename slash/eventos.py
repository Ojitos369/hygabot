

class Evento():
    dropeos_hallowen = {
        'calabaza': {
            'id': 'calabaza',
            'emoji': '🎃',
            'probabilidad': 1 /12,
            'value': '1 k de coins',
            'valor': '1k'
        },
        'esqueleto': {
            'id': 'esqueleto',
            'emoji': '💀',
            'probabilidad': 1 /60,
            'value': '10 k de coins',
            'valor': '10k'
        },
        'god_potion': {
            'id': 'god_potion',
            'emoji': '<:god_potion:892812740282941470>',
            'probabilidad': 1 /625,
            'value': 'Una god potion <:god_potion:892812740282941470>',
            'valor': None
        },
        'revenant': {
            'id': 'revenant',
            'emoji': '<:revenant:892834994832162817>',
            'probabilidad': 1 /110,
            'value': '50k de coins',
            'valor': '50k'
        },
        'tarantula': {
            'id': 'tarantula',
            'emoji': '<:tarantula:892834995125755964>',
            'probabilidad': 1 /225,
            'value': '100k de coins',
            'valor': '100k'
        },
        'sven': {
            'id': 'sven',
            'emoji': '<:sven:892834995239022602>',
            'probabilidad': 1 /575,
            'value': '500k de coins',
            'valor': '500k'
        },
        'voidgloom': {
            'id': 'voidgloom',
            'emoji': '<:voidgloom:892834995163512832>',
            'probabilidad': 1 /1025,
            'value': '1m de coins',
            'valor': '1m'
        }
    }

    def dropeo_hall(self, msg, comando = True):
        return False, ''
        user_id = msg.author.id
        username = msg.author.id
        try:
            tamanio_mensaje = len(msg.content)
            len_separado = len(msg.content.split())
        except:
            tamanio_mensaje = 7
            len_separado = 1
        guild_id = msg.guild.id
        if not (str(guild_id) == '831264016101802064' or str(guild_id) == '745106115934683177'):
            return False, ''
        other_bot = False
        if not comando:
            msg_content = msg.content.lower()
            # starts with ! or , or ; or . or / or ? or ( or )  or -
            if msg_content.startswith('!') or msg_content.startswith(',') or msg_content.startswith(';') or msg_content.startswith('.') or msg_content.startswith('/') or msg_content.startswith('?') or msg_content.startswith('(') or msg_content.startswith(')') or msg_content.startswith('-'):
                return False, ''
        if not comando:
            if tamanio_mensaje < 8 or len_separado < 2:
                return False, ''
        #username = msg.author.name
        from verificar import consulta, ejecutar, get_mochila
        import random
        
        mochila = ''
        dh = self.dropeos_hallowen
        items_obtenidos = []
        #print()
        #if comando:
            #print('Probabilidad con comando')
        #else:
            #print('Probabilidad normal')
        for  item, datos in dh.items():
            prob = random.random() * 100
            cantidad = 0
            item_prob = dh[item]['probabilidad']
            if comando:
                item_prob *= 18
            else:
                item_prob *= 2.1
            item_prob *= 100
            #print(f'{item} : {item_prob}')
            if prob <= item_prob:
                cantidad = 1
            if cantidad != 0:
                cantidad_actual = -1
                if mochila == '': mochila = get_mochila(user_id, username)
                try:
                    for elemento in mochila:
                        if elemento[2] == item:
                            cantidad_actual = elemento[3]
                            break
                except:
                    pass
                if cantidad_actual != -1:
                    query = f"UPDATE mochila SET cantidad = {cantidad_actual + cantidad} WHERE user_id = '{user_id}' and item_id = '{datos['id']}'"
                    ejecutar(query)
                else:
                    query = f"INSERT INTO mochila (id, user_id, item_id, cantidad) VALUES ('{user_id}_{datos['id']}', '{user_id}', '{datos['id']}', {cantidad})"
                    ejecutar(query)
                items_obtenidos.append([item, cantidad])
        text = ''
        dropeo_seccess = False
        if len(items_obtenidos) != 0:
            text += '\nHas encontrado:\n'
            for item in items_obtenidos:
                item_name = item[0]
                item_cantidad = item[1]
                if comando:
                    text += f"{item_name.replace('_', ' ')} x{item_cantidad}\n"
                else:
                    text += f"{dh[item_name]['emoji']} x{item_cantidad}\n"
            text += 'Revisa /hallBag para ver tu inventario'
            dropeo_seccess = True
        return [dropeo_seccess, text]

