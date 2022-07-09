from minions.base_minion import Minion

def zombie():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,20,20,17,17,13]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Zombie',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'rotten flesh',
                'Enchanted rotten flesh',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                0.93
            ]
        ))
    return minions

def skeleton():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,20,20,17,17,13]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Skeleton',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'bone',
                'Enchanted bone',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def spider():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,20,20,17,17,13]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Spider',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [1, 1],
            enchat_at = [
                [192, 0],
                [160, 0]
            ],
            items_producibles = [
                ['string', 'enchanted string', ''],
                ['spider eye', 'enchanted spider eye', '']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                1, 0.5
            ],
            diamond = False
        ))
    return minions

def cave():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,20,20,17,17,13]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Cave Spider',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = [1, 1],
            enchat_at = [
                [192, 0],
                [160, 0]
            ],
            items_producibles = [
                ['string', 'enchanted string', ''],
                ['spider eye', 'enchanted spider eye', '']
            ],
            productos_diferentes = 2,
            porcentaje_por_item = [
                0.5, 1
            ],
            diamond = False
        ))
    return minions

def creeper():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [27,27,25,25,23,23,21,21,18,18,14]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Creeper',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'gunpowder',
                'Enchanted gunpowder',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def enderman():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [32,32,30,30,28,28,25,25,22,22,18]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Enderman',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                20, 80
            ],
            items_producibles = [
                'ender pearl',
                'Enchanted ender pearl',
                'Absolute ender pearl'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def ghast():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [50,50,47,47,44,44,41,41,38,38,32]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Ghast',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                5, 0
            ],
            items_producibles = [
                'ghast tear',
                'Enchanted ghast tear',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def slime():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [26,26,24,24,22,22,19,19,16,16,12]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Slime',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1.8,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'slime ball',
                'Enchanted slime ball',
                'enchanted slime block'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def blaze():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [33,33,31,31,28.5,28.5,25,25,21,21,16.5]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Blaze',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1,
            enchat_at = [
                160, 160
            ],
            items_producibles = [
                'blazce rod',
                'Enchanted blaze powder',
                'Enchanted blaze rod'
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

def magma():
    #(self, name, nivel, delay, drops_per_action, enchat_at, items_producibles, diamond=True, productos_diferentes=1, porcentaje_por_item=[])
    delays = [32,32,20,20,28,28,25,25,22,22,18]
    minions = []
    for i in range(1, len(delays) + 1):
        minions.append(Minion(
            name = 'Magma Cube',
            nivel = i,
            delay = delays[i-1],
            drops_per_action = 1.8,
            enchat_at = [
                160, 0
            ],
            items_producibles = [
                'magma cream',
                'Enchanted magma cream',
                ''
            ],
            productos_diferentes = 1,
            porcentaje_por_item = [
                1
            ]
        ))
    return minions

