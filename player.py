# player.py
import pygame, math
from config import PLAYER_SPEED, PLAYER_SCALE, PLAYER_FIRE_COOLDOWN

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        # store base (unrotated) sprite and position
        self.original_image = pygame.transform.scale_by(sprite, PLAYER_SCALE)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.last_shot = 0  # last bullet fired (timestamp)
        
        # Health system
        self.health = 100
        self.max_health = 100
        self.invincibility_timer = 0  # Frames of invincibility after taking damage
        self.damage_cooldown = 30  # Take damage every 0.5 seconds

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        # movement vector from keys
        move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
        move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_SPEED
        # Store velocity for collision handling
        self.vel_x = move_x
        self.vel_y = move_y
        # apply movement (scaled by delta time)
        self.rect.x += move_x * dt
        self.rect.y += move_y * dt

    def aim_and_rotate(self, mouse_pos):
        # rotate sprite to face mouse
        dx, dy = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def can_shoot(self):
        # cooldown check (ms)
        return pygame.time.get_ticks() - self.last_shot >= PLAYER_FIRE_COOLDOWN

    def shoot(self, bullets, bullet_img):
        # spawn bullet toward mouse
        self.last_shot = pygame.time.get_ticks()
        bullets.add_bullet(self.rect.center, pygame.mouse.get_pos(), bullet_img)
    
    def take_damage(self, damage):
        if self.invincibility_timer <= 0:
            self.health -= damage
            self.invincibility_timer = self.damage_cooldown
            if self.health < 0:
                self.health = 0
            return True
        return False
    
    def update_invincibility(self):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
    
    def is_alive(self):
        return self.health > 0
    
    def draw_health_bar(self, surface, font):
        # Health bar background
        pygame.draw.rect(surface, (255, 0, 0), (10, 10, 200, 20))
        # Health bar foreground
        health_width = (self.health / self.max_health) * 200
        pygame.draw.rect(surface, (0, 255, 0), (10, 10, health_width, 20))
        # Health text
        health_text = font.render(f"HP: {self.health}/{self.max_health}", True, (255, 255, 255))
        surface.blit(health_text, (220, 10))
