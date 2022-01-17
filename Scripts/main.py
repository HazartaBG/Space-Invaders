import pygame
import time
import sys
import random
from pygame.locals import *
from player import Player

pygame.init()

images_path = '..\\Resources\\Sprites\\'
enemy1_image = pygame.transform.scale(pygame.image.load(images_path + "enemyBlack5.png"), (30, 25))  # Image scaled to 30% of it's original size
enemy2_image = pygame.transform.scale(pygame.image.load(images_path + "enemyRed1.png"), (30, 27))  # Image scaled to 30% of it's original size
player_image = pygame.transform.scale(pygame.image.load(images_path + "playerShip1_blue.png"), (30, 20))  # Image scaled to 30% of it's original size
player_laser_image = pygame.transform.scale(pygame.image.load(images_path + "laserBlue02.png"), (6, 14))
enemy_laser_image = pygame.transform.scale(pygame.image.load(images_path + "laserRed02.png"), (6, 14))

clock = pygame.time.Clock()
framerate = 60
last_time = time.time()

SCREEN_SIZE = (640, 480)  # X, Y
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Space Invaders")

player = Player(screen, player_image, player_laser_image, clock)

test_rect = Rect(SCREEN_SIZE[0] / 2 - 35, SCREEN_SIZE[1] / 2 - 35, 70, 70)

moving_right = False
moving_left = False
moving_up = False
moving_down = False
shooting = False

PLAYER_SPEED = 3
enemy_array = []
enemy_laser_arr = []

for y in range(0, 150, 50):
    for x in range(120, SCREEN_SIZE[0]-120, 60):
        enemy_rect = Rect(x, y, 30, 25)
        enemy_array.append(enemy_rect)

COOLDOWN_TIME = 700
cooldown_tracker = 0
started_cooldown = False

enemy_speed = 2

while True:
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    screen.fill((0, 0, 0))
    player.update(PLAYER_SPEED, dt, up=moving_up, down=moving_down, right=moving_right, left=moving_left, shooting=shooting)

    if enemy_array[len(enemy_array) - 1].x >= SCREEN_SIZE[0] - 30 or enemy_array[0].x < 0:
        enemy_speed *= -1

    for enemy_rect in enemy_array:
        pygame.draw.rect(screen, (0, 0, 255), enemy_rect, 2, 3)
        screen.blit(enemy1_image, (enemy_rect.x, enemy_rect.y))
        enemy_rect.x += enemy_speed

    if started_cooldown:
        cooldown_tracker += clock.get_time()
        if cooldown_tracker > COOLDOWN_TIME:
            cooldown_tracker = 0
            started_cooldown = False

    if not started_cooldown:
        laser_rect = Rect(random.choice(enemy_array).x + 15, random.choice(enemy_array).y + 25, 6, 14)
        enemy_laser_arr.append(laser_rect)
        started_cooldown = True

    for laser in enemy_laser_arr:
        # pygame.draw.rect(screen, (255, 0, 0), laser, 2, 3)
        screen.blit(enemy_laser_image, (laser.x, laser.y))
        laser.y += round(5 * dt)
        if laser.y > SCREEN_SIZE[1] + 10:
            enemy_laser_arr.remove(laser)

    mouse_pos = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 15, 20)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            # if event.key == K_x:
            #     for enemy_rect in enemy_array:
            #         enemy_rect.y += 50
            if event.key == K_a:
                moving_left = True
            elif event.key == K_d:
                moving_right = True
            if event.key == K_w:
                moving_up = True
            elif event.key == K_s:
                moving_down = True
            if event.key == K_SPACE:
                shooting = True

        if event.type == KEYUP:
            if event.key == K_a:
                moving_left = False
            elif event.key == K_d:
                moving_right = False
            if event.key == K_w:
                moving_up = False
            elif event.key == K_s:
                moving_down = False
            if event.key == K_SPACE:
                shooting = False

    pygame.display.update()
    clock.tick_busy_loop(framerate)
