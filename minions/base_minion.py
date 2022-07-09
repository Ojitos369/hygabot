from funciones.bazar import Bazar

class Minion:
    def __init__(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[]):
        self.name = name
        self.nivel = nivel
        self.bazar = Bazar()
        self.delay = delay
        self.drops_per_action = drops_per_action
        self.enchat_at = enchat_at
        self.items_producibles = items_producibles
        self.diamond = diamond
        self.productos_diferentes = productos_diferentes
        self.porcentaje_por_item = porcentaje_por_item
        self.diamantes = ''
        self.enchanted_diamantes = ''
        self.bloques_de_diamantes_encantados = ''
        self.basico = ''
        self.encantado = ''
        self.bloque_encantado = ''

    def produccion_por_dia(self, horas, fuel):
        produccion_diaria = (60 * 60 * horas) / (self.delay * 4.2)
        produccion_diaria += produccion_diaria * fuel
        items = {}
        diamantes_totales = 0
        items_totales = 0
        if self.productos_diferentes == 1:
            produccion_diaria *= self.drops_per_action
            if self.diamond and self.name != 'Diamond':
                diamantes_diarios = int(produccion_diaria / 10)
                produccion_diaria -= diamantes_diarios
                diamantes_totales += diamantes_diarios
            items_totales += produccion_diaria
            self.basico = int(produccion_diaria % self.enchat_at[0])
            produccion_diaria -= self.basico
            enchanted = int(produccion_diaria / self.enchat_at[0])
            if self.enchat_at[1] != 0:
                self.encantado = int(enchanted % self.enchat_at[1])
                enchanted -= self.encantado
                self.bloque_encantado = int(enchanted / self.enchat_at[1])
            else:
                self.encantado = enchanted
                self.bloque_encantado = 0
            items[f'{self.items_producibles[2].lower()}'] = self.bloque_encantado
            items[f'{self.items_producibles[1].lower()}'] = self.encantado
            items[f'{self.items_producibles[0].lower()}'] = self.basico
        else:
            self.basico = []
            self.encantado = []
            self.bloque_encantado = []
            for i in range(self.productos_diferentes):
                diario_produc = produccion_diaria * self.porcentaje_por_item[i] * self.drops_per_action[i]
                if self.diamond and self.name != 'Diamond':
                    diamantes_diarios = int(diario_produc / 10)
                    diario_produc -= diamantes_diarios
                    diamantes_totales += diamantes_diarios
                items_totales += diario_produc
                if self.items_producibles[i][0].lower() == 'diamond':
                    diamantes_totales += diario_produc
                    self.basico.append(0)
                    self.encantado.append(0)
                    self.bloque_encantado.append(0)
                    items[f'{self.items_producibles[i][2].lower()}'] = 0
                    items[f'{self.items_producibles[i][1].lower()}'] = 0
                    items[f'{self.items_producibles[i][0].lower()}'] = 0
                else:
                    self.basico.append(int(diario_produc % self.enchat_at[i][0]))
                    diario_produc -= self.basico[i]
                    enchanted = int(diario_produc / self.enchat_at[i][0])
                    if self.enchat_at[i][1] != 0:
                        self.encantado.append(int(enchanted % self.enchat_at[i][1]))
                        enchanted -= self.encantado[i]
                        self.bloque_encantado.append(int(enchanted / self.enchat_at[i][1]))
                    else:
                        self.encantado.append(enchanted)
                        self.bloque_encantado.append(0)
                    items[f'{self.items_producibles[i][2].lower()}'] = self.bloque_encantado[i]
                    items[f'{self.items_producibles[i][1].lower()}'] = self.encantado[i]
                    items[f'{self.items_producibles[i][0].lower()}'] = self.basico[i]

        if self.diamond and self.name != 'Diamond':
            self.diamantes = int(diamantes_totales % 160)
            diamantes_totales -= self.diamantes
            encantados = int(diamantes_totales / 160)
            self.enchanted_diamantes = encantados % 160
            encantados -= self.enchanted_diamantes
            self.bloques_de_diamantes_encantados = int(encantados / 160)
            items['diamond'] = self.diamantes
            items['enchanted diamond block'] = self.bloques_de_diamantes_encantados
            items['enchanted diamond'] = self.enchanted_diamantes

        return items

    def items_value(self, horas, fuel, bazar = None):
        items = self.produccion_por_dia(horas, fuel)
        if bazar is None:
            datos = self.bazar.bazar(text = 'consulta para minions', for_minions = True)
        else:
            datos = bazar
        ganancias = [0, 0, 0]
        for dato in datos.values():
            item_name = dato['product_id'].replace('_', ' ').lower()
            if item_name in items:
                sell_order = float(dato["buy_summary"][0]['pricePerUnit']) * items[item_name]
                sell_insta = float(dato['quick_status']['sellPrice']) * items[item_name]
                ganancias[0] += sell_order
                ganancias[1] += sell_insta
        return ganancias

    def detalles(self, horas, fuel, bazar = None):
        mensaje = {}
        ganancias_diarias = self.items_value(horas, fuel, bazar)
        if fuel == 0:
            name = f'Produccion de {self.name} minion nivel {self.nivel} en {horas} horas'
        else:
            name = f'Produccion de {self.name} minion nivel {self.nivel} en {horas} horas con {fuel * 100}% de aumento de velocidad'
        value = ''
        if self.productos_diferentes == 1:
            if self.basico > 0:
                value += f"{self.items_producibles[0].capitalize()}: {self.basico}\n"
            if self.encantado > 0:
                value += f"{self.items_producibles[1].capitalize()}: {self.encantado}\n"
            if self.bloque_encantado != 0:
                value += f"{self.items_producibles[2].capitalize()}: {self.bloque_encantado}\n"
        else:
            for i in range(self.productos_diferentes):
                if self.basico[i] > 0:
                    value += f"{self.items_producibles[i][0].capitalize()}: {self.basico[i]}\n"
                if self.encantado[i] > 0:
                    value += f"{self.items_producibles[i][1].capitalize()}: {self.encantado[i]}\n"
                if self.bloque_encantado[i] != 0:
                    value += f"{self.items_producibles[i][2].capitalize()}: {self.bloque_encantado[i]}\n"
        if self.diamond and self.name != 'Diamond':
            if self.diamantes > 0:
                value += f"Diamantes: {self.diamantes}\n"
            if self.enchanted_diamantes > 0:
                value += f"Diamantes encantados: {self.enchanted_diamantes}\n"
            if self.bloques_de_diamantes_encantados > 0:
                value += f"Bloques de diamantes encantados: {self.bloques_de_diamantes_encantados}\n"
        value += f"Total producido en {horas} horas con venta en sell order: "+ "{:,.2f}".format(ganancias_diarias[0]) + "\n"
        value += f"Total producido en {horas} horas con venta en sell insta: "+ "{:,.2f}".format(ganancias_diarias[1]) + "\n"
        mensaje['name'] = name
        mensaje['value'] = value
        return mensaje

    def datos(self, horas, fuel, bazar = None):
        ganancias_diarias = self.items_value(horas, fuel, bazar)
        diamonds = [self.diamantes, self.enchanted_diamantes, self.bloques_de_diamantes_encantados]
        values = {
            'name': self.name,
            'nivel': self.nivel,
            'diferentes': self.productos_diferentes,
            'producibles': self.items_producibles,
            'diamantes': diamonds,
            'ganancias': ganancias_diarias
        }
        return values