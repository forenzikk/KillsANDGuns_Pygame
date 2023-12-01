from parametres import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

o = False
matrix1 = [

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
    [1, o, o, o, o, o, o, o, o, o, 2, o, o, o, o, o, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

]


width_of_world = len(matrix1[0]) * tile#переменные для правильного вычисления луча в rays_geometry
height_of_world = len(matrix1) * tile
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
collision_walls = []#экземляр класса Rect
for j, row in enumerate(matrix1):#координаты строк - x, координаты списка - у
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * map_tile, j * map_tile))#заносим в множество только стены
            collision_walls.append(pygame.Rect(i * tile, j * tile, tile, tile))#квадрат со стороной размера нашей стены
            if char == 1:
                world_map[(i * tile, j * tile)] = 1
            elif char == 2:
                world_map[(i * tile, j * tile)] = 2
