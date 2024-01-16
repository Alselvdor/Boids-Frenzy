# main.py
import time
import socket
from threading import Thread

import pygame as pg
from pygame.locals import *

import RPi.GPIO as GPIO
import smbus

from digitalio import DigitalInOut
from adafruit_character_lcd.character_lcd import Character_LCD_Mono
import board

from boid import Boid
from hoik import Hoik
from obstacle import Obstacle
from flask import Flask, render_template, request
from hoikKeyboard import HoikKeyboard
from hoik_mouse_new import NewHoikKeyboard


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

def display_on_lcd(hoik_mouse_new, score_keyboard):
    lcd.clear()
    lcd.message = f"Score1: {hoik_mouse_new}\nScore2: {score_keyboard}"

WIDTH = 1000
HEIGHT = 800
max_boids = 50

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y

laser = Laser(0, 0)
arduino_connected = False
def send_scores_to_arduino(hoik_mouse_new, score_keyboard):
    global arduino_connected
    if arduino_connected:
        message = f"{hoik_mouse_new} {score_keyboard}"
        try:
            client_socket.sendall(message.encode())
        except socket.error:
            print("Error sending data to Arduino")
            arduino_connected = False

def display_scores(hoik_mouse_new, hoik_keyboard):
    global arduino_connected
    
    def update_scores():
        display_on_lcd(hoik_mouse_new.score, hoik_keyboard.score)
        last_mouse_score = hoik_mouse_new.score
        last_keyboard_score = hoik_keyboard.score
        send_scores_to_arduino(hoik_mouse_new.score, hoik_keyboard.score)
    # Schedule the update function to run every 100 milliseconds
    pg.time.set_timer(USEREVENT + 1, 100)
    while True:
        for event in pg.event.get():
            if event.type == USEREVENT + 1:
                update_scores()
            elif event.type == pg.QUIT:
                return

def handle_client(server_socket, hoik_mouse_new, hoik_keyboard):
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Arduino connected from {client_address}")

            # Send the current loop index and time to the Arduino
            message = f"{hoik_mouse_new.score} {hoik_keyboard.score}"
            client_socket.sendall(message.encode())

            # Close the connection
            client_socket.close()

        except socket.timeout:
            pass  # Continue the loop if no client is connecting

def main(WIDTH, HEIGHT):
    pg.init()
    font = pg.font.Font(None, 50)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("2 Players Boids Game v1.55(beta)")
    clock = pg.time.Clock()

    boids = [Boid(WIDTH, HEIGHT) for _ in range(max_boids)]

    hoik_mouse_new = NewHoikKeyboard(WIDTH, HEIGHT, speed_factor=15.0)
    hoik_keyboard = HoikKeyboard(WIDTH, HEIGHT, speed_factor=15.0)

    obstacles = [Obstacle(WIDTH, HEIGHT) for _ in range(0)]

    running = True
    game_over = False

    consumed_boids = set()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12346))
    server_socket.listen(1)
    server_socket.settimeout(1)  # Set a timeout for accept

    waiting_for_ardunio = True

    # Start a thread to continuously update and display scores
    scores_thread = Thread(target=display_scores, args=(hoik_mouse_new, hoik_keyboard))
    scores_thread.daemon = True
    scores_thread.start()

    # Start a thread to handle socket communication
    socket_thread = Thread(target=handle_client, args=(server_socket, hoik_mouse_new, hoik_keyboard))
    socket_thread.daemon = True
    socket_thread.start()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))

        if not game_over:
            laser.x, laser.y = pg.mouse.get_pos()

            for boid in boids:
                boid.draw(screen)
                boid.update(boids, [hoik_mouse_new, hoik_keyboard], obstacles)

                if boid.eaten == 0:
                    if (hoik_keyboard.position - boid.position).length() < hoik_keyboard.size + 2:
                        hoik_keyboard.score += 1
                        boid.eaten = 1
                        consumed_boids.add(boid)

            hoik_mouse_new.draw(screen)
            hoik_mouse_new.update(boids, obstacles)
            hoik_mouse_new.grow(boids)
            hoik_mouse_new.shrink()

            for consumed_boid in consumed_boids:
                boids.remove(consumed_boid)
            consumed_boids.clear()

            hoik_keyboard.draw(screen)
            hoik_keyboard.update(boids, obstacles)
            hoik_keyboard.grow(boids)
            hoik_keyboard.shrink()

            score_text_mouse = font.render(f"Mouse Hoik Score: {hoik_mouse_new.score}", True, (255, 255, 255))
            score_text_keyboard = font.render(f"Keyboard Hoik Score: {hoik_keyboard.score}", True, (255, 255, 255))
            screen.blit(score_text_mouse, (10, 10))
            screen.blit(score_text_keyboard, (590, 10))

            if (hoik_mouse_new.score + hoik_keyboard.score) == max_boids:
                game_over = True
                pg.display.flip()
                pg.time.delay(5000)
                running = False

        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        game_over = False
                        hoik_mouse_new.score = 0
                        hoik_keyboard.score = 0
                        boids = [Boid(WIDTH, HEIGHT) for _ in range(max_boids)]
                    elif event.key == pg.K_q:
                        running = False

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main(WIDTH, HEIGHT)
