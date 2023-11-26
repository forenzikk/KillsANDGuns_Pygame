import pygame, time
from sprites_obj import *
from player_config import *
from drawings import Drawing
from cooperation import *


def write_text(text):#вывод текста перед игрой
    screen.fill((0, 0, 0))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(5)  # Задержка в 5 секунд
    return None


pygame.init()#инициализация всех необходимых модулей
screen = pygame.display.set_mode((width, height))#размер экрана
pygame.mouse.set_visible(False)
screen_map = pygame.Surface(minimap_res)

pygame.display.set_caption("Kills & Guns")#title of game
icon = pygame.image.load('images/icon.png')#icon

#инициализация экземпляров
sprites = Sprites()
clock = pygame.time.Clock()#желаемое кол-во кадров в сек
player = Player(sprites)
drawing = Drawing(screen, screen_map, player, clock)
interaction = Interaction(player, sprites, drawing)

drawing.menu()
interaction.musical_playing()
font = pygame.font.Font(None, 36)

write_text("Добро пожаловать в настоящий ад, мой друг! Посмотрим, что ты можешь")
while True:
    player.movement()
    drawing.background(player.angle)
    walls, wall_shot = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])#передаем список параметров стен и список вычисленных параметров спрайтов
    drawing.mini_map(player)
    drawing.player_weapon([wall_shot, sprites.sprite_shot])

    interaction.interaction_objects()
    interaction.npc_action()
    interaction.check_win()

    pygame.display.flip()#обновление содержимого на каждой итерации
    clock.tick()
