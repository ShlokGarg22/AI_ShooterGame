# enemy.py
import pygame
import random
import math
from config import ENEMY_BASE_SPEED, ENEMY_SCALE, ENEMY_HP, WIDTH, HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_images):
        super().__init__()
        self.sprite_images = [pygame.transform.scale_by(img, ENEMY_SCALE) for img in sprite_images]
        self.image = self.sprite_images[0]
        self.rect = self.image.get_rect(center=(x, y))
        
        # Health and stats
        self.health = ENEMY_HP
        self.max_health = ENEMY_HP
        self.speed = ENEMY_BASE_SPEED
        
        # Animation
        self.animation_count = 0
        self.animation_speed = 0.25  # Animation speed
        
        # AI behavior
        self.reset_offset = 0
        self.offset_x = random.randrange(-100, 100)
        self.offset_y = random.randrange(-100, 100)
    
    def update(self, dt, player_pos):
        # Update animation
        self.animation_count += self.animation_speed * dt
        if self.animation_count >= len(self.sprite_images):
            self.animation_count = 0
        self.image = self.sprite_images[int(self.animation_count)]
        
        # AI movement with randomized offset
        if self.reset_offset == 0:
            self.offset_x = random.randrange(-100, 100)
            self.offset_y = random.randrange(-100, 100)
            self.reset_offset = random.randrange(120, 180)
        else:
            self.reset_offset -= 1
        
        # Move toward player with offset using vector math
        target_x = player_pos[0] + self.offset_x
        target_y = player_pos[1] + self.offset_y
        
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 5:
            dx /= dist
            dy /= dist
            self.rect.x += dx * self.speed * dt
            self.rect.y += dy * self.speed * dt
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True  # Enemy died
        return False
    
    def draw_health_bar(self, surface, camera_offset=(0, 0)):
        # Draw health bar above enemy
        bar_width = 30
        bar_height = 4
        bar_x = self.rect.centerx - bar_width // 2 + camera_offset[0]
        bar_y = self.rect.top - 8 + camera_offset[1]
        
        # Background (red)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # Foreground (green)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))


class EnemyManager:
    def __init__(self, sprite_images):
        self.enemies = pygame.sprite.Group()
        self.sprite_images = sprite_images
        self.spawn_timer = 0
        self.difficulty_multiplier = 1.0
    
    def update(self, dt, player_pos):
        # Update all enemies
        for enemy in self.enemies:
            enemy.update(dt, player_pos)
    
    def spawn_enemy_at(self, x, y):
        """Spawn enemy at specific position"""
        enemy = Enemy(x, y, self.sprite_images)
        enemy.speed *= self.difficulty_multiplier
        enemy.max_health = int(ENEMY_HP * self.difficulty_multiplier)
        enemy.health = enemy.max_health
        self.enemies.add(enemy)
    
    def increase_difficulty(self):
        """Make enemies harder each wave"""
        self.difficulty_multiplier += 0.15
    
    def draw(self, surface, camera_offset=(0, 0)):
        # Draw all enemies with camera shake
        for enemy in self.enemies:
            enemy_rect = enemy.rect.move(camera_offset)
            surface.blit(enemy.image, enemy_rect)
            enemy.draw_health_bar(surface, camera_offset)
    
    def check_bullet_collisions(self, bullets):
        """Check collisions between bullets and enemies"""
        kills = 0
        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
            if hit_enemies:
                bullet.kill()
                for enemy in hit_enemies:
                    if enemy.take_damage(20):  # 20 damage per bullet
                        kills += 1
                break
        return kills
    
    def check_player_collision(self, player_rect):
        """Check if any enemy is touching the player"""
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.rect):
                return True
        return False
    
    def get_count(self):
        return len(self.enemies)
    
    def reset(self):
        self.enemies.empty()
        self.spawn_timer = 0
        self.difficulty_multiplier = 1.0
