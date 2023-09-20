import pygame
import os
import numpy as np
import time
from Sensor import *

PREDATOR_IMG = pygame.image.load(os.path.join("assets", "predator.png"))
PREY_IMG = pygame.image.load(os.path.join("assets", "prey.png"))
FOOD_IMG = pygame.image.load(os.path.join("assets", "food.png"))
ENTITY_WIDTH = 20
ENTITY_HEIGHT = 20
FOOD_WIDTH = 20
FOOD_HEIGHT = 20
NUM_PREDATORS = 10
NUM_PREYS = 10
NUM_FOOD = 20
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1500
MAX_HUNGER = 30
HUNGER_STEP = 1


class Entity:
    def __init__(self):
        self.img = None
        self.x = np.random.randint(0, WINDOW_WIDTH)
        self.y = np.random.randint(0, WINDOW_HEIGHT)
        self.angle = 0
        self.velocity = 1
        self.die = False
        self.rect = pygame.Rect(self.x, self.y, ENTITY_WIDTH, ENTITY_HEIGHT)
        self.sensor = Sensor(self.rect.center[0], self.rect.center[1])

    def move(self, direction):
        if direction == 'A':
            self.rect.x -= self.velocity
        elif direction == 'D':
            self.rect.x += self.velocity
        elif direction == 'W':
            self.rect.y -= self.velocity
        elif direction == 'S':
            self.rect.y += self.velocity

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))

    def update_sensor(self, others):
        self.sensor = Sensor(self.rect.x, self.rect.y)
        possible_targets = [other.rect for other in others]
        return self.sensor.detect_target(possible_targets)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))


class Prey(Entity):
    def __init__(self):
        super().__init__()
        self.img = PREY_IMG


class Predator(Entity):
    def __init__(self):
        super().__init__()
        self.img = PREDATOR_IMG
        self.food_eaten = 0
        self.hunger = 0
        self.startTime = time.time()

    def updateHungerTimer(self):
        if (self.die == False):
            currentTime = time.time()
            elapsedTime = currentTime - self.startTime

            if (elapsedTime >= 5):
                self.increaseHunger()
                self.startTime = elapsedTime
    

    def increaseHunger(self):
        if self.hunger < MAX_HUNGER:
            self.hunger += HUNGER_STEP
            print("hunger increased to ", self.hunger)
        else:
            self.die = True
            print("died")


    def update_food_eaten(self):
        self.food_eaten += 1
