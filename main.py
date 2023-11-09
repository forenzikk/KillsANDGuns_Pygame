import pygame
import time
from parametres import *
from player_config import Player
import math
from play_map import world_map
from drawings import Drawing
from rays_geometry import *
from sprites_obj import *

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)
screen_map = pygame.Surface(minimap_res)

pygame.display.set_caption("Kills & Guns")#title of game
icon = pygame.image.load('images/icon.png')#icon

bg_sound = pygame.mixer.Sound('sounds/sound.mp3')#sound
bg_sound.play()

pygame.display.set_icon(icon)
clock = pygame.time.Clock()

#instance of classes
player = Player()
drawing = Drawing(screen, screen_map)
sprites = Sprites()

font = pygame.font.Font(None, 36)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(screen, screen_map)

def write_text(text):   #вывод текста перед игрой
    screen.fill((0, 0, 0))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(5)  # Задержка в 5 секунд
    return None

write_text("Добро пожаловать в настоящий ад, мой друг! Посмотрим, что ты можешь")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    screen.fill((0, 0, 0))

    #creating world
    drawing.background(player.angle)
    walls = ray_casting(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.mini_map(player)

    pygame.display.flip()
    clock.tick()
