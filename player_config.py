from play_map import *

class Player:
    def __init__(self, sprites):
        self.x, self.y = player_position
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.004#чувствительность
        # collision parameters
        self.side = 50#размер стороны квадрата, который будет игроком вместо точки
        self.rect = pygame.Rect(*player_position, self.side, self.side)
        # gun
        self.shot = False

    @property
    def get_position(self):
        return (self.x, self.y)

    @property #перенос списка всех коллизий в отдельное св-во (стены + спрайты)
    def collision_list(self):
        return collision_walls + [pygame.Rect(*obj.get_position, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()#копия текущего положения
        next_rect.move_ip(dx, dy)#переместим на dx, dy
        hit_indexes = next_rect.collidelistall(self.collision_list)#индекс стен с которыми столкнулся игрок (относительно)

        if len(hit_indexes):#в зависимости от столкновения ищем сторону, с которой столкнулись
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

            if abs(delta_x - delta_y) < 10:#уперлись в угол
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y#перемещение квадрата, за который выступает игрок
        self.angle %= (math.pi * 2)#угол направления игрока

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)#разрешение движения
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
            difference = pygame.mouse.get_pos()[0] - (width // 2)#разница координат курсора и середины окна
            pygame.mouse.set_pos(((width // 2), (height // 2)))#переносим указатель в центр
            self.angle += difference * self.sensitivity#прибавляем к нему ту самую разницу + учет чувствительности
