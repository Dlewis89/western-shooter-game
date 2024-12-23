import pygame
from pygame.math import Vector2
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(groups)

        self.import_assets(path)
        self.frame_index = 0
        self.status = 'down'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        self.pos = Vector2(self.rect.center)
        self.direction = Vector2()
        self.speed = 200
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites

        self.attacking = False

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = f"{self.status.split('_')[0]}_idle"

        if self.attacking:
            self.status = f"{self.status.split('_')[0]}_attack"



    def import_assets(self,path):
        self.animations = {}

        for index,folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
                    folder_path = folder[0].replace('\\','/')
                    path = f"{folder_path}/{file_name}"
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder_path.split('/')[-1]
                    self.animations[key].append(surf)

    def animation(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'

            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'

            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = Vector2()
                self.frame_index = 0

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
        self.get_status()
        self.move(dt)
        self.animation(dt)
