import pygame


def enemyScript(enemy_array, SCREEN_SIZE, enemy_speed, enemy1_image, screen):
    if enemy_array[len(enemy_array) - 1].x >= SCREEN_SIZE[0] - 30 or enemy_array[0].x <= 0:
        enemy_speed *= -1
    for enemy_rect in enemy_array:
        pygame.draw.rect(screen, (0, 0, 255), enemy_rect, 2, 3)
        screen.blit(enemy1_image, (enemy_rect.x, enemy_rect.y))
        enemy_rect.x += enemy_speed
