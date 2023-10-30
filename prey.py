from entity import *
import time
import pygame
import os

PREY_IMG = pygame.image.load(os.path.join("assets", "prey.png"))

class Prey(Entity):
    def __init__(self):
        super().__init__()
        self.vision_angle = 160
        self.vision_radius = 150
        self.dangerRadius = 60
        self.img = PREY_IMG
        self.lineColor = (199,21,133)
        self.angleToClosest = 0
        self.distanceToClosest = self.vision_radius+1
        self.spawnTime = time.time()
        self.timeSurvived = 0

    def isClosestInDangerZone(self):    
        if (self.x - (self.closestEntity.x))**2 + (self.y - (self.closestEntity.y))**2 < (self.dangerRadius)**2:
            return True

        return False

    def moveForward(self):
        self.x = self.x + self.velocity * math.cos(self.angle * math.pi / 180)
        self.y = self.y + self.velocity * math.sin(self.angle * math.pi / 180)

    def startSurvivalTime(self):
        self.spawnTime = time.time() 

    def updateSurvivalTime(self):
        if self.die == False:
            self.timeSurvived = time.time() - self.spawnTime       

    def drawDangerZone(self, surface):
        self.danger_rect = pygame.Rect(self.x-self.dangerRadius*2*0.5+self.size[0]*0.5, self.y-self.dangerRadius*2*0.5+self.size[0]*0.5, self.dangerRadius*2, self.dangerRadius*2)
        pygame.draw.arc(surface, self.lineColor, self.danger_rect, -(self.vision_angle*math.pi/180)-(self.angle*math.pi/180), (self.vision_angle*math.pi/180)-(self.angle*math.pi/180))
        pygame.draw.arc(surface, self.lineColor, self.danger_rect, -(self.vision_angle*math.pi/180)-(self.angle*math.pi/180), (self.vision_angle*math.pi/180)-(self.angle*math.pi/180))