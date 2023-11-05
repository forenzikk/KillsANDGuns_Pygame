from parametres import *

text_map = [
    '111111111111',
    '1......1...1',
    '1..111...1.1',
    '1....1..11.1',
    '1..2....1..1',
    '1..2...111.1',
    '1....1.....1',
    '1111111111111'
]

world_map = {}
minimap = set()
for i, row in enumerate(text_map):
    for j, symbol in enumerate(row):
        if symbol != '.':
            minimap.add((j * map_tile, i * map_tile))
            if symbol == '1':
                world_map[(j * tile, i * tile)] = '1'
            elif symbol == '2':
                world_map[(j * tile, i * tile)] = '2'