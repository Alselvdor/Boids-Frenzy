# hoik_keyboard.py
import pygame as pg
from pygame import Vector2
from rules import Rules
import random

from flask import Flask, render_template, request
from threading import Thread

app = Flask(__name__)
directions = []
@app.route('/')
def index():
    return render_template('game.html')
    
@app.route('/move', methods=['POST'])
def movement_collection():
    if 'direction' in request.json and request.json['direction'] in ['up', 'down', 'left', 'right']:
        print(request.json)
        directions.append(request.json['direction'])
        return "Done"
    else:
        return "Missing Direction Parameter"

class HoikKeyboard(Rules):
    def __init__(self, screen_width, screen_height, speed_factor):
        super().__init__(screen_width, screen_height)
        self.position = Vector2(random.uniform(0, screen_width), random.uniform(0, screen_height))
        self.velocity = Vector2(0, 0)  # Initialize velocity to zero for keyboard control
        self.radius = 100 
        self.size = 25
        self.speed_factor = 25*speed_factor  # Add a speed factor
        self.score = 0  # Add a score attribute

        flask_thread = Thread(target=lambda: app.run('0.0.0.0', 9080))
        flask_thread.start()
    
        
    def draw(self, screen):
        pg.draw.circle(screen, (255, 0, 100), (int(round(self.position.x)), int(round(self.position.y))), int(round(self.size)))

    def update(self, boids, obstacles=[]):
        keys = pg.key.get_pressed()
        self.velocity = Vector2(0, 0)
        if len(directions):
            if directions[0] == 'left':
                self.velocity.x = -1
            if directions[0] == 'right':
                self.velocity.x = 1
            if directions[0] == 'down':
                self.velocity.y = 1
            if directions[0] == 'up':
                self.velocity.y = -1
            directions.clear();
        
        # Check if the velocity vector has a non-zero length before scaling
        if self.velocity.length() > 0:
            if self.size > 50:
                self.velocity.scale_to_length(35)  # Decrease the speed for very large hoiks
            else:
                self.velocity.scale_to_length(50)  # Use the normal speed
        else:
            self.velocity = Vector2(0, 0)  # No movement if no keys are pressed

        self.position += self.velocity
        self.bound_position()

    def get_position(self):
        # Return the hoik's current position as a tuple (x, y)
        return (self.position.x, self.position.y)

    def grow(self, boids):
        for boid in boids:
            if (boid.position - self.position).length() < self.size + 2 and not boid.eaten:
                self.size += 1  # Gain size
                boid.eaten = 1  # Mark the boid as eaten
                self.score += 1  # Increment the score only when the boid is eaten for the first time

        if self.size > 60:
            self.size = 60  # Max size

    def shrink(self):
        self.size -= 0.01  # Lose size continuously
        if self.size < 25:  # Min size
            self.size = 25
