import math

width = 1200
height = 800
fps = 60
tile = 100
fps_pos = (width - 65, 5)

minimap_scale = 5
minimap_res = (width // minimap_scale - 70, height // minimap_scale)
map_scale = 2 * minimap_scale
map_tile = tile // map_scale
map_position = (0, height - height // minimap_scale - 640)

field_of_view = math.pi / 3
count_of_rays = 300
max_depth = 800
delta_angle = field_of_view / count_of_rays
distantion = count_of_rays / (2 * math.tan((field_of_view / 2)))
proj_coeff = 3 * distantion * tile
scale = width // count_of_rays

double_pi = math.pi * 2
center_of_ray = count_of_rays // 2 - 1
fake_rays = 100
fake_rays_range = count_of_rays - 1 + 2 * fake_rays

width_of_textures = 1200
heigth_of_textures = 1200
scale_texture = width_of_textures // tile

player_position = ((width // 2) // 4, (height // 2) - 50)
player_angle = 0
player_speed = 3
