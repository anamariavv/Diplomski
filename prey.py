from entity import *
import time
import pygame
import os

PREY_IMG = pygame.image.load(os.path.join("assets", "prey.png"))

class Prey(Entity):
    def __init__(self):
        super().__init__()
        self.vision_angle = 120
        self.vision_radius = 70
        self.img = PREY_IMG
        self.lineColor = (199,21,133)
        self.spawnTime = time.time()
        self.timeSurvived = 0
        self.energy = 50
        self.canMove = False

    def moveForward(self):
        if self.energy  > 0  and self.canMove:
            new_min = 0.5
            new_max = 1.5

            energyStandardized = ((self.energy - 0) / (50 - 0)) * (new_max - new_min) + new_min

            self.x = self.x + energyStandardized * self.velocity * math.cos(self.angle * math.pi / 180)
            self.y = self.y + energyStandardized * self.velocity * math.sin(self.angle * math.pi / 180)
            self.energy -= 0.03
        else:
            self.canMove = False

    def regenerateEnergy(self):
        self.energy += 0.2

        if self.energy >= 50:
            self.canMove = True
            self.energy = 50

    def startSurvivalTime(self):
        self.spawnTime = time.time() 

    def updateSurvivalTime(self):
        if self.die == False:
            self.timeSurvived = time.time() - self.spawnTime       

    def stopSurvivalTime(self):
        self.timeSurvived = time.time() - self.spawnTime

