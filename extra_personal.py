import json

def replaces(item):
    replaces_dict = {
        "'": '',
        "_": ' ',
        ".": '',
        "-": '',
        "(": "",
        ")": ""
    }
    for key, value in replaces_dict.items():
        item = item.replace(key, value)
    return item

def acomodar():
    with open('./json/items.json') as datos:
        items_data = json.load(datos)
    
    new_dic = {}
    letras_disponibles = []
    for letra in items_data:
        letras_disponibles.append(letra)
    
    #letras_disponibles = sorted(letras_disponibles)
    letras_disponibles = sorted(letras_disponibles, key=lambda x: (x[0].isdigit(), x))
    for letra in letras_disponibles:
        items = items_data[letra]
        for item in items:
            item_name = item.lower()
            item_name = replaces(item_name)
            try:
                alias = items[item]['alias']
                alias = alias.lower()
                alias = replaces(alias)
            except:
                alias = ''
            let_dis = []
            for pal in item_name.split():
                let = pal[0]
                if let not in let_dis:
                    let_dis.append(let)
            if alias != '':
                for pal in alias.split():
                    let = pal[0]
                    if let not in let_dis:
                        let_dis.append(let)
            let_dis = sorted(let_dis, key=lambda x: (x[0].isdigit(), x))
            for letter in let_dis:
                if letter not in new_dic:
                    new_dic[letter] = {}
                if item not in new_dic[letter]:
                    new_dic[letter][item] = items[item]
    
    #order new_dic
    new_dic_ord = {}
    letras_disponibles = []
    for letra in new_dic:
        letras_disponibles.append(letra)
    letras_disponibles = sorted(letras_disponibles, key=lambda x: (x[0].isdigit(), x))
    for letra in letras_disponibles:
        items = new_dic[letra]
        palabras = []
        for item in items:
            palabras.append(item)

        # sorted palabras first letter after numbers
        palabras = sorted(palabras, key=lambda x: (x[0].isdigit(), x))
        #palabras = sorted(palabras)
        new_dic_ord[letra] = {}
        for palabra in palabras:
            new_dic_ord[letra][palabra] = items[palabra]

    open(f'./json/items.json', 'w').write(json.dumps(new_dic_ord, indent=4))

def agregar():
    with open('./info_pruebas/pruebas.json') as datos:
        items = json.load(datos)
    with open('./json/items.json') as datos:
        items_data = json.load(datos)
    try:
        del items["pendientes"]
    except:
        pass
    for item in items:
        item_name = item.replace('_', ' ').lower()
        try:
            alias = items[item]['alias']
            alias = alias.lower()
            alias = replaces(alias)
        except:
            alias = ''
        letras = []
        for palabra in item_name.split():
            letra = palabra[0]
            if letra not in letras:
                letras.append(letra)
        if alias != '':
            for palabra in alias.split():
                letra = palabra[0]
                if letra not in letras:
                    letras.append(letra)
        for letra in letras:
            if letra not in items_data:
                items_data[letra] = {}
            if item not in items_data[letra]:
                items_data[letra][item] = items[item]
            else:
                del items_data[letra][item]
                items_data[letra][item] = items[item]
    open(f'./json/items.json', 'w').write(json.dumps(items_data, indent=4))

agregar()
acomodar()