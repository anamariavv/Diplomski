import pygame
import numpy as np
import math
import time

WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1500

class Entity:
    def __init__(self):
        self.img = None
        self.x = np.random.randint(0, WINDOW_WIDTH)
        self.y = np.random.randint(0, WINDOW_HEIGHT)
        self.angle = 0
        self.velocity = 1
        self.lineColor = (0,0,255)
        self.die = False
        self.closestEntity = None
        self.fitness = 0
        self.size =(32,32)
        self.surface = pygame.Surface(self.size)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.vision_rect = None
        self.startTime = 0
        self.canReproduce = False
        self.reproduce = False

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

        if closest is not None:
            self.closestEntity = closest                
        else:
            self.closestEntity = None

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

    def startReproductionTimer(self):
        self.startTime = time.time() 

    def updateReproductionTimer(self):
        timeElapsed = time.time() - self.startTime

        if(timeElapsed >= 10):
            self.canReproduce = True
            self.startTime = time.time()     

    def draw(self, surface):
        rotated_img = pygame.transform.rotate(self.img, -self.angle)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(center=(self.x, self.y)).center)
        self.rect = new_rect
        surface.blit(rotated_img, new_rect.center)

    def drawVisionLines(self, surface):
        center_x = self.img.get_rect(topleft = (self.x, self.y)).center[0]
        center_y = self.img.get_rect(topleft = (self.x, self.y)).center[1]
        x_end = center_x + self.vision_radius * math.cos(self.angle * math.pi / 180)
        y_end = center_y + self.vision_radius * math.sin(self.angle * math.pi / 180)

        self.vision_rect = pygame.Rect(self.x-self.vision_radius*2*0.5+self.size[0]*0.5, self.y-self.vision_radius*2*0.5+self.size[0]*0.5, self.vision_radius*2, self.vision_radius*2)
        pygame.draw.arc(surface, self.lineColor, self.vision_rect, -(self.vision_angle*math.pi/180)-(self.angle*math.pi/180), (self.vision_angle*math.pi/180)-(self.angle*math.pi/180))
        pygame.draw.line(surface, self.lineColor, self.img.get_rect(topleft=(self.x, self.y)).center, (x_end, y_end), 2)

    def drawLineToClosestEntity(self, surface):
        pygame.draw.rect(surface, self.lineColor ,self.img.get_rect(topleft=(self.x, self.y)), 2)

        if self.closestEntity is not None:
            pygame.draw.line(surface, self.lineColor, self.img.get_rect(topleft=(self.x, self.y)).center, self.closestEntity.img.get_rect(topleft=(self.closestEntity.x, self.closestEntity.y)).center, 2)

    def drawRectLines(self, surface):
        pygame.draw.rect(surface, self.lineColor,self.img.get_rect(topleft=(self.x, self.y)), 5)