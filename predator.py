from entity import *
import time
import pygame
import os

PREDATOR_IMG = pygame.image.load(os.path.join("assets", "predator.png"))
MAX_HUNGER = 4
HUNGER_STEP = 1

class Predator(Entity):
    def __init__(self):
        super().__init__()
        self.img = PREDATOR_IMG
        self.food_eaten = 0
        self.hunger = 0
        self.vision_angle = 60
        self.vision_radius = 180
        self.hungerStartTime = time.time()
        self.energy = 50
        self.canMove = False

    def moveForward(self):
        if self.energy > 0:
            new_min = 0.5
            new_max = 1.5

            energyStandardized = ((self.energy - 0) / (50 - 0)) * (new_max - new_min) + new_min

            self.x = self.x + energyStandardized * self.velocity * math.cos(self.angle * math.pi / 180)
            self.y = self.y + energyStandardized * self.velocity * math.sin(self.angle * math.pi / 180)
            self.energy -= 0.01  
        else:
            self.canMove = False 
    
    def regenerateEnergy(self):
        self.energy += 0.3

        if self.energy >= 50:
            self.canMove = True
            self.energy = 50             

    def updateHungerTimer(self):
        if (self.die == False):
            currentTime = time.time()
            elapsedTime = currentTime - self.hungerStartTime

            if (elapsedTime >= 2):
                self.increaseHunger()
                self.hungerStartTime = currentTime

    def increaseHunger(self):
        if self.hunger < MAX_HUNGER:
            self.hunger += HUNGER_STEP
        else:
            self.die = True

    def update_food_eaten(self):
        self.food_eaten += 1
