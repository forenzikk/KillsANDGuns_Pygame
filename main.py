import pygame
import time
from parametres import *
from player_config import Player
import math
from play_map import world_map
from drawings import elements_of_textures


def write_text(text):   #вывод текста перед игрой
    screen.fill((0, 0, 0))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(5)  # Задержка в 3 секунды
    return None


pygame.init()
screen = pygame.display.set_mode((1200, 800))

pygame.display.set_caption("Kills & Guns")
icon = pygame.image.load('images/icon.png')

bg_sound = pygame.mixer.Sound('sounds/sound.mp3')
bg_sound.play()

pygame.display.set_icon(icon)
clock = pygame.time.Clock()
screen_map = pygame.Surface((width // map_scale, height // map_scale))
player = Player()
drawing = elements_of_textures(screen, screen_map)

font = pygame.font.Font(None, 36)

write_text("Добро пожаловать в настоящий ад, мой друг! Посмотрим, что ты можешь")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    player.movement()
    screen.fill((0, 0, 0))

    drawing.background(player.angle)
    drawing.world(player.get_position, player.angle)
    drawing.mini_map(player)

    pygame.display.flip()
    clock.tick(fps)
