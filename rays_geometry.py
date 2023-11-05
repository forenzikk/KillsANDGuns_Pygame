import pygame
from parametres import *
from play_map import world_map


def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile


def ray_casting(player, textures):
    walls = []
    xo, yo = player.get_position
    xn, yn = mapping(xo, yo)
    cur_angle = player.angle - (field_of_wiev / 2)
    for ray in range(count_of_rays):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        if sin_a:
            sin_a = sin_a
        else:
            sin_a = 0.000001

        if cos_a:
            cos_a = cos_a
        else:
            cos_a = 0.000001

        # verticals
        if cos_a >= 0:
            x, dx = (xn + tile, 1)
        else:
            x, dx = (xn, -1)

        for i in range(0, width, tile):
            depth_vertical = (x - xo) / cos_a
            yv = yo + depth_vertical * sin_a
            tile_vertical = mapping(x + dx, yv)
            if tile_vertical in world_map:
                texture_vertical = world_map[tile_vertical]
                break
            x += dx * tile

        # horizontals
        if sin_a >= 0:
            y, dy = (yn + tile, 1)
        else:
            y, dy = (yn, -1)

        for i in range(0, height, tile):
            depth_horisontal = (y - yo) / sin_a
            xh = xo + depth_horisontal * cos_a
            tile_horisontal = mapping(xh, y + dy)
            if tile_horisontal in world_map:
                texture_horisontal = world_map[tile_horisontal]
                break
            y += dy * tile

        # projection
        if depth_vertical < depth_horisontal:
            depth, offset, texture = (depth_vertical, yv, texture_vertical)
        else:
            depth, offset, texture = (depth_horisontal, xh, texture_horisontal)

        offset = int(offset) % tile
        depth *= math.cos(player.angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = min(int(project_coeff / depth), 2 * height)

        wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, height_of_textures)
        wall_column = pygame.transform.scale(wall_column, (scale, proj_height))
        wall_pos = (ray * scale, (height // 2) - proj_height // 2)

        walls.append((depth, wall_column, wall_pos))
        cur_angle += delta_angle
    return walls
