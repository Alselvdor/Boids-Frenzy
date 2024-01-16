import pygame as pg
from pygame import Vector2
from rules import Rules
import random
import firebase_admin
from firebase_admin import credentials, firestore
from threading import Thread

cred = credentials.Certificate("Creds/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class HoikKeyboard(Rules):
    def __init__(self, screen_width, screen_height, speed_factor):
        super().__init__(screen_width, screen_height)
        self.position = Vector2(random.uniform(0, screen_width), random.uniform(0, screen_height))
        self.velocity = Vector2(0, 0)
        self.radius = 100
        self.size = 25
        self.speed_factor = 25 * speed_factor
        self.score = 0

        firebase_thread = Thread(target=self.fetch_directions_from_firebase)
        firebase_thread.start()

    def fetch_directions_from_firebase(self):
        collection_ref = db.collection(u'player1')
        doc_ref = collection_ref.document("movements")
        Timestampx_temp = 0

        while True:  # Run indefinitely (or add a condition to exit)
            doc = doc_ref.get()
            datas = doc.to_dict() if doc.exists else {}

            Timestampx = datas.get('Timestamp', 0)

            if Timestampx != Timestampx_temp:
                direction = datas.get('Direction', None)

                if direction is not None:
                    self.update_direction(direction)
                else:
                    print("No 'Direction' key in the document!")

                Timestampx_temp = Timestampx

    def update_direction(self, direction):
        if direction == 'left':
            self.velocity.x = -1
        elif direction == 'right':
            self.velocity.x = 1
        elif direction == 'down':
            self.velocity.y = 1
        elif direction == 'up':
            self.velocity.y = -1

    def draw(self, screen):
        pg.draw.circle(screen, (255, 0, 100), (int(round(self.position.x)), int(round(self.position.y))),
                       int(round(self.size)))

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

