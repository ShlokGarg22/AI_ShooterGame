# setup_sprites.py
# Script to create the bullet sprite in the assets folder
import pygame

pygame.init()

# Create bullet sprite (8x8 pixels - small yellow projectile)
bullet_surface = pygame.Surface((8, 8), pygame.SRCALPHA)
pygame.draw.circle(bullet_surface, (255, 255, 100), (4, 4), 3)
pygame.draw.circle(bullet_surface, (255, 220, 80), (4, 4), 2)
pygame.image.save(bullet_surface, "assets/sprites/bullet.png")

print("✅ Created bullet.png in assets/sprites/")
