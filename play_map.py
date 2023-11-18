from parametres import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

o = False
matrix_map = [

    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, o, o, o, o, o, 2, o, o, o, o, o, o, o, o, o, 1],
    [1, o, 2, 2, 2, o, o, o, o, 2, 2, 2, o, o, o, 2, 1],
    [1, o, 2, 2, 2, o, o, o, o, o, o, 2, 2, o, o, o, 1],
    [1, o, 2, 2, 2, o, o, o, o, o, o, o, 2, o, 2, o, 1],
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
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * map_tile, j * map_tile))
            collision_walls.append(pygame.Rect(i * tile, j * tile, tile, tile))
            if char == 1:
                world_map[(i * tile, j * tile)] = 1
            elif char == 2:
                world_map[(i * tile, j * tile)] = 2
