import math

width = 1200
height = 800
fps = 60
fps_position = (width - 60, 5)
tile = 100

player_position = ((width // 2), (height // 2))
angle_of_player = 0
speed_of_player = 2

field_of_wiev = math.pi / 3
count_of_rays = 120
max_depth = 2200
delta_angle = field_of_wiev / count_of_rays
distantion = count_of_rays / (2 * math.tan(field_of_wiev / 2))
project_coeff = 3 * distantion * tile
scale = width // count_of_rays

map_scale = 5
map_tile = tile // map_scale
map_position = (0, height - height // map_scale - 640)

width_of_textures = 1200
height_of_textures = 1200
texture_scale = width_of_textures // tile
