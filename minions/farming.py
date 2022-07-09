from minions.base_minion import Minion

def wheat():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [15, 15, 13, 13, 11, 11, 10, 10, 9, 9, 8, 7]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Wheat',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [1, 1.5],
            enchat_at = [
                [60, 0],
                [160, 0]
            ],
            items_producibles = [
                ['wheat', 'enchanted bread', ''],
                ['seeds', 'enchanted seeds', '']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                0.5, 0.5
            ]
        ))
    return minions

def carrot():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [20,20,18,18,16,16,14,14,12,12,10,8]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Carrot',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 3,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'carrot item',
                'Enchanted carrot',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def potato():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [20,20,18,18,16,16,14,14,12,12,10,8]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Potato',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 3,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'potato item',
                'Enchanted potato',
                'Enchanted baked potato'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def pumpkin():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [20,20,18,18,16,16,14,14,12,12,10,8]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Pumpkin',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'pumpkin',
                'Enchanted pumpkin',
                'polished pumpkin'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def melon():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [24,24,22.5,22.5,21,21,18.5,18.5,16,16,13,10]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Melon',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 5,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'melon',
                'Enchanted melon',
                'Enchanted melon block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def mushroom():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [30,30,28,28,26,26,23,23,20,20,16,12]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Mushroom',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [1, 1],
            enchat_at = [
                [160, 0],
                [160, 0]
            ],
            items_producibles = [
                ['red mushroom', 'enchanted red mushroom', ''],
                ['brown mushroom', 'enchanted brown mushroom', '']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                0.5, 0.5
            ]
        ))
    return minions

def cocoa():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [27, 27, 25, 25, 23, 23, 21, 21, 18, 18, 15, 12]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Cocoa Beans',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 3,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'ink sack:3',
                'Enchanted cocoa',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def cactus():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [27, 27, 25, 25, 23, 23, 21, 21, 18, 18, 15, 12]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Cactus',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 3,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'Cactus',
                'Enchanted cactus green',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def sugar():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [20,20,18,18,16,16,14,14,12,12,10,8]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Sugar Cane',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 3,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'sugar cane',
                'Enchanted sugar',
                'Enchanted sugar cane'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def cow():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,20,20,17,17,13,10]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Cow',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [1, 1],
            enchat_at = [
                [160, 0],
                [576, 0]
            ],
            items_producibles = [
                ['raw beef', 'enchanted raw beef', ''],
                ['leather', 'enchanted leather', '']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                1, 1
            ]
        ))
    return minions

def pig():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,20,20,17,17,13,10]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Pig',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'pork',
                'Enchanted pork',
                'Enchanted grilled pork'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def chicken():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,20,20,18,18,15,12]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Chicken',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [1, 1, 1],
            enchat_at = [
                [160, 0],
                [160, 0],
                [144, 144]
            ],
            items_producibles = [
                ['raw chicken', 'enchanted raw chicken', ''],
                ['feather', 'enchanted feather', ''],
                ['egg', 'enchanted egg', 'super egg']                
            ],
            productos_diferentes = 3,
            porcentaje_por_item = [
                1, 1, 1
            ],
            diamond = False
        ))
    return minions

def sheep():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [24,24,22,22,20,20,18,18,16,16,12,9]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Sheep',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [1, 1],
            enchat_at = [
                [160, 160],
                [160, 0]
            ],
            items_producibles = [
                ['mutton', 'enchanted mutton', 'enchanted cooked mutton'],
                ['white wool', 'enchanted wool', '']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                1, 1
            ]
        ))
    return minions

def rabbit():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,20,20,17,17,13,10]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Rabbit',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [1, 1, 1],
            enchat_at = [
                [160, 0],
                [160, 0],
                [576, 0]
            ],
            items_producibles = [
                ['rabbit', 'enchanted rabbit', ''],
                ['rabbit foot', 'enchanted rabbit foot', ''],
                ['rabbit hide', 'enchanted rabbit hide', '']
            ],
            productos_diferentes = 3,
            porcentaje_por_item = [
                1, 0.35, 0.35
            ]
        ))
    return minions

def nether_wart():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [50,50,47,47,44,44,41,41,38,38,32,27]
    minions = []
    for i in range(1, 13):
        minions.append(Minion(
            name = 'Nether Wart',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 3,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'nether stalk',
                'Enchanted nether stalk',
                'mutant nether stalk'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions
