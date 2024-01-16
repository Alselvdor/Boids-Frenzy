# main.py
import pygame as pg
from pygame.locals import *
from boid import Boid
from hoik import Hoik
from obstacle import Obstacle
from hoikKeyboard import HoikKeyboard
import RPi.GPIO as GPIO
import smbus
import socket
from digitalio import DigitalInOut
from adafruit_character_lcd.character_lcd import Character_LCD_Mono
import board

# LCD setup
lcd_columns = 16
lcd_rows = 2
lcd_rs = DigitalInOut(board.D26)
lcd_en = DigitalInOut(board.D19)
lcd_d4 = DigitalInOut(board.D13)
lcd_d5 = DigitalInOut(board.D6)
lcd_d6 = DigitalInOut(board.D5)
lcd_d7 = DigitalInOut(board.D11)

lcd = Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)

def display_on_lcd(score_mouse, score_keyboard):
    lcd.clear()
    lcd.message = f"Score1: {score_mouse}\nScore2: {score_keyboard}"

WIDTH = 1000
HEIGHT = 800
max_boids = 50

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y

laser = Laser(0, 0)

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

    # Create a socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12344))
    server_socket.listen(1)

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

                if boid.eaten == 0:
                    if (hoik_keyboard.position - boid.position).length() < hoik_keyboard.size + 2:
                        hoik_keyboard.score += 1
                        boid.eaten = 1
                        consumed_boids.add(boid)

            hoik_mouse.draw(screen)
            hoik_mouse.update(boids, [hoik_mouse, hoik_keyboard], laser.x, laser.y)
            hoik_mouse.grow(boids)
            hoik_mouse.shrink()

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
                display_on_lcd(hoik_mouse.score, hoik_keyboard.score)
                pg.display.flip()
                pg.time.delay(5000)
                running = False

            for obstacle in obstacles:
                obstacle.draw(screen)
        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        game_over = False
                        hoik_mouse.score = 0
                        hoik_keyboard.score = 0
                        boids = [Boid(WIDTH, HEIGHT) for _ in range(max_boids)]
                    elif event.key == pg.K_q:
                        running = False
        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main(WIDTH, HEIGHT)
