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

    def startSurvivalTime(self):
        self.spawnTime = time.time() 

    def updateSurvivalTime(self):
        if self.die == False:
            self.timeSurvived = time.time() - self.spawnTime       

    def stopSurvivalTime(self):
        self.timeSurvived = time.time() - self.spawnTime

