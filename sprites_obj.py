import pygame
from parametres import *
from collections import deque
from rays_geometry import *
from numba.core import types
from numba.typed import Dict
from numba import int32

class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'bochka': {
                'sprite': pygame.image.load('sprites/bochka/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': (0.4, 0.4),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'sprites/bochka/{i}.png').convert_alpha() for i in range(12)]),
                'death_animation': deque([pygame.image.load(f'sprites/bochka/{i}.png')
                                          .convert_alpha() for i in range(4)]),
                'is_dead': None,
                'dead_shift': 2.6,
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'obj_action': []
            },
            'pumpkin': {
                'sprite': pygame.image.load(f'sprites/creepy_pumpkin/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': (0.6, 0.6),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/soldier0/death/{i}.png')
                                           .convert_alpha() for i in range(2, 6)]),
                'is_dead': None,
                'dead_shift': 0.6,
                'animation_dist': None,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque(
                    [pygame.image.load(f'sprites/creepy_pumpkin/{i}.png').convert_alpha() for i in range(7)]),
            },
            'death': {
                'sprite': [pygame.image.load(f'sprites/death/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.0,
                'scale': (1.1, 1.1),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/soldier0/death/{i}.png')
                                           .convert_alpha() for i in range(2, 6)]),
                'is_dead': None,
                'dead_shift': 0.6,
                'animation_dist': None,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque(
                    [pygame.image.load(f'sprites/death/{i}.png').convert_alpha() for i in range(9)]),
            },
            'enemy1': {
                'sprite': [pygame.image.load(f'sprites/npc/soldier0/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/soldier0/death/{i}.png')
                                         .convert_alpha() for i in range(10)]),
                'is_dead': None,
                'dead_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/npc/soldier0/action/{i}.png')
                                    .convert_alpha() for i in range(4)])
            },
        }

        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['bochka'], (7.1, 2.1)),
            SpriteObject(self.sprite_parameters['bochka'], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters['pumpkin'], (8.7, 2.5)),
            SpriteObject(self.sprite_parameters['death'], (7, 4)),
            SpriteObject(self.sprite_parameters['death'], (5.52, 1.7)),
            SpriteObject(self.sprite_parameters['enemy1'], (2.5, 1.5)),
            SpriteObject(self.sprite_parameters['enemy1'], (5.51, 1.5)),
            SpriteObject(self.sprite_parameters['enemy1'], (6.61, 2.92)),
            SpriteObject(self.sprite_parameters['enemy1'], (7.68, 1.47)),
            SpriteObject(self.sprite_parameters['enemy1'], (8.75, 3.65)),
            SpriteObject(self.sprite_parameters['enemy1'], (1.27, 11.5)),
            SpriteObject(self.sprite_parameters['enemy1'], (1.26, 8.29)),
        ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))

    @property
    def blocked_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in self.list_of_objects:
            if obj.flag in {'door_h', 'door_v'} and obj.blocked:
                i, j = mapping(obj.x, obj.y)
                blocked_doors[(i, j)] = 0
        return blocked_doors


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()

        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']

        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * tile, pos[1] * tile
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        #self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False
        if self.viewing_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    @property
    def is_on_fire(self):
        if center_of_ray - self.side // 2 < self.current_ray < center_of_ray + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def get_position(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / delta_angle)
        self.current_ray = center_of_ray + delta_rays

        fake_ray = self.current_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and self.distance_to_sprite > 30:
            self.proj_height = min(int(proj_coeff / self.distance_to_sprite), height)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            if self.is_dead and self.is_dead != 'immortal':
                sprite_object = self.dead_animation()
                shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1.3)
            elif self.npc_action_trigger:
                sprite_object = self.npc_in_action()
            else:
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()


            # sprite scale and positions
            sprite_position = (self.current_ray * scale - half_sprite_width, (height // 2) - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return (self.distance_to_sprite, sprite, sprite_position)
        else:
            return (False,)

    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += double_pi
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0

        return self.dead_sprite

    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object
