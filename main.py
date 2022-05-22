from json.encoder import ESCAPE
import pygame
from pygame.locals import *

def draw_block(surface, block, block_x, block_y):
    surface.fill((110, 110, 5))
    surface.blit(block, (block_x, block_y))
    pygame.display.update()

def main():

    pygame.init()

    surface = pygame.display.set_mode((1000, 500))
    surface.fill((110, 110, 5))

    block = pygame.image.load('resources/block.jpg').convert()
    block_x = 100
    block_y = 100
    surface.blit(block, (block_x, block_y))

    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_UP:
                    block_y -= 10
                    draw_block(surface, block, block_x, block_y)
                if event.key == K_DOWN:
                    block_y += 10
                    draw_block(surface, block, block_x, block_y)
                if event.key == K_LEFT:
                    block_x -= 10  
                    draw_block(surface, block, block_x, block_y)
                if event.key == K_RIGHT:
                    block_x += 10
                    draw_block(surface, block, block_x, block_y)

            elif event.type == QUIT:
                running = False

if __name__ == '__main__':
    main()