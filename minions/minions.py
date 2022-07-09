from minions.farming import *
from minions.mining import *
from minions.combat import *
from minions.slayers import *
from minions.foragin import *

def crear_minions(slayer = True):
    minions = []

    # ----- Farming minions -----
    wheat_minions = wheat()
    carrot_minions = carrot()
    potato_minions = potato()
    pumpkin_minions = pumpkin()
    melon_minions = melon()
    mushroom_minions = mushroom()
    cocoa_minions = cocoa()
    cactus_minions = cactus()
    sugar_minions = sugar()
    cow_minions = cow()
    pig_minions = pig()
    chicken_minions = chicken()
    sheep_minions = sheep()
    rabbit_minions = rabbit()
    nether_wart_minions = nether_wart()

    minions.append(wheat_minions)
    minions.append(carrot_minions)
    minions.append(potato_minions)
    minions.append(pumpkin_minions)
    minions.append(melon_minions)
    minions.append(mushroom_minions)
    minions.append(cocoa_minions)
    minions.append(cactus_minions)
    minions.append(sugar_minions)
    minions.append(cow_minions)
    minions.append(pig_minions)
    minions.append(chicken_minions)
    minions.append(sheep_minions)
    minions.append(rabbit_minions)
    minions.append(nether_wart_minions)


    # ----- Mining minions -----
    cobblestone_minions = cobblestone()
    coal_minions = coal()
    iron_minions = iron()
    gold_minions = gold()
    diamond_minions = diamond()
    lapis_minions = lapis()
    emerald_minions = emerald()
    redstone_minions = redstone()
    quartz_minions = quartz()
    glowstone_minions = glowstone()
    flint_minions = flint()
    ice_minions = ice()
    sand_minions = sand()
    endstone_minions = endstone()
    clay_minions = clay()
    snow_minions = snow()
    mithril_minions = mithril()

    minions.append(cobblestone_minions)
    minions.append(coal_minions)
    minions.append(iron_minions)
    minions.append(gold_minions)
    minions.append(diamond_minions)
    minions.append(lapis_minions)
    minions.append(emerald_minions)
    minions.append(redstone_minions)
    minions.append(quartz_minions)
    minions.append(glowstone_minions)
    minions.append(flint_minions)
    minions.append(ice_minions)
    minions.append(sand_minions)
    minions.append(endstone_minions)
    minions.append(clay_minions)
    minions.append(snow_minions)
    minions.append(mithril_minions)


    # ----- Combat minions -----
    zombie_minion = zombie()
    skeleton_minion = skeleton()
    spider_minion = spider()
    cave_minion = cave()
    creeper_minion = creeper()
    enderman_minion = enderman()
    ghast_minion = ghast()
    slime_minion = slime()
    blaze_minion = blaze()
    magma_minion = magma()

    minions.append(zombie_minion)
    minions.append(skeleton_minion)
    minions.append(spider_minion)
    minions.append(cave_minion)
    minions.append(creeper_minion)
    minions.append(enderman_minion)
    minions.append(ghast_minion)
    minions.append(slime_minion)
    minions.append(blaze_minion)
    minions.append(magma_minion)

    
    # ----- Slayers -----
    if slayer:
        revenant_minions = revenant()
        tarantula_minions = tarantula()
        voidling_minions = voidling()

        minions.append(revenant_minions)
        minions.append(tarantula_minions)
        minions.append(voidling_minions)
    
    # ----- Foragin minions -----
    oak_minions = oak()
    spruce_minions = spruce()
    birch_minions = birch()
    dark_oak_minions = dark_oak()
    acacia_minions = acacia()
    jungle_minions = jungle()
    #fishing_minions = fishing()

    minions.append(oak_minions)
    minions.append(spruce_minions)
    minions.append(birch_minions)
    minions.append(dark_oak_minions)
    minions.append(acacia_minions)
    minions.append(jungle_minions)
    #minions.append(fishing_minions)

    return minions