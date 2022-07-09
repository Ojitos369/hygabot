from minions.base_minion import Minion

def cobblestone():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [14,14,12,12,10,10,9,9,8,8,7,6]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Cobblestone',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'cobblestone',
                'Enchanted cobblestone',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def coal():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [15,15,13,13,12,12,1,10,9,9,7,6]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Coal',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'coal',
                'Enchanted coal',
                'Enchanted coal block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def iron():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [17,17,15,15,14,14,12,12,10,10,8,7]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Iron',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'iron ingot',
                'Enchanted iron',
                'Enchanted iron block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def gold():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [22,22,20,20,18,18,16,16,14,14,11,9]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Gold',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'Gold ingot',
                'Enchanted Gold',
                'Enchanted Gold block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def diamond():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [29,29,27,27,25,25,22,22,19,19,15,12]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Diamond',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'diamond',
                'Enchanted diamond',
                'Enchanted diamond block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ],
            diamond = False
        ))
    return minions

def lapis():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [17,17,15,15,14,14,12,12,10,10,8,7]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Lapis',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 6,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'ink sack:4',
                'Enchanted lapis lazuli',
                'Enchanted lapis lazuli block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def emerald():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [28,28,26,26,24,24,21,21,18,18,14,12]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Emerald',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'emerald',
                'Enchanted emerald',
                'Enchanted emerald block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def lapis():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [17,17,15,15,14,14,12,12,10,10,8,7]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Lapis',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 6,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'ink sack:4',
                'Enchanted lapis lazuli',
                'Enchanted lapis lazuli block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def redstone():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [29,29,27,27,25,25,23,23,21,21,18,16]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Redstone',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4.5,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'redstone',
                'Enchanted redstone',
                'Enchanted redstone block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def lapis():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [17,17,15,15,14,14,12,12,10,10,8,7]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Lapis',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 6,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'ink sack:4',
                'Enchanted lapis lazuli',
                'Enchanted lapis lazuli block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def quartz():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [22.5,22.5,21,21,19,19,17,17,14.5,14.5,11.5]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Quartz',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'quartz',
                'Enchanted quartz',
                'Enchanted quartz block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def lapis():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [17,17,15,15,14,14,12,12,10,10,8,7]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Lapis',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 6,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'ink sack:4',
                'Enchanted lapis lazuli',
                'Enchanted lapis lazuli block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def obsidian():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [45,45,42,42,39,39,35,35,30,24,21]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Obsidian',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'obsidian',
                'Enchanted obsidian',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def lapis():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [17,17,15,15,14,14,12,12,10,10,8,7]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Lapis',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 6,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'ink sack:4',
                'Enchanted lapis lazuli',
                'Enchanted lapis lazuli block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def glowstone():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [25,25,23,23,21,21,19,19,16,16,13]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Glowstone',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 3,
            enchat_at = [
                160, 192
            ],
            items_producibles = [
                'GLOWSTONE DUST',
                'Enchanted GLOWSTONE DUST',
                'Enchanted GLOWSTONE'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def flint():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,19,19,16,16,13]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Flint',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'flint',
                'Enchanted flint',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ],
            diamond = False
        ))
    return minions

def ice():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [14,14,12,12,10,10,9,9,8,8,7]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Ice',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'ice',
                'Enchanted ice',
                'Enchanted packed ice'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def sand():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,19,19,16,16,13]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Sand',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'sand',
                'Enchanted sand',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def endstone():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,19,19,16,16,13]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'End Stone',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'ender stone',
                'Enchanted endstone',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def clay():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [32,32,30,30,27.5,27.5,24,24,20,20,16]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Clay',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'clay ball',
                'Enchanted clay ball',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def snow():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [13,13,12,12,11,11,9.5,9.5,8,8,6.5]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Snow',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                640, 0
            ],
            items_producibles = [
                'snow ball',
                'Enchanted snow block',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions


def mithril():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [80,80,75,75,70,70,65,65,60,60,55,50]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Clay',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'mithril ore',
                'Enchanted mithril',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions