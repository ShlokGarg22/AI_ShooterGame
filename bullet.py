# bullet.py
import pygame, math
from config import BULLET_SPEED, BULLET_LIFETIME, BULLET_SCALE

# ---------------------------------------------------------
# Bullet: tiny moving sprite that flies toward mouse
# ---------------------------------------------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target, image):
        super().__init__()
        # scale pixel bullet sprite
        self.image = pygame.transform.scale_by(image, BULLET_SCALE)
        self.rect = self.image.get_rect(center=pos)

        # calculate direction vector from player → target
        dx, dy = target[0] - pos[0], target[1] - pos[1]
        angle = math.atan2(dy, dx)
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * BULLET_SPEED

        # store when this bullet was created (to auto-delete later)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        # move bullet
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt

        # remove if lifetime expired
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

# ---------------------------------------------------------
# BulletGroup: manages all bullets easily
# ---------------------------------------------------------
class BulletGroup(pygame.sprite.Group):
    def add_bullet(self, pos, target, image):
        self.add(Bullet(pos, target, image))
