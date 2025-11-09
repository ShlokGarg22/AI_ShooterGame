# arena.py
import pygame
import random

class Arena:
    """Manages the game arena with parallax background layers and obstacles"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Load all background layers for parallax effect
        try:
            # Load full HD background layers
            self.bg_sky = pygame.image.load("asset1/PNG/Background/1920x1080/Sky_1920x1080.png").convert()
            self.bg_clouds = pygame.image.load("asset1/PNG/Background/1920x1080/Clouds_1920x1080.png").convert_alpha()
            self.bg_flora1 = pygame.image.load("asset1/PNG/Background/1920x1080/Flora1_1920x1080.png").convert_alpha()
            self.bg_flora2 = pygame.image.load("asset1/PNG/Background/1920x1080/Flora2_1920x1080.png").convert_alpha()
            
            # Scale backgrounds to fit screen
            self.bg_sky = pygame.transform.scale(self.bg_sky, (width, height))
            self.bg_clouds = pygame.transform.scale(self.bg_clouds, (width, height))
            self.bg_flora1 = pygame.transform.scale(self.bg_flora1, (width, height))
            self.bg_flora2 = pygame.transform.scale(self.bg_flora2, (width, height))
            
            print("✅ Loaded background layers successfully!")
        except Exception as e:
            print(f"⚠️ Error loading backgrounds: {e}")
            # Fallback gradient background
            self.bg_sky = pygame.Surface((width, height))
            self.bg_sky.fill((135, 206, 250))  # Sky blue
            self.bg_clouds = None
            self.bg_flora1 = None
            self.bg_flora2 = None
        
        # Load obstacle and decoration sprites
        self.obstacles = []
        self.decorations = []
        self.ground_tiles = []
        
        self.load_tileset()
        self.load_objects()
        self.load_decorations()
        
        # Camera offset for parallax
        self.camera_x = 0
        self.camera_y = 0
        self.parallax_offset_x = 0
        self.parallax_offset_y = 0
    
    def load_tileset(self):
        """Load ground tileset and create multiple platform levels"""
        try:
            tileset = pygame.image.load("asset1/PNG/Tileset.png").convert_alpha()
            tile_size = 32
            
            # Extract different tiles from tileset
            grass_tile = tileset.subsurface(pygame.Rect(0, 0, tile_size, tile_size))
            dirt_tile = tileset.subsurface(pygame.Rect(32, 0, tile_size, tile_size))
            stone_tile = tileset.subsurface(pygame.Rect(64, 0, tile_size, tile_size))
            
            # Create multiple ground levels for depth
            # Bottom ground (main floor)
            ground_y = self.height - 80
            for x in range(0, self.width, tile_size):
                tile_rect = pygame.Rect(x, ground_y, tile_size, tile_size)
                self.ground_tiles.append({"image": grass_tile, "rect": tile_rect, "layer": 3})
            
            # Middle platforms (left side)
            for x in range(100, 300, tile_size):
                tile_rect = pygame.Rect(x, 350, tile_size, tile_size)
                self.ground_tiles.append({"image": stone_tile, "rect": tile_rect, "layer": 2})
            
            # Middle platforms (right side)
            for x in range(650, 850, tile_size):
                tile_rect = pygame.Rect(x, 350, tile_size, tile_size)
                self.ground_tiles.append({"image": stone_tile, "rect": tile_rect, "layer": 2})
            
            # Top platform (center)
            for x in range(350, 610, tile_size):
                tile_rect = pygame.Rect(x, 200, tile_size, tile_size)
                self.ground_tiles.append({"image": dirt_tile, "rect": tile_rect, "layer": 1})
            
            print("✅ Loaded tileset and created multi-level ground")
        except Exception as e:
            print(f"⚠️ Error loading tileset: {e}")
    
    def load_objects(self):
        """Load ALL interactive objects and create a complete arena"""
        try:
            # Load all object images
            chest = pygame.image.load("asset1/PNG/chest.png").convert_alpha()
            flying_stone = pygame.image.load("asset1/PNG/Flying_stone.png").convert_alpha()
            cave = pygame.image.load("asset1/PNG/cave_entrance.png").convert_alpha()
            key = pygame.image.load("asset1/PNG/key.png").convert_alpha()
            
            # Load additional objects
            try:
                objects_sheet = pygame.image.load("asset1/PNG/Objects.png").convert_alpha()
            except:
                objects_sheet = None
            
            # Scale objects to appropriate sizes
            chest = pygame.transform.scale(chest, (50, 45))
            flying_stone_large = pygame.transform.scale(flying_stone, (100, 70))
            flying_stone_medium = pygame.transform.scale(flying_stone, (70, 50))
            flying_stone_small = pygame.transform.scale(flying_stone, (50, 35))
            cave = pygame.transform.scale(cave, (180, 140))
            key = pygame.transform.scale(key, (30, 30))
            
            # ===== FLOATING ISLANDS (obstacles) =====
            obstacle_positions = [
                # Top floating islands
                (160, 150, flying_stone_large),
                (480, 120, flying_stone_large),
                (800, 160, flying_stone_large),
                
                # Mid-level floating stones
                (300, 280, flying_stone_medium),
                (660, 290, flying_stone_medium),
                (480, 350, flying_stone_small),
                
                # Lower level obstacles
                (120, 450, chest),
                (840, 440, chest),
                (420, 480, chest),
                (580, 485, chest),
                
                # Extra floating platforms
                (250, 400, flying_stone_small),
                (710, 395, flying_stone_small),
            ]
            
            for x, y, img in obstacle_positions:
                rect = img.get_rect(center=(x, y))
                self.obstacles.append({"image": img, "rect": rect})
            
            # ===== BACKGROUND DECORATIONS =====
            # Cave entrance (center top)
            cave_rect = cave.get_rect(center=(self.width // 2, 120))
            self.decorations.append({"image": cave, "rect": cave_rect, "layer": "back"})
            
            # Keys scattered around (decorative)
            key_positions = [(200, 320), (760, 330), (480, 230)]
            for x, y in key_positions:
                key_rect = key.get_rect(center=(x, y))
                self.decorations.append({"image": key, "rect": key_rect, "layer": "mid"})
            
            print("✅ Loaded all objects successfully - Full arena created!")
        except Exception as e:
            print(f"⚠️ Error loading objects: {e}")
    
    def load_decorations(self):
        """Load ALL decorative elements to fill the arena"""
        try:
            # Load all decoration images
            predator_plant = pygame.image.load("asset1/PNG/Predator_plant.png").convert_alpha()
            fairy = pygame.image.load("asset1/PNG/Fairys.png").convert_alpha()
            stalactite = pygame.image.load("asset1/PNG/stalactites.png").convert_alpha()
            shinies = pygame.image.load("asset1/PNG/shinies.png").convert_alpha()
            
            # Load additional decorations
            try:
                details = pygame.image.load("asset1/PNG/Details.png").convert_alpha()
                clouds_tiles = pygame.image.load("asset1/PNG/Clouds_in_tiles.png").convert_alpha()
                spikes = pygame.image.load("asset1/PNG/Spikes.png").convert_alpha()
            except:
                details = None
                clouds_tiles = None
                spikes = None
            
            # Scale decorations
            predator_plant_large = pygame.transform.scale(predator_plant, (70, 80))
            predator_plant_small = pygame.transform.scale(predator_plant, (45, 55))
            fairy = pygame.transform.scale(fairy, (35, 35))
            stalactite_large = pygame.transform.scale(stalactite, (50, 60))
            stalactite_small = pygame.transform.scale(stalactite, (30, 40))
            shinies = pygame.transform.scale(shinies, (40, 40))
            
            if spikes:
                spikes = pygame.transform.scale(spikes, (60, 30))
            
            # ===== TOP AREA (Stalactites and fairies) =====
            top_decorations = [
                (120, 40, stalactite_large, "back"),
                (300, 30, stalactite_small, "back"),
                (480, 35, stalactite_large, "back"),
                (660, 25, stalactite_small, "back"),
                (840, 45, stalactite_large, "back"),
                
                # Flying fairies
                (200, 180, fairy, "mid"),
                (500, 160, fairy, "mid"),
                (760, 190, fairy, "mid"),
                (380, 250, fairy, "mid"),
                (600, 260, fairy, "mid"),
            ]
            
            # ===== GROUND LEVEL (Plants and details) =====
            ground_decorations = [
                (80, self.height - 120, predator_plant_large, "mid"),
                (880, self.height - 115, predator_plant_large, "mid"),
                (350, self.height - 110, predator_plant_small, "mid"),
                (610, self.height - 110, predator_plant_small, "mid"),
                (180, self.height - 100, predator_plant_small, "mid"),
                (780, self.height - 105, predator_plant_small, "mid"),
            ]
            
            # ===== SHINIES (Glowing effects scattered) =====
            shiny_positions = [
                (240, 310, shinies, "mid"),
                (720, 320, shinies, "mid"),
                (140, 200, shinies, "mid"),
                (820, 210, shinies, "mid"),
                (480, 170, shinies, "mid"),
            ]
            
            # ===== SPIKES (Hazards on platforms) =====
            if spikes:
                spike_positions = [
                    (220, 330, spikes, "mid"),
                    (740, 330, spikes, "mid"),
                ]
                top_decorations.extend(spike_positions)
            
            # Add all decorations
            for x, y, img, layer in top_decorations + ground_decorations + shiny_positions:
                rect = img.get_rect(center=(x, y))
                self.decorations.append({"image": img, "rect": rect, "layer": layer})
            
            print("✅ Loaded ALL decorations - Arena is fully populated!")
        except Exception as e:
            print(f"⚠️ Error loading decorations: {e}")
    
    def update_camera(self, player_pos):
        """Update camera for parallax effect"""
        # Smooth camera follow for parallax layers
        target_x = (player_pos[0] - self.width // 2) * 0.05
        target_y = (player_pos[1] - self.height // 2) * 0.05
        
        # Smooth interpolation
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Calculate parallax offsets for different layers
        self.parallax_offset_x = self.camera_x
        self.parallax_offset_y = self.camera_y
    
    def draw(self, screen):
        """Draw all arena layers with proper depth sorting"""
        # ===== BACKGROUND LAYERS (Parallax) =====
        # Layer 1: Sky (no parallax - static background)
        screen.blit(self.bg_sky, (0, 0))
        
        # Layer 2: Clouds (slow parallax)
        if self.bg_clouds:
            cloud_x = -self.parallax_offset_x * 0.2
            cloud_y = -self.parallax_offset_y * 0.2
            screen.blit(self.bg_clouds, (cloud_x, cloud_y))
        
        # Layer 3: Flora 1 (medium parallax - distant plants)
        if self.bg_flora1:
            flora1_x = -self.parallax_offset_x * 0.4
            flora1_y = -self.parallax_offset_y * 0.4
            screen.blit(self.bg_flora1, (flora1_x, flora1_y))
        
        # ===== BACK DECORATIONS (Behind everything) =====
        for decoration in self.decorations:
            if decoration.get("layer") == "back":
                screen.blit(decoration["image"], decoration["rect"])
        
        # Layer 4: Flora 2 (faster parallax - closer plants)
        if self.bg_flora2:
            flora2_x = -self.parallax_offset_x * 0.6
            flora2_y = -self.parallax_offset_y * 0.6
            screen.blit(self.bg_flora2, (flora2_x, flora2_y))
        
        # ===== MID DECORATIONS (Between background and gameplay) =====
        for decoration in self.decorations:
            if decoration.get("layer") == "mid":
                screen.blit(decoration["image"], decoration["rect"])
        
        # ===== GROUND TILES (Multiple layers) =====
        # Sort by layer to draw back to front
        sorted_tiles = sorted(self.ground_tiles, key=lambda t: t.get("layer", 3))
        for tile in sorted_tiles:
            screen.blit(tile["image"], tile["rect"])
        
        # ===== OBSTACLES (Foreground - collidable objects) =====
        for obstacle in self.obstacles:
            screen.blit(obstacle["image"], obstacle["rect"])
        
        # ===== FRONT DECORATIONS (In front of everything) =====
        for decoration in self.decorations:
            if decoration.get("layer") == "front":
                screen.blit(decoration["image"], decoration["rect"])
    
    def get_obstacle_rects(self):
        """Return all obstacle collision rectangles"""
        return [obs["rect"] for obs in self.obstacles]
    
    def check_collision(self, rect):
        """Check if rect collides with any obstacle"""
        for obstacle in self.obstacles:
            if rect.colliderect(obstacle["rect"]):
                return True
        return False
