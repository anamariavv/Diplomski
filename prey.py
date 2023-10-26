from entity import *
import time
import pygame
import os

PREY_IMG = pygame.image.load(os.path.join("assets", "prey.png"))

class Prey(Entity):
    def __init__(self):
        super().__init__()
        self.vision_angle = 180
        self.vision_radius = 70
        self.img = PREY_IMG
        self.lineColor = (199,21,133)
        self.spawnTime = time.time()
        self.timeSurvived = 0

    def moveForward(self):
        self.x = self.x + self.velocity * math.cos(self.angle * math.pi / 180)
        self.y = self.y + self.velocity * math.sin(self.angle * math.pi / 180)

    def startSurvivalTime(self):
        self.spawnTime = time.time() 

    def updateSurvivalTime(self):
        if self.die == False:
            self.timeSurvived = time.time() - self.spawnTime       

