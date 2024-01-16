# Pygame 
from pygame import Vector2
import pygame as pg

# Pygame
#import RPi.GPIO as GPIO

# Random
import random
import time
# Rules class
from rules import Rules

#GPIO.setmode(GPIO, BCM)
#GPIO.setwarnings(False)
#GPIO.setup(17, GPIO.OUT)
#GPIO.output(17, GPIO.LOW)

class Hoik(Rules):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.position = Vector2(random.randrange(0, screen_width), random.randrange(0, screen_height))
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.radius = 100 # Radius of the hoiks vision
        self.size = 20 # Size of the hoiks
        self.score = 0

    ### Draw the hoiks on the screen
    def draw(self, screen):
        pg.draw.circle(screen, (255, 0, 100), (int(round(self.position.x)), int(round(self.position.y))), int(round(self.size)))

    # Gain size when eating boids
    # Inside the Hoik class
    def grow(self, boids):
        for boid in boids:
            if (boid.position - self.position).length() < self.size + 2 and not boid.eaten:
                self.size += 1  # Gain size
                boid.eaten = 1  # Mark the boid as eaten
                self.score += 1  # Increment the score only when the boid is eaten for the first time
                #GPIO.output(17, GPIO.HIGH)
                #GPIO.output(17, GPIO.LOW)
        if self.size > 20:
            self.size = 20  # Max size


    # Lose size when not eating boids for a while 
    def shrink(self):
        self.size -= 0.01 # Lose size continuously
        if self.size < 5: # Min size
            self.size = 5 

    def reproduce(self, hoiks):
        if len(hoiks) < 10:
            if self.size > 10:
                if random.random() < 0.001:
                    # Reproduce a new hoik next to the parent without overlapping and crashin the game
                    hoiks.append(Hoik(self.screen_width, self.screen_height))
                    hoiks[-1].position = self.position + Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

    def die(self, hoiks):
        # Die if there are too many hoiks
        if len(hoiks) > 2:
            if self.size < 6:
                if random.random() < 0.0005:
                    hoiks.remove(self)
            # Randomly die, maybe heart attack or something
            if random.random() < 0.0001:
                hoiks.remove(self)
    
    ### Update the position of the hoiks
    def update(self, boids, hoiks, laser_x, laser_y, obstacles=[]):
        # Calculate the direction vector from hoik to the laser pointer
        direction = Vector2(laser_x - self.position.x, laser_y - self.position.y)
        # Normalize the direction vector
        if direction.length() > 0:
            direction.normalize_ip()
            
        # Adjust speed based on size
        if self.size > 10:
            speed = 7
        else:
            speed = 10

        # Update the position of the hoik based on the direction vector and speed
        self.position.x += direction.x * speed
        self.position.y += direction.y * speed

        # Wrap the position of the hoik
        Rules.bound_position(self)

        # Weights of the rules
        w1 = 0.7  # Weight for chasing the closest boid
        w2 = 0.5  # Keep distance away from other hoiks
        w3 = 0.4  # Match velocity

"""         # Rules hoiks follow
        chase = w1 * Rules.chase(self, boids)  # Chase the closest boid
        efficiency = w2 * Rules.keep_distance_away(self, hoiks, 50)  # Keep distance away from other hoiks
        dodge = Rules.tend_to_place(self, obstacles)  # Avoid obstacles
        align = w3 * Rules.match_velocity(self, boids)  # Match velocity



        # Update velocity
        self.velocity += chase + efficiency + align + dodge

        # Limit the speed of the hoik
        if self.velocity.length() > 10:
            self.velocity.scale_to_length(10)

        # Update position based on velocity """


        






