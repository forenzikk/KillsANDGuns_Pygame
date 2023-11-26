from play_map import *
from collections import deque
from random import randrange
import sys

class Drawing:
    def __init__(self, screen, screen_map, player, clock):
        self.screen = screen
        self.screen_map = screen_map
        self.player = player
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.Font('font/font.ttf', 144)
        self.textures = {1: pygame.image.load('images/wall1.png').convert(),
                         2: pygame.image.load('images/wall2.png').convert(),
                         'S': pygame.image.load('images/luna.jpg').convert()
                         }
        # menu
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('images/background.jpg').convert()
        # weapon parameters
        self.weapon_base_sprite = pygame.image.load('sprites/guns/shotgun/base/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/guns/shotgun/shot/{i}.png').convert_alpha()
                                            for i in range(20)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()#для удобного определения позиции спрайта с оружием
        self.weapon_position = ((width // 2) - self.weapon_rect.width // 2, height - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 3
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound('sounds/gun.mp3')
        # sfx parameters
        self.sfx = deque([pygame.image.load(f'sprites/guns/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % width#смещение по текстуре
        self.screen.blit(self.textures['S'], (sky_offset, 0))
        self.screen.blit(self.textures['S'], (sky_offset - width, 0))
        self.screen.blit(self.textures['S'], (sky_offset + width, 0))
        pygame.draw.rect(self.screen, (20, 20, 20), (0, (height // 2), width, height // 2))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):#отсортировали по глубине
            if obj[0]:
                _, object, object_pos = obj#отсекаем лишние значения для спрайтов
                self.screen.blit(object, object_pos)#наносим объекты на главную поверхность

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
            self.shot_projection = min(shots)[1] // 2
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

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.screen.blit(sfx, ((width // 2) - sfx_rect.w // 2, (height // 2) - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def win(self):#отрисовка окончания игры
        render = self.font_win.render('YOU WIN!!!', 1, (randrange(40, 120), 0, 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = (width // 2), (height // 2)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 430, rect.centery - 140))
        pygame.display.flip()
        self.clock.tick(15)

    def menu(self):#архитектура менюшки
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/menu_sound.mp3')
        pygame.mixer.music.play(-1)

        x = 0

        button_font = pygame.font.Font('font/font.ttf', 72)
        label_font = pygame.font.Font('font/font1.otf', 155)
        start = button_font.render('START', 1, pygame.Color('white'))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = (width // 2), (height // 2)
        exit = button_font.render('EXIT', 1, pygame.Color('white'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = (width // 2), (height // 2) + 200
        author = button_font.render("Made by Ovannisyan", 1, pygame.Color('white'))
        text_author = pygame.Rect(0, 0, 400, 150)
        text_author.center = (width // 2), (height // 2) + 300


        while self.menu_trigger:#отрисовка экрана перед игрой
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menu_picture, (0, 0), (x % width, height // 2, width, height))
            x += 1

            pygame.draw.rect(self.screen, (0, 0, 0), button_start, border_radius=25, width=10)#START
            self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.screen, (0, 0, 0), button_exit, border_radius=25, width=10)#EXIT
            self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            pygame.draw.rect(self.screen, (0, 0, 0), text_author, border_radius=25, width=10)#AUTHOR
            self.screen.blit(author, (text_author.centery - 520, text_author.centery - 20))

            label = label_font.render('KILLS and GUNS', 1, (40, 40, 40))#Название игры
            self.screen.blit(label, (70, 30))

            mouse_position = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_position):#реализация кликабельности
                pygame.draw.rect(self.screen, (0, 0, 0), button_start, border_radius=25)
                self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_position):
                pygame.draw.rect(self.screen, (0, 0, 0), button_exit, border_radius=25)
                self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)
