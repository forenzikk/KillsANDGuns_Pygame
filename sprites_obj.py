import pygame
from parametres import *


class sprites:
    def __init__(self):
        self.sprite_types = {
            'bochka': pygame.image.load('sprites/bochka/bochka.png').convert_alpha(),
            'slizen': pygame.image.load('sprites/slizen/0.png').convert_alpha(),
            'slizen2': pygame.image.load('sprites/slizen/1.png').convert_alpha(),
            'death': pygame.image.load(f'sprites/death/0.png').convert_alpha(),
            'enemy': pygame.image.load(f'sprites/enemy/0.png').convert_alpha()
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['bochka'], True, (7.1, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['bochka'], True, (5.9, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['bochka'], True, (8.1, 3.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['bochka'], True, (6.1, 1.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['bochka'], True, (6.1, 4.1), 1.8, 0.4),

            SpriteObject(self.sprite_types['slizen'], True, (15.1, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['slizen'], True, (4.9, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['slizen'], True, (2.1, 3.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['slizen2'], True, (4.1, 4.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['slizen2'], True, (6.1, 3.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['slizen2'], True, (7.1, -1.1), 1.8, 0.4),

            SpriteObject(self.sprite_types['death'], True, (7, 4), -0.2, 0.7),
            SpriteObject(self.sprite_types['enemy'], True, (7, 6), -0.2, 0.7)
        ]


class SpriteObject:
    def __init__(self, object, static, position, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = position[0] * tile, position[1] * tile
        self.shift = shift
        self.scale = scale

        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for i in range(fake_rays)]
        fake_walls1 = [walls[-1] for i in range(fake_rays)]
        fake_walls = fake_walls0 + walls + fake_walls1

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
        if 0 <= fake_ray <= count_of_rays - 1 + 2 * fake_rays and distance_to_sprite < fake_walls[fake_ray][0]:
            proj_height = min(int(project_coeff / distance_to_sprite * self.scale), 2 * height)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.static:
                if theta < 0:
                    theta += double_pi
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_positions = (current_ray * scale - half_proj_height, (height // 2) - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_positions)
        else:
            return (False,)
