import pygame
import sys
import numpy as np
from noise import snoise2
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 32
WORLD_SIZE = 16
GRAVITY = 0.5
JUMP_FORCE = -10
MOVE_SPEED = 5

# Colors
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
DIRT_BROWN = (139, 69, 19)
STONE_GRAY = (128, 128, 128)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minegraft")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE * 2
        self.velocity_y = 0
        self.jumping = False
        self.on_ground = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # Ground collision
        if self.y + self.height > WINDOW_HEIGHT - BLOCK_SIZE:
            self.y = WINDOW_HEIGHT - BLOCK_SIZE - self.height
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.jumping = True
            self.on_ground = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

class World:
    def __init__(self):
        self.blocks = np.zeros((WORLD_SIZE, WORLD_SIZE), dtype=int)
        self.generate_terrain()

    def generate_terrain(self):
        # Simple terrain generation using Perlin noise
        for x in range(WORLD_SIZE):
            height = int(snoise2(x * 0.1, 0, octaves=1, persistence=0.5) * 3 + WORLD_SIZE // 2)
            for y in range(WORLD_SIZE):
                if y > height:
                    self.blocks[x, y] = 0  # Air
                elif y == height:
                    self.blocks[x, y] = 1  # Grass
                elif y > height - 3:
                    self.blocks[x, y] = 2  # Dirt
                else:
                    self.blocks[x, y] = 3  # Stone

    def draw(self, screen, player):
        # Draw blocks relative to player position
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                if self.blocks[x, y] != 0:  # Don't draw air blocks
                    block_x = x * BLOCK_SIZE - player.x + WINDOW_WIDTH // 2
                    block_y = y * BLOCK_SIZE - player.y + WINDOW_HEIGHT // 2
                    
                    if -BLOCK_SIZE <= block_x <= WINDOW_WIDTH and -BLOCK_SIZE <= block_y <= WINDOW_HEIGHT:
                        color = {
                            1: GRASS_GREEN,
                            2: DIRT_BROWN,
                            3: STONE_GRAY
                        }.get(self.blocks[x, y], (0, 0, 0))
                        
                        pygame.draw.rect(screen, color, (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE))

def main():
    player = Player()
    world = World()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-MOVE_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            player.move(MOVE_SPEED, 0)

        # Update
        player.update()

        # Draw
        screen.fill(SKY_BLUE)
        world.draw(screen, player)
        player.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 