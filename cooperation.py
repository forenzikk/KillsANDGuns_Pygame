from parametres import *
from player_config import *
from rays_geometry import *
from play_map import *
import math
import pygame
from numba import njit

@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_x, npc_y, blocked_doors, world_map, player_position):
    ox, oy = player_position
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    current_angle = math.atan2(delta_y, delta_x)
    current_angle += math.pi

    sin_a = math.sin(current_angle)
    if sin_a:
        sin_a = sin_a
    else:
        sin_a = 0.000001

    cos_a = math.cos(current_angle)

    if cos_a:
        cos_a = cos_a
    else:
        cos_a = 0.000001

    # verticals
    if cos_a >= 0:
        x, dx = xm + tile, 1
    else:
        x, dx = xm, -1

    for i in range(0, int(abs(delta_x)) // tile):
        depth_vertical = (x - ox) / cos_a
        yv = oy + depth_vertical * sin_a
        tile_vertical = mapping(x + dx, yv)
        if tile_vertical in world_map or tile_vertical in blocked_doors:
            return False
        x += dx * tile

    # horizontals
    if sin_a >= 0:
        y, dy = ym + tile, 1
    else:
        y, dy = ym, -1

    for i in range(0, int(abs(delta_y)) // tile):
        depth_horisontal = (y - oy) / sin_a
        xh = ox + depth_horisontal * cos_a
        tile_horisontal = mapping(xh, y + dy)
        if tile_horisontal in world_map or tile_horisontal in blocked_doors:
            return False
        y += dy * tile
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.pain_sound = pygame.mixer.Sound('sounds/pain.mp3')

    def interaction_objects(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_casting_npc_player(obj.x, obj.y,
                                                  self.sprites.blocked_doors,
                                                  world_map, self.player.get_position):
                            if obj.flag == 'npc':
                                self.pain_sound.play()
                            obj.is_dead = True
                            obj.blocked = None
                            self.drawing.shot_animation_trigger = False
                    if obj.flag in {'door_h', 'door_v'} and obj.distance_to_sprite < tile:
                        obj.door_open_trigger = True
                        obj.blocked = None
                    break

    def npc_action(self):
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y,
                                          self.sprites.blocked_doors,
                                          world_map, self.player.get_position):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        if abs(obj.distance_to_sprite) > tile:
            dx = obj.x - self.player.get_position[0]
            dy = obj.y - self.player.get_position[1]
            if dx < 0:
                obj.x = obj.x + 1
            else:
                obj.x = obj.x - 1

            if dy < 0:
                obj.y = obj.y + 1
            else:
                obj.y = obj.y - 1

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/background.mp3')
        pygame.mixer.music.play(10)

    def check_win(self):
        if not len([obj for obj in self.sprites.list_of_objects if obj.flag == 'npc' and not obj.is_dead]):
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sounds/winSound.mp3')
            pygame.mixer.music.play()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                self.drawing.win()
