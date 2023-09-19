import os
import math
import numpy as np
import sympy
import pygame
from pygame import Rect
from sympy import Line, Point, Point2D

SENSOR_RANGE = 400
SENSOR_ANGLE_START = 0
ANGLE_INCREMENT = 20
NUM_RAYS = 20

class Sensor():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.rays = self.create_bounds(self.x, self.y)

    def create_bounds(self, start_x, start_y):
        rays = []

        for i in range(NUM_RAYS):
            angle = SENSOR_ANGLE_START + i * ANGLE_INCREMENT
            ray_end_x = start_x + SENSOR_RANGE * np.cos(np.deg2rad(angle))
            ray_end_y = start_y + SENSOR_RANGE * np.sin(np.deg2rad(angle))
            rays.append((ray_end_x, ray_end_y))

        return rays

    def detect_target(self, target_rects):  
        nn_inputs = []

        for index, target_rect in enumerate(target_rects):
            dist_to_target = math.dist((self.x, self.y), target_rect.center)
            if dist_to_target <= SENSOR_RANGE:
                nn_inputs.append(dist_to_target) 

        while len(nn_inputs) < 15:
            nn_inputs.append(SENSOR_RANGE)

        nn_inputs.sort()
        # print(f'inputs are {nn_inputs}')

        return nn_inputs

    # def target_in_bounds(self, target_rect, left_ray, right_ray):
    #     dot_1 = np.dot(target_rect.center, left_ray)
    #     dot_2 = np.dot(target_rect.center, right_ray)

    #     if (dot_1 <= 0 and dot_2 <= 0) or (dot_1 >= 0 and dot_2 >= 0):
    #         return True 