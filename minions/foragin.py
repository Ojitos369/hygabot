from minions.base_minion import Minion

def oak():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [48,48,45,45,42,42,38,38,33,33,27]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Oak',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'log',
                'Enchanted oak log',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def spruce():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [48,48,45,45,42,42,38,38,33,33,27]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Spruce',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'log:1',
                'Enchanted spruce log',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def birch():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [48,48,45,45,42,42,38,38,33,33,27]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Birch',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'log:2',
                'Enchanted birch log',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def dark_oak():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [48,48,45,45,42,42,38,38,33,33,27]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Dark Oak',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'log_2:1',
                'Enchanted dark oak log',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def acacia():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [48,48,45,45,42,42,38,38,33,33,27]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Acacia',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'log_2',
                'Enchanted acacia log',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def jungle():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [48,48,45,45,42,42,38,38,33,33,27]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Jungle',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 4,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'log_2',
                'Enchanted jungle log',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def fishing():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [29,29,26,26,23,23,19,19,14.5,14.5,10,8]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Revenant',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [3, 1],
            enchat_at = [
                [160, 0],
                [160, 160]
            ],
            items_producibles = [
                ['rotten flesh', 'enchanted rotten flesh', ''],
                ['diamond', 'enchanted diamond', 'enchanted diamond block']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                1, .2
            ]
        ))
    return minions