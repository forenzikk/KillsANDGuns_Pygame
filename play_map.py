from parametres import *

"""text_map = [                                #текстовый вид нашей карты (вид сверху)
    'XXXXXXXXXXXX',
    'X......XX..X',
    'X..XXX...X.X',
    'X....X..XX.X',
    'X...X...X..X',
    'X..X...XXX.X',
    'XX...X..X..X',
    'XXXXXXXXXXXX'
]"""
text_map = [
    'XXXXXXXXXXXXXXXXXX',
    'X......XXX.......X',
    'X...XX......XXXX.X',
    'X...X...XX.......X',
    'X......XX.....XXXX',
    'X.XXX.....XXX....X',
    'X......X.....XX..X',
    'XXXXXXXXXXXXXXXXXX'
]

world_map = set()                       #задаем координаты и выстраиваем стены на карте
minimap = set()#мини-карта
for i, row in enumerate(text_map):
    for j, symbol in enumerate(row):
        if symbol == 'X':
            world_map.add((j * tile, i * tile))
            minimap.add((i * map_tile, j * map_tile))