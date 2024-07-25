import pygame
from random import randrange

pygame.init()
SCREEN_WIDTH: int = 756
SCREEN_HEIGHT: int = 850
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

road = pygame.image.load("Images\\road.png").convert_alpha()
player = pygame.transform.scale(pygame.image.load("Images\\player.png").convert_alpha(), (58.5, 132.5))
sprites = [pygame.transform.scale(pygame.image.load("Images\\red_car.png").convert_alpha(), (58.5, 132.5)),
           pygame.transform.scale(pygame.image.load("Images\\yellow_car.png").convert_alpha(), (58.5, 132.5))]
start: int = pygame.time.get_ticks()
clock = pygame.time.Clock()
player_x: int = 0
player_y: int = 500
running: bool = True
game_over: bool = False
y = 0
speed = 5


class EnemyCar:
    def __init__(self, sprites: list, speed: float): # NOQA
        self.sprite = sprites[randrange(0, len(sprites))]
        self.width, self.height = self.sprite.get_size()
        self.x_pos: int = randrange(0, 4)
        self.y_pos: float = -self.height
        self.speed_of_car: float = speed

    def car(self) -> None:
        self.y_pos += self.speed_of_car
        screen.blit(self.sprite, ((128.25 * self.x_pos) + 145, self.y_pos))

    def is_off_screen(self) -> bool:
        return self.y_pos > SCREEN_HEIGHT


def is_touching(player_x: float, player_y: int, player_width: float, player_height:float, enemy_car) -> bool: # NOQA
    enemy_x: float = (128.25 * enemy_car.x_pos) + 145
    enemy_y: float = enemy_car.y_pos
    enemy_width: float = enemy_car.width
    enemy_height: float = enemy_car.height

    return (player_x < enemy_x + enemy_width and
            player_x + player_width > enemy_x and
            player_y < enemy_y + enemy_height and
            player_y + player_height > enemy_y)


def is_valid_position(new_car, cars, min_distance=100) -> bool: # NOQA
    new_x = (128.25 * new_car.x_pos) + 145
    new_y = new_car.y_pos
    for car in cars: # NOQA
        existing_x = (128.25 * car.x_pos) + 145
        existing_y = car.y_pos
        if abs(new_x - existing_x) < car.width and abs(new_y - existing_y) < min_distance:
            return False
    return True


player_width, player_height = player.get_size()
cars = [EnemyCar(sprites, speed)]

while running:
    screen.blit(road, (0, y))
    y = y - speed
    if y <= -620:
        y = 0
        if speed < 250:
            speed += 0.001

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and player_x < 3 and (pygame.time.get_ticks() - start) > 500:
        player_x += 1
        start = pygame.time.get_ticks()
    if keys[pygame.K_LEFT] and player_x > 0 and (pygame.time.get_ticks() - start) > 500:
        player_x -= 1
        start = pygame.time.get_ticks()

    for car in cars:
        car.car()

    for car in cars[:]:
        if car.is_off_screen():
            cars.remove(car)
        elif is_touching((128.25 * player_x) + 145, player_y, player_width, player_height, car):
            game_over = True

    if len(cars) < 2 and randrange(0, 50) > 40:
        new_car = EnemyCar(sprites, speed)
        if is_valid_position(new_car, cars):
            cars.append(new_car)

    if game_over:
        pygame.draw.rect(screen, (200, 0, 0), (0, 50, SCREEN_WIDTH, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or ESC)', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, 100)
        screen.blit(text, text_rect)

    screen.blit(player, ((128.25 * player_x) + 145, player_y))
    pygame.display.update()
    pygame.event.pump()
    clock.tick(60)

    while game_over:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            game_over = False
            cars.clear()
            start = pygame.time.get_ticks()
            clock = pygame.time.Clock()
            player_x = 0
            player_y = 500
            running = True
            y = 0
            speed = 5
        if keys[pygame.K_ESCAPE]:
            game_over = False
            running = False
        pygame.event.pump()
pygame.quit()
