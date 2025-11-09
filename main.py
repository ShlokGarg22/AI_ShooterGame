# main.py
import pygame
from config import WIDTH, HEIGHT, FPS, TITLE
from player import Player
from bullet import BulletGroup
from enemy import EnemyManager
from arena import Arena
from camera import Camera

# ---------------------------------------------------------
# 1️⃣ Initialize Pygame
# ---------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# ---------------------------------------------------------
# 2️⃣ Load Assets (sprites)
# ---------------------------------------------------------
# Loading sprites from assets/sprites folder
player_img = pygame.image.load("assets/sprites/player_walk_0.png").convert_alpha()
bullet_img = pygame.image.load("assets/sprites/bullet.png").convert_alpha()

# Load enemy sprites (slime animations)
enemy_images = [
    pygame.image.load("assets/sprites/slime_animation_0.png").convert_alpha(),
    pygame.image.load("assets/sprites/slime_animation_1.png").convert_alpha(),
    pygame.image.load("assets/sprites/slime_animation_2.png").convert_alpha(),
    pygame.image.load("assets/sprites/slime_animation_3.png").convert_alpha()
]

# ---------------------------------------------------------
# 3️⃣ Create Player + Bullet Group + Enemies + Arena
# ---------------------------------------------------------
player = Player(WIDTH // 2, HEIGHT // 2, player_img)
bullets = BulletGroup()
enemy_manager = EnemyManager(enemy_images)
arena = Arena(WIDTH, HEIGHT)
camera = Camera()

# Game state
score = 0
game_over = False
wave = 1
enemies_per_wave = 5
enemies_spawned_this_wave = 0
enemies_killed_this_wave = 0
wave_complete = False
wave_complete_timer = 0

# Spawn zones (left and right edges)
SPAWN_LEFT = 50
SPAWN_RIGHT = WIDTH - 50

# ---------------------------------------------------------
# 4️⃣ Main Game Loop
# ---------------------------------------------------------
running = True
while running:
    dt = clock.tick(FPS) / 16.67   # frame time normalization (~60fps baseline)

    # ---- Handle Quit ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---- Mouse Shooting ----
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_over and player.can_shoot():
                player.shoot(bullets, bullet_img)
                camera.start_shake(3, 8)  # Shake on shoot
        
        # ---- Restart Game ----
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            # Reset everything
            player = Player(WIDTH // 2, HEIGHT // 2, player_img)
            bullets = BulletGroup()
            enemy_manager.reset()
            score = 0
            game_over = False
            wave = 1
            enemies_per_wave = 5
            enemies_spawned_this_wave = 0
            enemies_killed_this_wave = 0
            wave_complete = False
            wave_complete_timer = 0

    if not game_over:
        # ---- Wave System: Spawn enemies from left and right ----
        if not wave_complete:
            if enemies_spawned_this_wave < enemies_per_wave:
                if enemy_manager.get_count() < enemies_per_wave:
                    # Spawn from left or right edge
                    spawn_side = "left" if enemies_spawned_this_wave % 2 == 0 else "right"
                    spawn_x = SPAWN_LEFT if spawn_side == "left" else SPAWN_RIGHT
                    spawn_y = HEIGHT // 2 + (enemies_spawned_this_wave - enemies_per_wave // 2) * 80
                    
                    # Clamp Y position
                    spawn_y = max(100, min(HEIGHT - 100, spawn_y))
                    
                    enemy_manager.spawn_enemy_at(spawn_x, spawn_y)
                    enemies_spawned_this_wave += 1
        
        # ---- Update ----
        player.handle_input(dt)
        player.aim_and_rotate(pygame.mouse.get_pos())
        player.update_invincibility()
        bullets.update(dt)
        
        # Check collision with obstacles
        obstacle_rects = arena.get_obstacle_rects()
        for obs_rect in obstacle_rects:
            if player.rect.colliderect(obs_rect):
                # Push player back
                if hasattr(player, 'vel_x') and hasattr(player, 'vel_y'):
                    player.rect.x -= player.vel_x * dt
                    player.rect.y -= player.vel_y * dt
        
        enemy_manager.update(dt, player.rect.center)
        arena.update_camera(player.rect.center)
        camera.update()
        
        # ---- Check Collisions ----
        # Bullets vs Enemies
        kills = enemy_manager.check_bullet_collisions(bullets)
        if kills > 0:
            score += kills * 10
            enemies_killed_this_wave += kills
            camera.start_shake(5, 10)  # Shake on enemy kill
        
        # Enemies vs Player
        if enemy_manager.check_player_collision(player.rect):
            if player.take_damage(1):
                camera.start_shake(8, 15)  # Big shake on damage
        
        # Check if player died
        if not player.is_alive():
            game_over = True
        
        # ---- Wave Complete Check ----
        if enemies_killed_this_wave >= enemies_per_wave and not wave_complete:
            wave_complete = True
            wave_complete_timer = 120  # 2 seconds at 60fps
        
        if wave_complete:
            wave_complete_timer -= 1
            if wave_complete_timer <= 0:
                # Start next wave
                wave += 1
                enemies_per_wave = 5 + wave * 2  # More enemies each wave
                enemies_spawned_this_wave = 0
                enemies_killed_this_wave = 0
                wave_complete = False
                # Increase enemy difficulty
                enemy_manager.increase_difficulty()

        # ---- Draw ----
        arena.draw(screen)  # Draw arena background
        
        # Apply camera shake
        cam_offset = camera.get_offset()
        player_rect_shaken = player.rect.move(cam_offset)
        screen.blit(player.image, player_rect_shaken)
        
        # Draw bullets with shake
        for bullet in bullets.sprites():
            bullet_rect = bullet.rect.move(cam_offset)
            screen.blit(bullet.image, bullet_rect)
        
        enemy_manager.draw(screen, cam_offset)
        
        # Draw UI
        player.draw_health_bar(screen, font)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 40))
        
        wave_text = font.render(f"Wave: {wave}", True, (255, 215, 0))
        screen.blit(wave_text, (WIDTH - 150, 10))
        
        enemies_text = small_font.render(f"Enemies: {enemies_killed_this_wave}/{enemies_per_wave}", True, (255, 255, 255))
        screen.blit(enemies_text, (10, 70))
        
        # Wave complete banner
        if wave_complete:
            banner_text = font.render(f"WAVE {wave} COMPLETE!", True, (0, 255, 0))
            banner_rect = banner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            # Draw semi-transparent background
            overlay = pygame.Surface((banner_rect.width + 40, banner_rect.height + 20))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            overlay_rect = overlay.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(overlay, overlay_rect)
            screen.blit(banner_text, banner_rect)
    
    else:
        # ---- Game Over Screen ----
        arena.draw(screen)  # Keep background
        
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        wave_reached_text = font.render(f"Wave Reached: {wave}", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        
        text_rect1 = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        text_rect2 = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
        text_rect3 = wave_reached_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        text_rect4 = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        screen.blit(game_over_text, text_rect1)
        screen.blit(final_score_text, text_rect2)
        screen.blit(wave_reached_text, text_rect3)
        screen.blit(restart_text, text_rect4)

    pygame.display.flip()

# ---------------------------------------------------------
# 5️⃣ Exit Game Cleanly
# ---------------------------------------------------------
pygame.quit()
