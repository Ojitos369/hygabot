from minions.base_minion import Minion

def revenant():
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

def tarantula():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [29,29,26,26,23,23,19,19,14.5,14.5,10]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Tarantula',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [3.16, 1, 1],
            enchat_at = [
                [192, 0],
                [160, 0],
                [160, 160]
            ],
            items_producibles = [
                ['string', 'enchanted string', ''],
                ['spider eye', 'enchanted spider eye', ''],
                ['iron ingot', 'enchanted iron', 'enchated iron block']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                1, 1, .2
            ]
        ))
    return minions

def voidling():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [45,45,42,42,39,39,35,35,30,30,24]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Voidling',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [2.42, 1],
            enchat_at = [
                [160, 0],
                [160, 160]
            ],
            items_producibles = [
                ['obsidian', 'enchanted obsidian', ''],
                ['quartz', 'enchanted quartz', 'enchanted quartz block']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                1, .4
            ],
            diamond = False
        ))
    return minions