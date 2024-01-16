""" # Pygame
#import RPi.GPIO as GPIO
import pygame as pg
from pygame.locals import *
import math
import random
import time

# Classes
from boid import Boid
from hoik import Hoik
from obstacle import Obstacle
from hoikKeyboard import HoikKeyboard

import argparse
import sys
#GPIO.setmode(GPIO, BCM)
#GPIO.setwarnings(False)
#GPIO.setup(17, GPIO.OUT)

WIDTH = 1000
HEIGHT = 800
max_boids = 100  # Maximum number of boids you want in the simulation

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Key:
    def __init__(self, x, y):
        self.x = x
        self.y = y

laser = Laser(0, 0)  # Initialize the laser pointer position

def main(WIDTH, HEIGHT):
    pg.init()
    font = pg.font.Font(None, 50)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Boids")
    clock = pg.time.Clock()

    boids = [Boid(WIDTH, HEIGHT) for _ in range(max_boids)]
    
    # Initialize hoik_mouse and hoik_keyboard
    hoik_mouse = Hoik(WIDTH, HEIGHT)
    hoik_keyboard = Hoik(WIDTH, HEIGHT)
    obstacles = [Obstacle(WIDTH, HEIGHT) for _ in range(0)]

    running = True
    game_over = False

    # Track which boids have been consumed by the keyboard hoik in the current frame
    consumed_boids = set()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))

        if not game_over:
            laser.x, laser.y = pg.mouse.get_pos()
            mouse_x, mouse_y = hoik_mouse.position
#            Key.x, Key.y = HoikKeyboard.get_position()
#            keyboard_x, keyboard_y = hoik_keyboard.position

            for boid in boids:
                boid.draw(screen)
                boid.update(boids, [hoik_mouse, hoik_keyboard], obstacles)

                # Check if this boid has been consumed by the keyboard hoik
                if boid.eaten == 0:
#                    if (hoik_keyboard.position - boid.position).length() < hoik_keyboard.size + 2:
#                       hoik_keyboard.score += 1
#                       boid.eaten = 1
#                        consumed_boids.add(boid)
                    if (hoik_mouse.position - boid.position).length() < hoik_mouse.size + 2:
                        hoik_mouse.score += 1
                        boid.eaten = 1
                        consumed_boids.add(boid)

            hoik_mouse.draw(screen)
            hoik_mouse.update(boids, hoik_mouse, laser.x, laser.y)
            hoik_mouse.grow(boids)
            hoik_mouse.shrink()

#            hoik_keyboard.draw(screen)
#            hoik_keyboard.update(boids, hoik_keyboard, Key.x, Key.y)
#            hoik_keyboard.grow(boids)
#            hoik_keyboard.shrink()


            # Display scores for each hoik
            score_text_mouse = font.render(f"Mouse Hoik Score: {hoik_mouse.score}", True, (255, 255, 255))
            score_text_keyboard = font.render(f"Keyboard Hoik Score: {hoik_keyboard.score}", True, (255, 255, 255))
            screen.blit(score_text_mouse, (10, 10))
            screen.blit(score_text_keyboard, (590, 10))

            if (hoik_mouse.score + hoik_keyboard.score) == max_boids:
                game_over = True
                if hoik_mouse.score > hoik_keyboard.score:
                    winner = "Mouse Hoik"
                    game_over_text = font.render(f"Game Ended - Player1 won with a score of {hoik_mouse.score}", True, (255, 255, 255))
                elif hoik_keyboard.score > hoik_mouse.score:
                    winner = "Keyboard Hoik"
                    game_over_text = font.render(f"Game Ended - Player2 won with a score of {hoik_keyboard.score}", True, (255, 255, 255))
                else:
                    winner = "Draw!"
                    game_over_text = font.render(f"Game Ended With a Draw! {hoik_mouse.score} - {hoik_keyboard.score} ", True, (255, 255, 255))
                text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(game_over_text, text_rect)
                pg.display.flip()
                pg.time.delay(5000)
                running = False

            for obstacle in obstacles:
                obstacle.draw(screen)

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main(WIDTH, HEIGHT) """
# Pygame


import pygame as pg
from pygame.locals import *
import math
import random

# Classes
from boid import Boid
from hoik import Hoik
from obstacle import Obstacle
from hoikKeyboard import HoikKeyboard

import argparse
import sys

WIDTH = 1000
HEIGHT = 800
max_boids = 50  # Maximum number of boids you want in the simulation3

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y

laser = Laser(0, 0)  # Initialize the laser pointer position

def main(WIDTH, HEIGHT):
    pg.init()
    font = pg.font.Font(None, 50)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("2 Players Boids Game v1.55(beta)")
    clock = pg.time.Clock()

    boids = [Boid(WIDTH, HEIGHT) for _ in range(max_boids)]
    
    # Initialize hoik_mouse and hoik_keyboard
    hoik_mouse = Hoik(WIDTH, HEIGHT)
    hoik_keyboard = HoikKeyboard(WIDTH, HEIGHT, speed_factor=15.0)

    obstacles = [Obstacle(WIDTH, HEIGHT) for _ in range(0)]

    running = True
    game_over = False

    # Track which boids have been consumed by the keyboard hoik in the current frame
    consumed_boids = set()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))

        if not game_over:
            laser.x, laser.y = pg.mouse.get_pos()

            for boid in boids:
                boid.draw(screen)
                boid.update(boids, [hoik_mouse, hoik_keyboard], obstacles)

                # Check if this boid has been consumed by the keyboard hoik
                if boid.eaten == 0:
                    if (hoik_keyboard.position - boid.position).length() < hoik_keyboard.size + 2:
                        hoik_keyboard.score += 1
                        boid.eaten = 1
                        consumed_boids.add(boid)

            hoik_mouse.draw(screen)
            hoik_mouse.update(boids, [hoik_mouse, hoik_keyboard], laser.x, laser.y)
            hoik_mouse.grow(boids)
            hoik_mouse.shrink()

            # Handle the case where a boid was consumed in this frame
            for consumed_boid in consumed_boids:
                boids.remove(consumed_boid)
            consumed_boids.clear()

            hoik_keyboard.draw(screen)
            hoik_keyboard.update(boids, obstacles)
            hoik_keyboard.grow(boids)
            hoik_keyboard.shrink()

            # Display scores for each hoik
            score_text_mouse = font.render(f"Mouse Hoik Score: {hoik_mouse.score}", True, (255, 255, 255))
            score_text_keyboard = font.render(f"Keyboard Hoik Score: {hoik_keyboard.score}", True, (255, 255, 255))
            screen.blit(score_text_mouse, (10, 10))
            screen.blit(score_text_keyboard, (590, 10))

            if (hoik_mouse.score + hoik_keyboard.score) == max_boids:
                game_over = True
                if hoik_mouse.score > hoik_keyboard.score:
                    winner = "Mouse Hoik"
                    game_over_text = font.render(f"Game Ended - Player1 won with a score of {hoik_mouse.score}", True, (255, 255, 255))
                elif hoik_keyboard.score > hoik_mouse.score:
                    winner = "Keyboard Hoik"
                    game_over_text = font.render(f"Game Ended - Player2 won with a score of {hoik_keyboard.score}", True, (255, 255, 255))
                else:
                    winner = "Draw!"
                    game_over_text = font.render(f"Game Ended With a Draw! {hoik_mouse.score} - {hoik_keyboard.score} ", True, (255, 255, 255))
                text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(game_over_text, text_rect)
                pg.display.flip()
                pg.time.delay(5000)
                running = False

            for obstacle in obstacles:
                obstacle.draw(screen)
        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:  # Reset the game
                        game_over = False
                        hoik_mouse.score = 0
                        hoik_keyboard.score = 0
                        boids = [Boid(WIDTH, HEIGHT) for _ in range(max_boids)]
                    elif event.key == pg.K_q:  # Quit the game
                        running = False
        pg.display.flip()
        clock.tick(60)
        
    pg.quit()

if __name__ == "__main__":
    main(WIDTH, HEIGHT)
"""
import pygame as pg
from pygame.locals import *
import math
import random

# Classes
from boid import Boid
from hoik import Hoik
from obstacle import Obstacle
from hoikKeyboard import HoikKeyboard

import argparse
import sys

WIDTH = 1000
HEIGHT = 800
max_boids = 100  # Maximum number of boids you want in the simulation

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y

laser = Laser(0, 0)  # Initialize the laser pointer position

def main(WIDTH, HEIGHT):
    pg.init()
    font = pg.font.Font(None, 50)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("2 Players Boids Game v1.55(beta)")
    clock = pg.time.Clock()

    boids = [Boid(WIDTH, HEIGHT) for _ in range(max_boids)]

    reset_button = pg.Rect(10, HEIGHT - 50, 100, 40)
    quit_button = pg.Rect(WIDTH - 110, HEIGHT - 50, 100, 40)

    # Initialize hoik_mouse and hoik_keyboard
    hoik_mouse = Hoik(WIDTH, HEIGHT)
    hoik_keyboard = HoikKeyboard(WIDTH, HEIGHT, speed_factor=15.0)

    obstacles = [Obstacle(WIDTH, HEIGHT) for _ in range(0)]

    running = True
    game_over = False

    # Track which boids have been consumed by the keyboard hoik in the current frame
    consumed_boids = set()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # Handle reset and quit button clicks
            if event.type == pg.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    game_over = False
                    hoik_mouse.score = 0
                    hoik_keyboard.score = 0
                    boids = [Boid(WIDTH, HEIGHT) for _ in range(max_boids)]
                elif quit_button.collidepoint(event.pos):
                    running = False

        screen.fill((0, 0, 0))

        if not game_over:
            laser.x, laser.y = pg.mouse.get_pos()

            for boid in boids:
                boid.draw(screen)
                boid.update(boids, [hoik_mouse, hoik_keyboard], obstacles)

                # Check if this boid has been consumed by the keyboard hoik
                if boid.eaten == 0:
                    if (hoik_keyboard.position - boid.position).length() < hoik_keyboard.size + 2:
                        hoik_keyboard.score += 1
                        boid.eaten = 1
                        consumed_boids.add(boid)

            hoik_mouse.draw(screen)
            hoik_mouse.update(boids, [hoik_mouse, hoik_keyboard], laser.x, laser.y)
            hoik_mouse.grow(boids)
            hoik_mouse.shrink()

            # Handle the case where a boid was consumed in this frame
            for consumed_boid in consumed_boids:
                boids.remove(consumed_boid)
            consumed_boids.clear()

            hoik_keyboard.draw(screen)
            hoik_keyboard.update(boids, obstacles)
            hoik_keyboard.grow(boids)
            hoik_keyboard.shrink()

            # Display scores for each hoik
            score_text_mouse = font.render(f"Mouse Hoik Score: {hoik_mouse.score}", True, (255, 255, 255))
            score_text_keyboard = font.render(f"Keyboard Hoik Score: {hoik_keyboard.score}", True, (255, 255, 255))
            screen.blit(score_text_mouse, (10, 10))


    pg.quit()

if __name__ == "__main__":
    main(WIDTH, HEIGHT)
"""