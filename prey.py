from entity import *
import time
import pygame
import os

PREY_IMG = pygame.image.load(os.path.join("assets", "prey.png"))

class Prey(Entity):
    def __init__(self):
        super().__init__()
        self.vision_angle = 160
        self.vision_radius = 100
        self.img = PREY_IMG
        self.lineColor = (199,21,133)
        self.angleToClosest = 0
        self.fleeRadius = 150
        self.distanceToClosest = self.vision_radius+1
        self.spawnTime = time.time()
        self.timeSurvived = 0

    # def isWithinFleeRadius(self, others):
    #     if self.isInRadius(other):
    #         otherAngle = self.calculateAngle(self.img.get_rect(topleft = (self.x, self.y)).center, other.img.get_rect(topleft=(other.x, other.y)).center)
    #         leftBound = (self.angle-self.vision_angle) % 360
    #         rightBound = (self.angle+self.vision_angle) % 360
    #         if self.isWithinVisionAngle(leftBound, rightBound, otherAngle):
    #             distanceToOther = math.dist(self.img.get_rect(topleft = (self.x, self.y)).center, other.img.get_rect(topleft=(other.x, other.y)).center)
    #             if distanceToOther < minDistance:
    #                 minDistance = distanceToOther
    #                 angleDifference = self.calculateAngleDifference(self.angle, otherAngle)
    #                 closest = other


    def moveForward(self):
        self.x = self.x + self.velocity * math.cos(self.angle * math.pi / 180)
        self.y = self.y + self.velocity * math.sin(self.angle * math.pi / 180)

    def startSurvivalTime(self):
        self.spawnTime = time.time() 

    def updateSurvivalTime(self):
        if self.die == False:
            self.timeSurvived = time.time() - self.spawnTime       

