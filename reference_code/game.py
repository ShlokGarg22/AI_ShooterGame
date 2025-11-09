import pygame
import sys
import math
import random

pygame.init()

display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load and convert images for better performance
player_walk_images = [pygame.image.load("player_walk_0.png").convert_alpha(), 
                      pygame.image.load("player_walk_1.png").convert_alpha(),
                      pygame.image.load("player_walk_2.png").convert_alpha(), 
                      pygame.image.load("player_walk_3.png").convert_alpha()]

player_weapon = pygame.image.load("shotgun.png").convert()
player_weapon.set_colorkey((255,255,255))

# Font for UI
font = pygame.font.Font(None, 36)

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
        self.health = 100
        self.max_health = 100
    def handle_weapons(self, display):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x, rel_y = mouse_x - player.x, mouse_y - player.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        player_weapon_copy = pygame.transform.rotate(player_weapon, angle)

        display.blit(player_weapon_copy, (self.x+15-int(player_weapon_copy.get_width()/2), self.y+25-int(player_weapon_copy.get_height()/2)))


    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0

        self.animation_count += 1

        if self.moving_right:
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32, 42)), (self.x, self.y))
        elif self.moving_left:
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
        else:
            display.blit(pygame.transform.scale(player_walk_images[0], (32, 42)), (self.x, self.y))

        self.handle_weapons(display)

        self.moving_right = False
        self.moving_left = False
    
    def draw_health_bar(self, display):
        # Health bar background
        pygame.draw.rect(display, (255, 0, 0), (10, 10, 200, 20))
        # Health bar foreground
        health_width = (self.health / self.max_health) * 200
        pygame.draw.rect(display, (0, 255, 0), (10, 10, health_width, 20))
        # Health text
        health_text = font.render(f"HP: {self.health}/{self.max_health}", True, (255, 255, 255))
        display.blit(health_text, (220, 10))

class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.radius = 5
    
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0,0,0), (self.x+16, self.y+16), self.radius)
    
    def is_off_screen(self):
        # Check if bullet is far off screen (for cleanup)
        return self.x < -100 or self.x > 900 or self.y < -100 or self.y > 700

class SlimeEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_images = [pygame.image.load("slime_animation_0.png").convert_alpha(), 
                                pygame.image.load("slime_animation_1.png").convert_alpha(),
                                pygame.image.load("slime_animation_2.png").convert_alpha(), 
                                pygame.image.load("slime_animation_3.png").convert_alpha()]
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-300, 300)
        self.offset_y = random.randrange(-300, 300)
        self.health = 30
        self.width = 32
        self.height = 30
    def main(self, display):
        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-300, 300)
            self.offset_y = random.randrange(-300, 300)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player.x + self.offset_x > self.x-display_scroll[0]:
            self.x += 1
        elif player.x + self.offset_x < self.x-display_scroll[0]:
            self.x -= 1

        if player.y + self.offset_y > self.y-display_scroll[1]:
            self.y += 1
        elif player.y + self.offset_y < self.y-display_scroll[1]:
            self.y -= 1

        display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (self.width, self.height)), (self.x-display_scroll[0], self.y-display_scroll[1]))
    
    def check_collision_with_bullet(self, bullet):
        # Simple circle collision detection
        bullet_center_x = bullet.x + 16
        bullet_center_y = bullet.y + 16
        enemy_center_x = self.x - display_scroll[0] + self.width // 2
        enemy_center_y = self.y - display_scroll[1] + self.height // 2
        
        distance = math.sqrt((bullet_center_x - enemy_center_x)**2 + (bullet_center_y - enemy_center_y)**2)
        return distance < (bullet.radius + self.width // 2)
    
    def check_collision_with_player(self, player_obj):
        # Check if enemy touches player
        if (abs(self.x - display_scroll[0] - player_obj.x) < 30 and 
            abs(self.y - display_scroll[1] - player_obj.y) < 30):
            return True
        return False



enemies = [SlimeEnemy(400, 300)]
player = Player(400, 300, 32, 32)

display_scroll = [0,0]

player_bullets = []

# Game stats
score = 0
spawn_timer = 0
spawn_interval = 120  # Spawn enemy every 2 seconds (120 frames at 60 FPS)
game_over = False

while True:
    display.fill((24,164,86))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not game_over:
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Restart game
                player.health = player.max_health
                enemies = [SlimeEnemy(400, 300)]
                player_bullets = []
                score = 0
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()

        pygame.draw.rect(display, (255,255,255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))

        if keys[pygame.K_a]:
            display_scroll[0] -= 5
            player.moving_left = True
            for bullet in player_bullets:
                bullet.x += 5
        if keys[pygame.K_d]:
            display_scroll[0] += 5
            player.moving_right = True
            for bullet in player_bullets:
                bullet.x -= 5
        if keys[pygame.K_w]:
            display_scroll[1] -= 5
            for bullet in player_bullets:
                bullet.y += 5
        if keys[pygame.K_s]:
            display_scroll[1] += 5
            for bullet in player_bullets:
                bullet.y -= 5

        # Spawn new enemies
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            # Spawn enemy at random position off screen
            spawn_side = random.randint(0, 3)
            if spawn_side == 0:  # Top
                new_enemy = SlimeEnemy(random.randint(0, 800) + display_scroll[0], -50 + display_scroll[1])
            elif spawn_side == 1:  # Bottom
                new_enemy = SlimeEnemy(random.randint(0, 800) + display_scroll[0], 650 + display_scroll[1])
            elif spawn_side == 2:  # Left
                new_enemy = SlimeEnemy(-50 + display_scroll[0], random.randint(0, 600) + display_scroll[1])
            else:  # Right
                new_enemy = SlimeEnemy(850 + display_scroll[0], random.randint(0, 600) + display_scroll[1])
            enemies.append(new_enemy)

        player.main(display)

        # Update and draw bullets
        for bullet in player_bullets[:]:
            bullet.main(display)
            # Remove bullets that are off screen
            if bullet.is_off_screen():
                player_bullets.remove(bullet)

        # Update enemies and check collisions
        for enemy in enemies[:]:
            enemy.main(display)
            
            # Check collision with bullets
            for bullet in player_bullets[:]:
                if enemy.check_collision_with_bullet(bullet):
                    enemy.health -= 10
                    if bullet in player_bullets:
                        player_bullets.remove(bullet)
                    if enemy.health <= 0:
                        if enemy in enemies:
                            enemies.remove(enemy)
                        score += 10
                    break
            
            # Check collision with player
            if enemy.check_collision_with_player(player):
                player.health -= 1
                if player.health <= 0:
                    game_over = True

        # Draw UI
        player.draw_health_bar(display)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        display.blit(score_text, (10, 40))
        enemies_text = font.render(f"Enemies: {len(enemies)}", True, (255, 255, 255))
        display.blit(enemies_text, (10, 70))

    else:
        # Game Over screen
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        
        display.blit(game_over_text, (300, 250))
        display.blit(final_score_text, (280, 300))
        display.blit(restart_text, (250, 350))

    clock.tick(60)
    pygame.display.update()
