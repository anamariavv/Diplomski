import pygame
import os
import numpy as np
import time
from Sensor import *

PREDATOR_IMG = pygame.image.load(os.path.join("assets", "predator.png"))
PREY_IMG = pygame.image.load(os.path.join("assets", "prey.png"))
NUM_PREDATORS = 10
NUM_PREYS = 10
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1500
MAX_HUNGER = 10
HUNGER_STEP = 1

class Entity:
    def __init__(self):
        self.img = None
        self.x = np.random.randint(0, WINDOW_WIDTH)
        self.y = np.random.randint(0, WINDOW_HEIGHT)
        self.angle = 0
        self.velocity = 1
        self.die = False
        self.size =(32,32)
        self.surface = pygame.Surface(self.size)
        self.surface.fill("green")
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.vision_rect = None

    def moveForward(self):
        self.x = self.x + self.velocity * math.cos(self.angle * math.pi / 180)
        self.y = self.y + self.velocity * math.sin(self.angle * math.pi / 180)

    def turn_left(self):
        self.angle -= 5
        self.angle %= 360

    def turn_right(self):
        self.angle += 5
        self.angle %= 360

    def getClosest(self, others):
        minDistance = 180
        angleDifference = 0
        closest = None

        for other in others:
            if self.isInRadius(other):
                otherAngle = self.calculateAngle(self.img.get_rect(topleft = (self.x, self.y)).center, other.img.get_rect(topleft=(other.x, other.y)).center)
                leftBound = (self.angle-self.vision_angle) % 360
                rightBound = (self.angle+self.vision_angle) % 360
                if self.isWithinVisionAngle(leftBound, rightBound, otherAngle):
                    distanceToOther = math.dist(self.img.get_rect(topleft = (self.x, self.y)).center, other.img.get_rect(topleft=(other.x, other.y)).center)
                    if distanceToOther < minDistance:
                        minDistance = distanceToOther
                        angleDifference = self.calculateAngleDifference(self.angle, otherAngle)
                        closest = other

        return closest, minDistance, angleDifference

    def isInRadius(self, other):    
        if (self.x - (other.x))**2 + (self.y - (other.y))**2 < (self.vision_radius)**2:
            return True
        return False

    def isWithinVisionAngle(self, leftBound, rightBound, angle):    
        if (leftBound < angle % 360  < rightBound) or (rightBound < leftBound and not(rightBound < angle % 360  < leftBound)): 
            return True
        return False    

    def calculateAngleDifference(self, angle1, angle2):
        angle2 %= 360
        angleDifference = angle1 - angle2

        if angleDifference > 180:
            angleDifference -= 360
        if angleDifference < -180:
            angleDifference += 360

        return angleDifference

    def calculateAngle(self, point1, point2):
        if point2[0] - point1[0] == 0:
            if point2[1] - point1[1] > 0:
                return 90
            else:
                return -90
        else:
            return math.degrees(math.atan2(1*(point2[1] - point1[1]), (point2[0] - point1[0])))  

    def collidesWithPoint(self, mouseX, mouseY):
        if self.rect.collidepoint(mouseX, mouseY):
            return True
        return False

    def draw(self, surface):
        rotated_img = pygame.transform.rotate(self.img, -self.angle)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(center=(self.x, self.y)).center)
        self.rect = new_rect
        surface.blit(rotated_img, new_rect.center)

    def drawVisionLines(self, surface):
        center_x = self.img.get_rect(topleft = (self.x, self.y)).center[0]
        center_y = self.img.get_rect(topleft = (self.x, self.y)).center[1]
        x_end = center_x + 180 * math.cos(self.angle * math.pi / 180)
        y_end = center_y + 180 * math.sin(self.angle * math.pi / 180)

        self.vision_rect = pygame.Rect(self.x-self.vision_radius*2*0.5+self.size[0]*0.5, self.y-self.vision_radius*2*0.5+self.size[0]*0.5, self.vision_radius*2, self.vision_radius*2)
        pygame.draw.arc(surface, (0,0,255), self.vision_rect, -(self.vision_angle*math.pi/180)-(self.angle*math.pi/180), (self.vision_angle*math.pi/180)-(self.angle*math.pi/180))
        pygame.draw.line(surface, (0, 0,255), self.img.get_rect(topleft=(self.x, self.y)).center, (x_end, y_end), 2)

    def drawLineToClosestEntity(self, surface, closest):
        pygame.draw.rect(surface, (100, 100, 55),self.img.get_rect(topleft=(self.x, self.y)), 2)
        pygame.draw.line(surface, (0, 0, 255), self.img.get_rect(topleft=(self.x, self.y)).center, closest.img.get_rect(topleft=(closest.x, closest.y)).center, 2)

    def drawRectLines(self, surface):
        pygame.draw.rect(surface, (255, 165, 0),self.img.get_rect(topleft=(self.x, self.y)), 5)

class Prey(Entity):
    def __init__(self):
        super().__init__()
        self.vision_angle = 120
        self.vision_radius = 70
        self.img = PREY_IMG
        self.spawnTime = time.time()
        self.timeSurvived = 0

    def startSurvivalTime(self):
        self.spawnTime = time.time() 

    def updateSurvivalTime(self):
        if self.die == False:
            self.timeSurvived = time.time() - self.spawnTime       

    def stopSurvivalTime(self):
        self.timeSurvived = time.time() - self.spawnTime

class Predator(Entity):
    def __init__(self):
        super().__init__()
        self.img = PREDATOR_IMG
        self.food_eaten = 0
        self.hunger = 0
        self.vision_angle = 60
        self.vision_radius = 180
        self.startTime = time.time()

    def updateHungerTimer(self):
        if (self.die == False):
            currentTime = time.time()
            elapsedTime = currentTime - self.startTime

            if (elapsedTime >= 2):
                self.increaseHunger()
                self.startTime = currentTime

    def increaseHunger(self):
        if self.hunger < MAX_HUNGER:
            self.hunger += HUNGER_STEP
        else:
            self.die = True

    def update_food_eaten(self):
        self.food_eaten += 1
