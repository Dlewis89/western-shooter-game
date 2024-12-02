import pygame
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((100,100))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)

        self.pos = Vector2(self.rect.center)
        self.direction = Vector2()
        self.speed = 200

        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, dt):
        if self.direction.magnitude() > 0:
         self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

    def update(self, dt):
        self.input()
        self.move(dt)
