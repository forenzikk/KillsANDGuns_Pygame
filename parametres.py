import math

width = 1200
height = 800
fps = 60
tile = 100

player_pos = ((width // 2), (height // 2))
angle_of_player = 0
speed_of_player = 2

field_of_wiev = math.pi / 3
count_of_rays = 120
max_depth = 2200
delta_angle = field_of_wiev / count_of_rays
distantion = count_of_rays / (2 * math.tan(field_of_wiev / 2))
project_coeff = 3 * distantion * tile
scale = width // count_of_rays
