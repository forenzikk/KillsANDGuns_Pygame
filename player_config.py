import pygame, time
from play_map import *
from drawings import *


class Player:
    def __init__(self, sprites):
        self.x, self.y = player_position
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.004  # чувствительность
        # Параметры коллизий
        self.side = 50  # размер стороны квадрата, который будет игроком вместо точки
        self.rect = pygame.Rect(*player_position, self.side, self.side)
        # gun
        self.shot = False
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()

    @property
    def get_position(self):
        return (self.x, self.y)

    # перенос списка всех коллизий в отдельное св-во (стены + спрайты)
    @property
    def collision_list(self):
        return collision_walls + [
            pygame.Rect(
                *obj.get_position,
                obj.side,
                obj.side) for obj in self.sprites.list_of_objects if obj.blocked]

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()  # копия текущего положения
        next_rect.move_ip(dx, dy)  # переместим на dx, dy
        # индекс стен с которыми столкнулся игрок (относительно)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):  # в зависимости от столкновения ищем сторону, с которой столкнулись
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:  # уперлись в угол
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False

                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            text_font = pygame.font.Font('font/font.ttf', 62)
            pause_text_1 = text_font.render("Режим паузы", 1, pygame.Color('white'))
            pause_text_2 = text_font.render("Жми 'c', чтобы продолжить", 1, pygame.Color('white'))
            text = pygame.Rect(0, 0, 400, 150)
            text.center = 600, 700
            self.screen.blit(pause_text_1, (text.centery - 320, text.centery - 500))
            self.screen.blit(pause_text_2, (text.centery - 580, text.centery - 400))

            pygame.display.update()
            self.clock.tick(5)

    def movement(self):
        self.keys_control()
        self.mouse_control()
        # перемещение квадрата, за который выступает игрок
        self.rect.center = self.x, self.y
        self.angle %= (math.pi * 2)  # угол направления игрока

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)  # разрешение движения
        if keys[pygame.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_p]:
            self.pause()

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True

    def mouse_control(self):
        if pygame.mouse.get_focused():
            # разница координат курсора и середины окна
            difference = pygame.mouse.get_pos()[0] - 600
            # переносим указатель в центр
            pygame.mouse.set_pos((600, 400))
            # прибавляем к нему ту самую разницу + учет чувствительности
            self.angle += difference * self.sensitivity
