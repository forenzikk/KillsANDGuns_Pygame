import levels
from sprites_obj import *
from parametres import *
from random import randrange, randint
from rays_geometry import *
import sys, time, json
from parametres import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

class Drawing:
    def __init__(self, screen, screen_map, player, clock):
        self.screen = screen
        self.screen_map = screen_map
        self.player = player
        self.flag = 0
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.Font('font/font.ttf', 144)
        self.textures = {1: pygame.image.load('images/wall1.png').convert(),
                         2: pygame.image.load('images/wall2.png').convert(),
                         'S': pygame.image.load('images/luna.jpg').convert()
                         }
        # меню
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('images/background.jpg').convert()
        # параметры вооружения
        self.weapon_base_sprite = pygame.image.load('sprites/guns/shotgun/base/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/guns/shotgun/shot/{i}.png').convert_alpha()
                                            for i in range(20)])#класс очереди
        self.weapon_rect = self.weapon_base_sprite.get_rect()#для удобного определения позиции спрайта с оружием
        self.weapon_position = (600 - self.weapon_rect.width // 2, 800 - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 3
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound('sounds/gun.mp3')
        # sfx параметры
        self.sfx = deque([pygame.image.load(f'sprites/guns/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)
        self.screen = pygame.display.set_mode((1200, 800))
        self.font = pygame.font.Font(None, 96)
        self.score = 10000

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % 1200#смещение по текстуре
        self.screen.blit(self.textures['S'], (sky_offset, 0))
        self.screen.blit(self.textures['S'], (sky_offset - 1200, 0))
        self.screen.blit(self.textures['S'], (sky_offset + 1200, 0))
        pygame.draw.rect(self.screen, (20, 20, 20), (0, 400, 1200, 400))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):#отсортировали по глубине
            if obj[0]:
                trash, object, object_position = obj#отсекаем лишние значения для спрайтов
                self.screen.blit(object, object_position)#наносим объекты на главную поверхность

    def mini_map(self, player):
        self.screen_map.fill((0, 0, 0))
        map_x, map_y = player.x // map_scale, player.y // map_scale
        pygame.draw.line(self.screen_map, (220, 220, 0), (map_x, map_y), (map_x + 10 * math.cos(player.angle),
                                                 map_y + 10 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.screen_map, (255, 0, 0), (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.screen_map, (169, 161, 125), (x, y, map_tile, map_tile))
        self.screen.blit(self.screen_map, map_position)

    def player_weapon(self, shots):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
            self.shot_projection = min(shots)[1] // 2#определение кратчайшего расстония до объекта под огнем
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.screen.blit(shot_sprite, self.weapon_position)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.screen.blit(self.weapon_base_sprite, self.weapon_position)

    def draw_score(self):
        substracter = randint(0, 1)
        self.score = self.score - substracter
        record = self.score
        max_score_str = str(self.score)
        render = self.font.render(max_score_str, 0, (255, 255, 255))
        render2 = self.font.render("Your score: ", 0, (255, 255, 255))
        self.screen.blit(render2, (1200 - 580, 5))
        self.screen.blit(render, (1200 - 170, 5))
        return record


    def bullet_sfx(self):#взрыв по объекту центрального луча и вблизи него
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.screen.blit(sfx, (600 - sfx_rect.w // 2, 400 - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def show_win(self):  # отрисовка окончания игры
        render = self.font_win.render('YOU WIN!!!', 1, (randrange(0, 255), 0, 0))
        self.screen.blit(render, (600 - 400, 400))
        pygame.display.flip()
        self.clock.tick(10)

    def menu(self):#архитектура менюшки
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/menu_sound.mp3')
        pygame.mixer.music.play(-1)

        x = 0

        button_font = pygame.font.Font('font/font.ttf', 72)
        label_font = pygame.font.Font('font/font1.otf', 155)
        level1 = button_font.render('LEVEL 1', 1, pygame.Color('white'))
        button_level1 = pygame.Rect(0, 0, 400, 150)
        button_level1.center = 600, (400 - 85)
        level2 = button_font.render('LEVEL 2', 1, pygame.Color('white'))
        button_level2 = pygame.Rect(0, 0, 400, 150)
        button_level2.center = 600, 450
        exit = button_font.render('EXIT', 1, pygame.Color('white'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = 600, 600
        author = button_font.render("Made by Ovannisyan", 1, pygame.Color('white'))
        text_author = pygame.Rect(0, 0, 400, 150)
        text_author.center = 600, 700


        while self.menu_trigger:#отрисовка экрана перед игрой
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menu_picture, (0, 0), (x % 1200, 400, 1200, 800))
            x += 1

            pygame.draw.rect(self.screen, (0, 0, 0), button_level1, border_radius=25, width=10)#LEVEL1
            self.screen.blit(level1, (button_level1.centerx - 150, button_level1.centery - 70))

            pygame.draw.rect(self.screen, (0, 0, 0), button_level2, border_radius=25, width=10)#LEVEL2
            self.screen.blit(level2, (button_level2.centerx - 150, button_level2.centery - 50))

            pygame.draw.rect(self.screen, (0, 0, 0), button_exit, border_radius=25, width=10)#EXIT
            self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            pygame.draw.rect(self.screen, (0, 0, 0), text_author, border_radius=25, width=10)#AUTHOR
            self.screen.blit(author, (text_author.centery - 520, text_author.centery - 20))

            label = label_font.render('KILLS and GUNS', 1, (40, 40, 40))#Название игры
            self.screen.blit(label, (70, 30))

            mouse_position = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_level1.collidepoint(mouse_position):#реализация кликабельности
                pygame.draw.rect(self.screen, (0, 0, 0), button_level1, border_radius=25)
                self.screen.blit(level1, (button_level1.centerx - 130, button_level1.centery - 70))
                if mouse_click[0]:
                    self.flag = 1
                    self.menu_trigger = False

            if button_level2.collidepoint(mouse_position):
                pygame.draw.rect(self.screen, (0, 0, 0), button_level2, border_radius=25)
                self.screen.blit(level2, (button_level2.centerx - 150, button_level2.centery - 70))
                if mouse_click[0]:
                    self.flag = 2
                    self.menu_trigger = False

            elif button_exit.collidepoint(mouse_position):
                pygame.draw.rect(self.screen, (0, 0, 0), button_exit, border_radius=25)
                self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)

            if self.flag == 1:
                with open('levels.json', 'r') as file:
                    data = json.load(file)
                    matrix = data["map_1"]
                    matrix1 = dict()
                    matrix1["map"] = matrix
                    json.dump(matrix1, open('current_lvl.json', 'w', encoding='utf-8'))
                self.screen.fill((0, 0, 0))
                text_surface = self.font.render("1 уровень", True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.center = (600, 400)
                self.screen.blit(text_surface, text_rect)
                pygame.display.flip()
                time.sleep(2)
                return True

            elif self.flag == 2:
                with open('levels.json', 'r') as file:
                    data = json.load(file)
                    matrix = data["map_2"]
                    matrix2 = dict()
                    matrix2["map"] = matrix
                    json.dump(matrix2, open('current_lvl.json', 'w', encoding='utf-8'))
                self.screen.fill((0, 0, 0))
                text_surface = self.font.render("2 уровень", True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.center = (600, 400)
                self.screen.blit(text_surface, text_rect)
                pygame.display.flip()
                time.sleep(2)
                return False


with open('current_lvl.json', 'r') as file:
    data = json.load(file)
    map_for_level = data["map"]

# переменные для правильного вычисления луча в rays_geometry
width_of_world = len(map_for_level[0]) * tile
height_of_world = len(map_for_level) * tile
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
collision_walls = []  # экземляр класса Rect
for j, row in enumerate(
        map_for_level):  # координаты строк - x, координаты списка - у
    for i, char in enumerate(row):
        if char:
            # заносим в множество только стены
            mini_map.add((i * map_tile, j * map_tile))
            # квадрат со стороной размера нашей стены
            collision_walls.append(pygame.Rect(i * tile, j * tile, tile, tile))
            if char == 1:
                world_map[(i * tile, j * tile)] = 1
            elif char == 2:
                world_map[(i * tile, j * tile)] = 2
