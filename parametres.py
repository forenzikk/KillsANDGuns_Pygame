import math

width = 1200
height = 800
fps = 60
tile = 100
fps_pos = (width - 65, 5)

player_pos = ((width // 2) // 4, (height // 2) - 50)
player_angle = 0
player_speed = 2

field_of_wiev = math.pi / 3
count_of_rays = 300
max_depth = 1000
delta_angle = field_of_wiev / count_of_rays
distantion = count_of_rays / (2 * math.tan((field_of_wiev / 2)))
project_coeff = 3 * distantion * tile
scale = width // count_of_rays

minimap_scale = 5
minimap_res = (width // minimap_scale - 70, height // minimap_scale)
map_scale = 2 * minimap_scale
map_tile = tile // map_scale
map_pos = (0, height - height // minimap_scale - 640)

double_pi = math.pi * 2
texture_width = 1200
texture_height = 1200
texture_scale = texture_width // tile

center_of_ray = count_of_rays // 2 - 1
fake_rays = 100
fake_rays_range = count_of_rays - 1 + 2 * fake_rays
