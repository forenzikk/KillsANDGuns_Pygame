import pygame
from parametres import *
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'bochka': {
                'sprite': pygame.image.load('sprites/bochka/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': 0.4,
                'animation': deque(
                    [pygame.image.load(f'sprites/bochka/{i}.png').convert_alpha() for i in range(12)]),
                'animation_dist': 800,
                'animation_speed': 10,
            },
            'pumpkin': {
                'sprite': pygame.image.load('sprites/creepy_pumpkin/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': 0.6,
                'animation': deque([pygame.image.load(f'sprites/creepy_pumpkin/{i}.png').convert_alpha() for i in range(8)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'death': {
                'sprite': [pygame.image.load(f'sprites/death/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pygame.image.load(f'sprites/death/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10,
                'blocked': True,
            },
            'fire': {
                'sprite': pygame.image.load('sprites/fire/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque(
                    [pygame.image.load(f'sprites/fire/{i}.png').convert_alpha() for i in range(16)]),
                'animation_dist': 800,
                'animation_speed': 5,
                'blocked': None,
            },
        }

        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['bochka'], (7.1, 2.1)),
            SpriteObject(self.sprite_parameters['bochka'], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters['pumpkin'], (8.7, 2.5)),
            SpriteObject(self.sprite_parameters['death'], (7, 4)),
            SpriteObject(self.sprite_parameters['fire'], (8.6, 5.6))
        ]


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.pos = self.x, self.y = pos[0] * tile, pos[1] * tile
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi

        delta_rays = int(gamma / delta_angle)
        current_ray = center_of_ray + delta_rays
        distance_to_sprite *= math.cos((field_of_wiev / 2) - current_ray * delta_angle)

        fake_ray = current_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and distance_to_sprite > 30:
            proj_height = min(int(project_coeff / distance_to_sprite * self.scale), height * 2)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            #sprite for angle
            if self.viewing_angles:
                if theta < 0:
                    theta += double_pi
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            #animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            #scales and positions
            sprite_pos = (current_ray * scale - half_proj_height, (height // 2) - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)