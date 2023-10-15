from parametres import *
import sys
import pygame

text_map = [                                #текстовый вид нашей карты (вид сверху)
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X...XXXX........XXXXX.......X',
    'X....X.....XXX..X.......X...X',
    'X.......XX...X..X..XX.......X',
    'XXXX............XXXX.....XXXX',
    'X......XX..XXXXX.....X......X',
    'X....X...XXX......X.....XX..X',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

world_map = set()                       #задаем координаты и выстраиваем стены на карте
for i, row in enumerate(text_map):
    for j, symbol in enumerate(row):
        if symbol == 'X':
            world_map.add((j * tile, i * tile))