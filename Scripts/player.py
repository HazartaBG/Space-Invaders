import pygame

PLAYER_SPEED = 2
LASER_SPEED = 5

COOLDOWN_TIME = 10
cooldown_tracker = 0
started_cooldown = False


class Player(pygame.sprite.Sprite):

    def __init__(self, parent, image, laser_image, clock):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.image_size = self.image.get_size()

        self.laser_image = laser_image
        self.laser_size = self.laser_image.get_size()
        self.lasers = []

        self.parent = parent
        self.parent_size = self.parent.get_size()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.parent_size[0] // 2, self.parent_size[1] // 2

        self.clock = clock
        self.lives = 3

    def update(self, player_speed, dt, enemy_list, **kwargs) -> list[pygame.Rect]:
        global cooldown_tracker, started_cooldown

        if started_cooldown:
            cooldown_tracker += self.clock.get_time()
            if cooldown_tracker > COOLDOWN_TIME:
                cooldown_tracker = 0
                started_cooldown = False

        if kwargs.get("up") and self.rect.y > 0:
            self.rect.y = round(self.rect.y - PLAYER_SPEED * dt)
        elif kwargs.get("down") and self.rect.y < self.parent_size[1] - self.image_size[1]:
            self.rect.y = round(self.rect.y + PLAYER_SPEED * dt)

        if kwargs.get("left") and self.rect.x > 0:
            self.rect.x = round(self.rect.x - PLAYER_SPEED * dt)
        elif kwargs.get("right") and self.rect.x < self.parent_size[0] - self.image_size[0]:
            self.rect.x = round(self.rect.x + PLAYER_SPEED * dt)

        if kwargs.get("shooting"):
            if not started_cooldown:  # and not len(self.lasers)
                laser_rect = pygame.Rect(self.rect.x + self.laser_size[1] - 2, self.rect.y, self.laser_size[0], self.laser_size[1])
                self.lasers.append(laser_rect)
                started_cooldown = True

        for laser_rect in self.lasers:
            self.parent.blit(self.laser_image, (laser_rect.x, laser_rect.y))
            # pygame.draw.rect(self.parent, (0, 0, 255), laser_rect, 2, 3)
            for index in laser_rect.collidelistall(enemy_list):
                enemy_list.pop(index)
                self.lasers.remove(laser_rect)

            if laser_rect.y < -20:
                self.lasers.remove(laser_rect)
            else:
                laser_rect.y = round(laser_rect.y - LASER_SPEED * dt)

        # pygame.draw.rect(self.parent, (0, 0, 255), self.rect, 2, 3)
        self.parent.blit(self.image, (self.rect.x, self.rect.y))

        return enemy_list

    def take_damage(self, damage):
        self.lives -= damage

