from Tile import Tile
from BaseEntities import *
from Creatures import *
import globals as global_vars


_plants = []
_herbivores = []
_carnivores = []
_entity_dict = {
    "ʷ": Vegetation,
    "ʬ": Vegetation,
    "Y": Vegetation,
    "җ": Herbivore,
    "ԅ": Carnivore,
    "~": Water,
    "∽": Water,
    ":": Beach,
    "_": HorizLimitTop,
    "‾": HorizLimitBottom,
    "|": VertLimit
}


def init_map(map_filename):
    """
    sets up the tile_map and map dimension info as global module vars
    :param map_filename: relative path to the map file
    """
    global _tile_map, _map_width, _map_height
    _tile_map = _parse_map('maps/' + map_filename + '.map')
    _map_width = len(_tile_map[0])
    _map_height = len(_tile_map)


def _parse_map(map_path):
    """
    initialises internal map (2D-list) with tiles and puts initialised entity
    on each tile if there is one on that position.
    :param map_path: relative path to the map file
    :return: tile_map
    """
    tile_map = []

    for y, row in enumerate(open(map_path)):
        tile_map.append([])
        for x, token in enumerate(row.rstrip('\n')):
            tile = Tile(y, x)
            if token != " ":    #empty space is not an entity
                _init_entity(token, tile)
            tile_map[-1].append(tile)

    return tile_map


def _init_entity(token, tile):
    """
    initialises actual entity from the token and adds it to one of the entity
    lists, if it is a creature. the entity will associate itself with the
    given tile
    :param token: textual token representing the entity
    :param tile: the tile to be associated with the entity
    """
    try:
        entity_class = _entity_dict[token]
    except KeyError:
        raise KeyError("your map contains this unexpected token: " + token)

    if entity_class == Carnivore:
        _carnivores.append(entity_class(tile))
    elif entity_class == Herbivore:
        _herbivores.append(entity_class(tile))
    elif entity_class == Vegetation:
        _plants.append(entity_class("ʷʬY".index(token), tile))
    else:   #basic entities don't need to be held in an extra list
        entity_class(tile)


def token_map():
    """
    builds a token map from the tile map
    :return: textual representation of the current map
    """
    return [map(str, row) for row in _tile_map]


def update():
    """
    updates all entities. this is done in three steps. first to act are
    carnivores, second are herbivores and third are plants.
    """
    global_vars.anim_toggler = not global_vars.anim_toggler
    _handle_animal_type(hunter_class=Carnivore, prey_class=Herbivore)
    _handle_animal_type(hunter_class=Herbivore, prey_class=Vegetation)
    _veggie_action()


def _handle_animal_type(hunter_class, prey_class):
    """
    lets all animals of the hunter class act. eaten prey will be removed from
    the corresponding prey list. newborn/starved hunters will be added/removed
    from the corresponding hunter lists.
    :param hunter_class: the hunter class
    :param prey_class: the prey class
    """

    if hunter_class == Carnivore:
        hunter_list, prey_list = _carnivores, _herbivores
    else:
        hunter_list, prey_list = _herbivores, _plants

    born_hunters = []

    for hunter in hunter_list:
        env = _get_env(hunter.pos_y, hunter.pos_x, 1)

        if hunter.life_over():
            hunter_list.remove(hunter.die())

        elif hunter.is_hungry():
            dead_animal = hunter.hunger_game(env)
            if isinstance(dead_animal, prey_class):      #found food
                prey_list.remove(dead_animal)
            elif isinstance(dead_animal, hunter_class):  #starved
                hunter_list.remove(dead_animal)
            else:  #hunter moves if it couldn't find food / didn't starve
                hunter.move(env)

        else:   #hunter tries to reproduce only if it is not hungry
            newborn_hunter = hunter.try_reproduction(env)
            if newborn_hunter:
                born_hunters.append(newborn_hunter)
            else:   #hunter moves if it couldn't find partner
                hunter.move(env)

    hunter_list.extend(born_hunters)


def _veggie_action():
    """
    lets all plants act. new plants (reproduction) will be added to
    the plants list.
    """
    new_plants = []

    for plant in _plants:
        if plant.wants_to_grow():
            grown_plant = plant.try_growth(
                _get_env(plant.pos_y, plant.pos_x, 1)
            )
            if grown_plant:
                new_plants.append(grown_plant)

    _plants.extend(new_plants)


def _get_env(pos_y, pos_x, scope):
    """
    calculates part of map around a specific object with a given range.
    parts that are outside of the map will be filled with tiles holding
    limit placeholder entities.
    :param pos_y: y-coordinate of object in map
    :param pos_x: x-coordinate of object in map
    :param scope: range around object to be returned
    scope = 1 [x][x][x] scope = 2 [x][x][x][x][x]
              [x][o][x]           [x][x][x][x][x]
              [x][x][x]           [x][x][o][x][x]
                                  [x][x][x][x][x]
                                  [x][x][x][x][x]
    :return: part of map as two dimensional list
    """
    env = []

    for offset_y in range(-scope, scope + 1):
        env.append([])
        y_on_map = pos_y + offset_y
        for offset_x in range(-scope, scope + 1):
            x_on_map = pos_x + offset_x
            try:
                env[-1].append(_tile_map[y_on_map][x_on_map])
            except IndexError:
                env[-1].append(Tile(entity=Limit()))

    return env
