from parametres import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

o = False
matrix_map = [

    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, o, o, o, o, o, 2, o, o, o, o, o, o, o, o, o, 1],
    [1, o, 2, 2, o, o, o, o, o, 2, 2, 2, o, o, o, 2, 1],
    [1, o, o, o, o, o, o, o, o, o, o, 2, 2, o, o, o, 1],
    [1, o, 2, 2, o, o, o, o, o, o, o, o, 2, o, 2, o, 1],
    [1, o, o, o, o, o, 2, o, o, 2, 2, o, 2, o, o, o, 1],
    [1, o, 2, o, o, o, 2, o, o, 2, o, o, 2, o, o, o, 1],
    [1, o, o, 2, o, o, 2, o, o, o, o, o, o, o, o, o, 1],
    [1, o, 2, o, o, o, o, o, o, o, 2, o, o, 2, 2, o, 1],
    [1, o, 2, o, o, o, 2, 2, o, 2, o, o, o, 2, 2, o, 1],
    [1, o, o, o, o, 2, o, 2, o, o, 2, o, o, o, o, o, 1],
    [1, o, 2, o, 2, o, o, o, o, 2, o, o, 2, o, o, o, 1],
    [1, o, o, o, o, o, 2, o, o, o, o, o, 2, 2, o, o, 1],
    [1, o, 2, 2, 2, o, o, o, 2, o, o, o, o, 2, 2, 2, 1],
    [1, o, o, o, o, o, o, o, o, o, 4, o, o, o, o, o, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

]

width_of_world = len(matrix_map[0]) * tile
height_of_world = len(matrix_map) * tile
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
collision_walls = []
for i, line in enumerate(matrix_map):
    for j, symbol in enumerate(line):
        if symbol:
            mini_map.add((j * map_tile, i * map_tile))
            collision_walls.append(pygame.Rect(j * tile, i * tile, tile, tile))
            if symbol == 1:
                world_map[(j * tile, i * tile)] = 1
            elif symbol == 2:
                world_map[(j * tile, i * tile)] = 2
