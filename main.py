import pygame
import time
from parametres import *

from player_config import *
import math
from play_map import *
from rays_geometry import *


pygame.init()
screen = pygame.display.set_mode((1200, 800))

pygame.display.set_caption("Kills & Guns")
icon = pygame.image.load('images/icon.png')

bg_sound = pygame.mixer.Sound('sounds/sound.mp3')
bg_sound.play()

pygame.display.set_icon(icon)
clock = pygame.time.Clock()
player = Player()

font = pygame.font.Font(None, 36)


def write_text(text):   #вывод текста перед игрой
    screen.fill((0, 0, 0))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(5)  # Задержка в 3 секунды
    return None

write_text("Добро пожаловать в настоящий ад, мой друг! Посмотрим, что ты можешь")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    player.movement()
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (40, 40, 40), (0, 0, width, (height // 2)))#небо
    pygame.draw.rect(screen, (15, 15, 15), (0, (height // 2), width, (height // 2)))#земля

    ray_casting(screen, player.get_position, player.angle) #настройка видимости игрока

    pygame.display.flip()
    clock.tick(fps)
