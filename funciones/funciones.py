# importando basic, inventarios, help, wardrobe, ender_chest, backpack, bazar, minions, buscar_inv, ah_player, slayers, recomendaciones, novedades, emojis, buscar_guild, pets, talismanes, pruebas, escencias, hotm, forge, claim
from funciones.basic import Basicos
from funciones.inventarios import Inventarios
from funciones.help import Help
from funciones.wardrobe import Wardrobe
from funciones.ender_chest import Ender
from funciones.backpack import Backpack
from funciones.bazar import Bazar
from funciones.minions import Minions
from funciones.buscar_inv import Busqueda
from funciones.ah_player import Ah_player
from funciones.slayers import Slayer_player
from funciones.recomendaciones import Recomendaciones
from funciones.novedades import Novedades
from funciones.emojis import Emojis
from funciones.buscar_guild import Bu_guild
from funciones.pets import Pets
from funciones.talismanes import Talismanes
from funciones.pruebas import Pruebas
from funciones.escencias import Escencias
from funciones.hotm import Hotm
from funciones.forge import Forge
from funciones.claim import Claim
from funciones.query import Query
from funciones.personal import Personal

def importar_funciones():
    basic = Basicos()
    inventario = Inventarios()
    help = Help()
    wardrobe = Wardrobe()
    ender = Ender()
    backpack = Backpack()
    bazar = Bazar()
    minions = Minions()
    buscar = Busqueda()
    ah_player = Ah_player()
    slayers = Slayer_player()
    recomendaciones = Recomendaciones()
    novedades = Novedades()
    emojis = Emojis()
    bu_guild = Bu_guild()
    pets = Pets()
    talismanes = Talismanes()
    pruebas = Pruebas()
    escencias = Escencias()
    hotm = Hotm()
    forge = Forge()
    claim = Claim()
    query = Query()
    personal = Personal()

    funciones_totales = [
        basic,
        inventario,
        wardrobe,
        ender,
        backpack,
        bazar,
        minions,
        buscar,
        ah_player,
        recomendaciones,
        novedades,
        emojis,
        bu_guild,
        pets,
        talismanes,
        pruebas,
        escencias,
        hotm,
        forge,
        claim,
        query,
        personal
    ]
    return funciones_totales