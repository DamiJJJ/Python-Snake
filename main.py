# Project - Pygame snake
# Damian Mrozek

import pygame
from pygame.locals import *
import random

SIZE = 40

class Mouse:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('resources/mouse.png').convert_alpha()
        self.parent_screen = parent_screen
        self.x = SIZE*random.randint(1, 23)
        self.y = SIZE*random.randint(1, 18)

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 23) * SIZE
        self.y = random.randint(1, 18) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/body.png').convert_alpha()
        self.head = pygame.image.load('resources/head_down.png').convert_alpha()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def set_head(self, direction):
        self.head = pygame.image.load(f'resources/head_{direction}.png').convert_alpha()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        if self.length == 1:
            self.direction = 'left'
        if not(self.direction == "right"):
            self.direction = 'left'
            self.set_head(self.direction)

    def move_right(self):
        if self.length == 1:          
            self.direction = 'right'
        if not(self.direction == "left"):
            self.direction = 'right'
            self.set_head(self.direction)

    def move_up(self):
        if self.length == 1:
            self.direction = 'up'
        if not(self.direction == 'down'):
            self.direction = 'up' 
            self.set_head(self.direction)  

    def move_down(self):
        if self.length == 1:
            self.direction = 'down'
        if not(self.direction == 'up'):
            self.direction = 'down'
            self.set_head(self.direction)

    def draw(self):
        self.parent_screen.blit(self.head, (self.x[0], self.y[0]))
        for i in range(1, self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):

        for i in range(self.length-1, 0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE    
        self.draw() 
        
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gra Snake")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.mouse = Mouse(self.surface)
        self.mouse.draw()
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def display_score(self):
        font = pygame.font.SysFont('helvetica', 30)
        score = font.render(f'Wynik: {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(score, (875, 10))

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load('resources/background.jpg')
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.mouse.draw()
        self.display_score()
        pygame.display.flip()

        # Snake colliding with Mouse
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.mouse.x, self.mouse.y):
            self.play_sound('eat')
            self.snake.increase_length()
            self.mouse.move()

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('game_over')
                raise ValueError('Game over')      

        # Snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] < 1000 and 0 <= self.snake.y[0] < 800):
            self.play_sound('game_over')
            raise ValueError('Hit the boundry')
        
        # Preventing mouse spawning inside snake
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.mouse.x, self.mouse.y):
                print("MYSZ")
                self.mouse.move()
        
         # Preventing mouse spawning inside snake
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.mouse.x, self.mouse.y):
                print("MYSZ")
                self.mouse.move()

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('helvetica', 30)
        line1 = font.render(f'Przegrałeś! Twój wynik to: {self.snake.length}', True, (255, 0, 0))
        line1_rect = line1.get_rect(center=(500, 350))
        self.surface.blit(line1, line1_rect)

        line2 = font.render('Aby zagrać ponownie wciśnij Enter. Aby opuścić naciśnij Escape!', True, (255, 255, 255))
        line2_rect = line2.get_rect(center=(500, 400))
        self.surface.blit(line2, line2_rect)
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.mouse = Mouse(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()
                    
                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except ValueError:
                self.show_game_over()
                pause = True
                self.reset()

            pygame.time.delay(150)


if __name__ == '__main__':
    game = Game()
    game.run()